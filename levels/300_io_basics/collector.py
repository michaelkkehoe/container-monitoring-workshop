import os
import signal
import subprocess
import time

from cgroup import Cgroup
import helpers

CGROUP_DIR = "/sys/fs/cgroup/blkio/"
DEVNULL = open(os.devnull, 'w')

disk_read_prev = 0
disk_write_prev = 0


def collect_disk_io(cgroup_name):
    """
      Collect the disk IO utilization
    """
    cgroup_stats_dir = os.path.join(CGROUP_DIR)
    disk_stats = helpers.parse_nk(open(os.path.join(cgroup_stats_dir, 'blkio.throttle.io_service_bytes'), 'r').read())

    # TODO by attendees, get the read/write stats from the `202:0` device and work out the read/write bytes per second


if __name__ == "__main__":
    pid = -1

    def _termination_handler(signal, frame):
        cg = Cgroup('level_300')
        cg.remove_task(pid)
        cg.delete()

    signal.signal(signal.SIGINT,  _termination_handler)
    signal.signal(signal.SIGTERM, _termination_handler)

    def in_my_cgroup():
        """
          Function to add new process into the cgroup
        """
        pid = os.getpid()
        cg = Cgroup('level_300')
        cg.add_task(pid)

    # Create a cgroup called "level_300", set the CPU limit to 50%, which is one core
    cg = Cgroup('level_300')
    cg.set_shares(2)
    cg.set_cores(2)

    # Set read/write BPS to be 1MB/s for the drive device
    cg.set_io_read_bps("1:5", 1048576)
    cg.set_io_write_bps("202:0", 1048576)

    # Create a process and add it to the cgroup
    p1 = subprocess.Popen(["/bin/dd",
                           "if=/dev/zero",
                           "of=/tmp/test.ig",
                           "oflag=direct",
                           "bs=20M",
                           "count=1"],
                           stderr=DEVNULL,
                           stdout=DEVNULL,
                           preexec_fn=in_my_cgroup)


    # Run the monitoring loop, report every 60 seconds
    while True:
        print collect_disk_io("level_300")
        time.sleep(1)
