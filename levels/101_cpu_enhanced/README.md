# Level 101: CPU Enhanced monitoring
In the previous level, we wrote a simple program to evaluate how much CPU the container was using over a 60 second duration. While averages may be ok for some applications, you may be surprised to find how much CPU you may actually be utilizing.

## Relevant Documentation
# [cgroup v1 Documentation BWC](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt)
* [Percentiles](https://en.wikipedia.org/wiki/Percentile)

## Exercises
* Write code that provides the 99th percentile CPU usage & standard deviation of the container over a minute duration

## How to check your work
Look at the output of the program and you should see a 99th percentile usage of just over 50%
