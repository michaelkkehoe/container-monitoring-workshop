import os
import signal
import subprocess
import time

from cgroup import Cgroup
import helpers

import numpy

CGROUP_DIR = "/sys/fs/cgroup/cpu,cpuacct/"
DEVNULL = open(os.devnull, 'w')

cpu_stat_nr_throttle_prev = 0
cpu_stat_throttled_time_prev = 0


def collect_cpu(cgroup_name):
    """
      Collect the average CPU utilization over a minute period
    """
    cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
    cpu_stats = helpers.parse_fk(open(os.path.join(cgroup_stats_dir, 'cpu.stat'), 'r').read())

    global cpu_stat_nr_throttle_prev
    global cpu_stat_throttled_time_prev
    cpu_stat_nr_throttle_curr = cpu_stats['nr_throttled']
    cpu_stat_throttled_time_curr = cpu_stats['throttled_time']

    # TODO by attendees: Calculate the number of throttles since the last measurement time

    # TODO by attendees: Calculate the amount of time the cgroup is throttled (in ms) since the last measurement time

    return cpu_stat_nr_throttle, cpu_stat_throttled_time
    

if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_102')
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
        cg = Cgroup('level_102')
        cg.add_task(pid)

    # Create a cgroup called "level_102", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_102')
    cg.set_shares(1)
    cg.set_cores(1)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen([helpers.sysbench(),
                           "--test=cpu",
                           "--cpu-max-prime=1000000000",
                           "--num-threads=2",
                           "--max-time=300",
                           "--forced-shutdown=0",
                           "run"],
                           stderr=DEVNULL,
                           stdout=DEVNULL,
                           preexec_fn=in_my_cgroup)


    # Run the monitoring loop, report every 60 seconds
    while True:
        print collect_cpu("level_102")
        time.sleep(10)
