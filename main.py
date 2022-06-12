from google.cloud import compute_v1

def fetch_vms(project, zone):
    
    c = compute_v1.InstancesClient.from_service_account_json("xcc-assessment-jakub.json")
    print(c)
    instances = c.list(project=project, zone=zone)
    return instances


def fetch_snapshots(projects):
    c = SnapshotsClient.from_service_account_json("xcc-assessment-jakub.json")
    snapshots = c.list(project=project)
    return snapshots

fetch_vms("xcc-assessment-jakub", "europe-west4-a")
