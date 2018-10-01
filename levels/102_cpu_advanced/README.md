# Level 102: Advanced CPU monitoring
In the 101 level, we saw that percentiles give us a little more detail about the CPU usage over a period of time. cgroups have the ability to throttle processes that are using too much CPU 'quota'. We will learn how to measure the number of throttles & throttle time.

## Relevant Documentation
* [CFS Bandiwdth Control](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt)

## Exercises
* Determine if/ how much the cgroup is throttling the container. This should be measured in a 10s duration

## How to check your work
You should see a non-zero throttle time
