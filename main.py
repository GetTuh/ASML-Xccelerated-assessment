def fetch_vms(project,zone):
    c=InstancesClient.from_service_account_json(".json")
    instances = c.list(project=project, zone=zone)
    return instances

def fetch_snapshots(projects):
    c=SnapshotsClient.from_service_account_json(".json")
    snapshots = c.list(project=project)
    return snapshots