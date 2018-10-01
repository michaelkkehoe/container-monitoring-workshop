import os
import signal
import subprocess
import time

import helpers

#from cgroups import Cgroup
from cgroup import Cgroup

CGROUP_DIR = "/sys/fs/cgroup/memory/"
DEVNULL = open(os.devnull, 'w')


def collect_memory(cgroup_name):
    """
      Collect the average CPU utilization over a minute period
    """
    cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
    # TODO by attendees: Find the right files to get the memory limit & memory usage

    memory_usage_percentage = 0
    try:
        memory_usage_percentage = 100.0 * memory_usage / memory_limit
    except ZeroDivisionError:
        pass
    return memory_usage_percentage

if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_200')
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
        cg = Cgroup('level_200')
        cg.add_task(pid)

    # Create a cgroup called "level_200", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_200')
    cg.set_memory_limit(2)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen(["/bin/sysbench",
                           "--test=cpu",
                           "--num-threads=1",
                           "--max-time=300",
                           "--forced-shutdown=0",
                           "run"],
                           stderr=DEVNULL,
                           stdout=DEVNULL,
                           preexec_fn=in_my_cgroup)


    # Run the monitoring loop, report every 60 seconds
    while True:
        print collect_memory("level_200")
        time.sleep(1)
