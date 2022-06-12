import sys
from google.cloud import compute_v1

def fetch_vms(project, zone):
    c = compute_v1.InstancesClient.from_service_account_json(
        "xcc-assessment-jakub.json")
    instances = c.list(project=project, zone=zone)
    return instances


def fetch_snapshots(project):
    c = compute_v1.SnapshotsClient.from_service_account_json("xcc-assessment-jakub.json")
    snapshots = c.list(project=project)
    return snapshots


def backup1(project,zone):
    vms = fetch_vms(project, zone)
    for vm in vms.items:
        print(vm.name)
        print(vm.labels['backup'])
        print(vm.disks[0].source)
        if(vm.labels['backup']):
            snapshots=fetch_snapshots(project)
            print(snapshots.items[0].creation_timestamp)



def main(mode, zone=0):
    project = 'xcc-assessment-jakub'
    if(mode == "backup-1"):
        backup1(project, zone)
       

main(str(sys.argv[1]),str(sys.argv[2]))
