import os
import signal
import subprocess
import time

from cgroup import Cgroup
import helpers

import numpy

CGROUP_DIR = "/sys/fs/cgroup/cpu,cpuacct/"
DEVNULL = open(os.devnull, 'w')

cpu_stat_nr_periods_prev = 0
cpuacct_usage_prev_in_ns = 0


def collect_cpu(cgroup_name, percentile):
    """
      Collect the average CPU utilization over a minute period
    """
    percentages = []
    for x in range(0, 60):
        cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
        cpu_stats = helpers.parse_fk(open(os.path.join(cgroup_stats_dir, 'cpu.stat'), 'r').read())
        cpu_usage = helpers.parse_nlsv(open(os.path.join(cgroup_stats_dir, 'cpuacct.usage'), 'r').read())
        cpu_quota = helpers.parse_nlsv(open(os.path.join(cgroup_stats_dir, 'cpu.cfs_quota_us'), 'r').read())

        cpu_stat_nr_periods_curr = cpu_stats['nr_periods']
        cpuacct_usage_curr_in_ns = cpu_usage[0]
        cpu_cfs_quota_in_us = cpu_quota[0]

        global cpu_stat_nr_periods_prev
        global cpuacct_usage_prev_in_ns
        num_periods_elapsed  = cpu_stat_nr_periods_curr - cpu_stat_nr_periods_prev
        cpuacct_usage_diff_in_ns = cpuacct_usage_curr_in_ns - cpuacct_usage_prev_in_ns 
        max_allowed_cpu_time_in_us = num_periods_elapsed * cpu_cfs_quota_in_us

        cpu_stat_nr_periods_prev = cpu_stat_nr_periods_curr
        cpuacct_usage_prev_in_ns = cpuacct_usage_curr_in_ns

        cpu_usage_percentage = 0 
        try: 
            cpu_usage_percentage = 100.0 * cpuacct_usage_diff_in_ns / (max_allowed_cpu_time_in_us * 1000) 
        except ZeroDivisionError: 
            pass
        # TODO by attendees: Add the percentage to a list
        time.sleep(1)

    # TODO by attendees: Calculate the percentile using numpy
    return None


if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_101')
        cg.remove_task(pid)
        cg.delete()

    signal.signal(signal.SIGINT,  _termination_handler)
    signal.signal(signal.SIGTERM, _termination_handler)

    pid = -1
    def in_my_cgroup():
        """
          Function to add new process into the cgroup
        """
        pid = os.getpid()
        cg = Cgroup('level_101')
        cg.add_task(pid)

    # Create a cgroup called "level_101", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_101')
    cg.set_shares(2)
    cg.set_cores(2)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen(["/bin/sysbench",
                           "--test=cpu",
                           "--cpu-max-prime=1000000000",
                           "--num-threads=1",
                           "--max-time=300",
                           "--forced-shutdown=0",
                           "run"],
                           stderr=DEVNULL,
                           stdout=DEVNULL,
                           preexec_fn=in_my_cgroup)


    # Run the monitoring loop, report every 60 seconds
    while True:
        print collect_cpu("level_101", 99)
        # time.sleep(60)
