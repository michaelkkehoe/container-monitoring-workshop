import time


def process_pid_utilization():
    """
      Determine the utilization of PID's in a cgroup
    """
    pid_current = 1
    pid_max = 5

    if pid_current > 0:
        return float(float(pid_current) / float(pid_max)) * 100
    else:
        return 0

if __name__ == "__main__":
    while True:
        print process_pid_utilization()
        time.sleep(10)
