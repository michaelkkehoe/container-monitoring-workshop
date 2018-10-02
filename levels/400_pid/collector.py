import os
import signal
import subprocess
import time

from cgroup import Cgroup
import helpers

CGROUP_DIR = "/sys/fs/cgroup/pids/"
DEVNULL = open(os.devnull, 'w')

def collect_pid_utilization(cgroup_name):
    """
      Determine the utilization of PID's in a cgroup
    """
    cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
    # TODO by attendee: Get the current number of pids, max number of pids & determine the percentage utilization

if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_400')
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
        cg = Cgroup('level_400')
        cg.add_task(pid)

    # Create a cgroup called "level_400", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_400')
    cg.set_shares(2)
    cg.set_cores(2)

    # Set the max PID's to 10
    cg.set_max_pids(10)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen([helpers.sysbench(),
                           "--test=cpu",
                           "--cpu-max-prime=1000000000",
                           "--num-threads=1",
                           "--max-time=20",
                           "--forced-shutdown=0",
                           "run"],
                           stderr=DEVNULL,
                           stdout=DEVNULL,
                           preexec_fn=in_my_cgroup)


    # Run the monitoring loop, report every 60 seconds
    while True:
        print collect_pid_utilization("level_400")
        time.sleep(5)
