import sys
from tabulate import tabulate

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


def backup1(project, zone):
    vms = fetch_vms(project, zone)
    tableData = []
    for vm in vms.items:
        disk = vm.disks[0].source.split('/')[-1]
        if(vm.labels['backup'] == 'true'):
            snapshots = fetch_snapshots(project)
            tableData.append([vm.name, vm.labels['backup'],
                             disk, snapshots.items[0].creation_timestamp])
        else:
            tableData.append([vm.name, vm.labels['backup'], disk, "Never"])

    print(tabulate(tableData, headers=[
          "Instance", "Backup Enabled", "Disk", "Last Backup"]))


def main(mode, zone=0):
    project = 'xcc-assessment-jakub'
    if(mode == "backup-1"):
        backup1(project, zone)


main(str(sys.argv[1]), str(sys.argv[2]))
