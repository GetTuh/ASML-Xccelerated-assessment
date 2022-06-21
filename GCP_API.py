from google.cloud import compute_v1


def fetch_vms(project, zone):
    print("Fetching vms...")
    c = compute_v1.InstancesClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    instances = c.list(project=project, zone=zone)
    return instances


def fetch_snapshots(project):
    print("Fetching snapshots...")
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    snapshots = c.list(project=project)
    return snapshots


def create_snapshot(project, zone, disk, name):
    print(f'Creating snapshot with name {name}')
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    snap = {
        'name': name,
        'source_disk': disk.source  # TODO: change to source_disk_id
    }
    c.insert(project=project, snapshot_resource=snap)


def delete_snapshot(project, snapshot):
    c = compute_v1.SnapshotsClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    c.delete(project=project, snapshot=snapshot)
