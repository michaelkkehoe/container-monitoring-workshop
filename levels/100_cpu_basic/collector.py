

def collect_nlsv():
    return

def collect_ssv():
    return

def collect_fk():
    return

def collect_nk():
    return

def collect_all_metrics_for_a_cgroup(cgroup_name):
    """
      Collect all the Cgroup CPU metrics for a cgroup
      :param string: Name of the group
      :returns: A key-value dict of metric name and value
      :rtype: dict
    """
    cgroup_dir = os.path.join(self._cgroup_slice_path(subsystem, cgroup_slice), cgroup)
    
