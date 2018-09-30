import time

import .helpers

def collect_throttle(cgroup_name):

    throttle_data_file = os.path.join([CGROUP_DIR, cgroup_name, 'cpu.stat'])
    cpu_stats = helpers.parse_fk(throttle_data_file.read())
    num_throttle = cpu_stats['nr_throttled']
    time_throttle = cpu_stats['throttled_usec']


if __name__ == "__main__":
    while True:
        print collect_throttle("level_102")
        time.sleep(60) 
