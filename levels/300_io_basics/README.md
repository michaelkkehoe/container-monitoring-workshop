# Level 300: IO Basics
> "The "io" controller regulates the distribution of IO resources. This controller implements both weight based and absolute bandwidth or IOPS limit distribution; however, weight based distribution is available only if cfq-iosched is in use and neither scheme is available for blk-mq devices." - https://www.kernel.org/doc/Documentation/cgroup-v2.txt

## Relevant Documentation 
* [cgroup v2 Documentation](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)(IO Interface Files)

## Exercises
* Determine the read and write Bits/ second of the container
* Determine the read and write IOPS of the container
* Determine the read and write bandwidth utilization (percentage) of the contaienr
* Determine the read and write IOPS utilization (percentage) of the container

## How to check your work
You should see a write rate of 1MB/s
