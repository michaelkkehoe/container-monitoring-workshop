# Level 100: Basic CPU monitoring
In this level, we will learn the basics of monitoring CPU usage.

## Relevant Documentation
* [cgroup v2 Documentation](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)
* [CFS Scheduler](https://www.kernel.org/doc/Documentation/scheduler/sched-design-CFS.txt)
* [cgroup CPU Accounting Controller](https://www.kernel.org/doc/Documentation/cgroup-v1/cpuacct.txt)
* [cgroup CPUSets](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt)

## Exercises
* Write code that provides the average CPU usage of the container over a minute duration

## Extra information
The way we are working out the average (mean) CPU usage over a 60 second duration. This will require implementing the following formula
```
cpuacct_usage_diff_in_ns = (cpuacct_usage_curr_in_ns - cpuacct_usage_prev_in_ns) 
max_allowed_cpu_time_in_us = num_periods_elapsed * cpu_cfs_quota_in_us 
cpu_usage_percentage = (cpuacct_usage_diff_in_ns / (max_allowed_cpu_time_in_us * 1000)) * 100 
```

## How to run the excercise

## How to check your work
Look at the output of your program and you should see an average CPU usage of 50%
