from google.cloud import compute_v1

def fetch_vms(project, zone):
    c = compute_v1.InstancesClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    instances = c.list(project=project, zone=zone)
    return instances


def fetch_snapshots(project):
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    snapshots = c.list(project=project)
    return snapshots


def create_snapshot(project, zone, disk):
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    snap = {
        'name': 'test',
        'source_disk': disk.source
    }
    response = c.insert(project=project, snapshot_resource=snap)


def delete_snapshot(project, snapshot):
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    c.delete(project=project, snapshot=snapshot)
