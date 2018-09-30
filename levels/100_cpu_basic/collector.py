import time
import .helpers


CGROUP_DIR = "/cgroup/"
cpu_stat_nr_periods_prev = 0
cpuacct_usage_prev_in_ns = 0


def collect_cpu(cgroup_name):
    cgroup_stats_dir = os.path.join(CGROUP_DIR, cgroup_name)
    
    cpu_stat_nr_periods_prev
    cpu_stat_nr_periods_curr
    cpuacct_usage_prev_in_ns
    cpuacct_usage_curr_in_ns
    cpu_cfs_quota_in_us

    # TODO by attendee: Calculate the CPU utilization. Use the algorithm in the exercise document
    num_periods_elapsed  = cpu_stat_nr_periods_curr - cpu_stat_nr_periods_prev
    cpuacct_usage_diff_in_ns = cpuacct_usage_curr_in_ns - cpuacct_usage_prev_in_ns 
    max_allowed_cpu_time_in_us = num_periods_elapsed * cpu_cfs_quota_in_us

    cpu_usage_percentage = 0 
    try: 
        cpu_usage_percentage = 100.0 * cpuacct_usage_diff_in_ns / (max_allowed_cpu_time_in_us * 1000) 
    except ZeroDivisionError: 
        pass 
    return cpu_usage_percentage


if __name__ == "__main__":
    while True:
        print collect_cpu("level_101")
        time.sleep(60) 
