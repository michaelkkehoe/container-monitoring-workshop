import os
import signal
import subprocess
import time

from cgroup import Cgroup
import helpers

CGROUP_DIR = "/sys/fs/cgroup/memory/"
DEVNULL = open(os.devnull, 'w')

swap_events_prev = 0
failed_allocations_prev = 0

def collect_memory(cgroup_name):
    """
      Collect the average CPU utilization over a minute period
    """
    cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
    # TODO by attendees: Get the following data and return a tuple:
    # * number of swap events
    # * number of memory+Swap hit limit events

    global swap_events_prev
    global failed_allocations_prev

    swap_events = swap_events_curr - swap_events_prev
    failed_allocations = failed_allocations_curr - failed_allocations_prev

    swap_events_prev = swap_events_curr
    failed_allocations_prev = failed_allocations_curr

    return swap_events, failed_allocations

if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_201')
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
        cg = Cgroup('level_201')
        cg.add_task(pid)

    # Create a cgroup called "level_201", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_201')
    cg.set_memory_limit(2)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen([helpers.sysbench(),
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
        print collect_memory("level_201")
        time.sleep(1)
