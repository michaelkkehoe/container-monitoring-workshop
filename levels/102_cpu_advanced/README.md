# Level 102: Advanced CPU monitoring
In the 101 level, we learnt that average CPU can be extremely misleading when gauging the performance of a container. Percentiles are a better way to understand what's happening. Linux cgroups provide one more additional measure for measuring performance; throttle time.

## Relevant Documentation
* [cgroup v2 Documentation](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)
* [CFS Bandiwdth Control](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt)

## Exercises
* Determine if/ how much the cgroup is throttling the container. This should be measured in a 60s duration

## How to run the excercise

## How to check your work
You should see a non-zero throttle time
