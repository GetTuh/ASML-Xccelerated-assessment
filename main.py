import sys
from tabulate import tabulate

import GCP_API

def backup1(project, zone):
    vms = GCP_API.fetch_vms(project, zone)
    tableData = []
    for vm in vms.items:
        disk = vm.disks[0].source.split('/')[-1]
        if(vm.labels['backup'] == 'true'):
            snapshots = GCP_API.fetch_snapshots(project)
            tableData.append([vm.name, vm.labels['backup'],
                             disk, snapshots.items[0].creation_timestamp])
        else:
            tableData.append([vm.name, vm.labels['backup'], disk, "Never"])

    print(tabulate(tableData, headers=[
          "Instance", "Backup Enabled", "Disk", "Last Backup"]))


def backup2(project, zone):
    vms = GCP_API.fetch_vms(project, zone)
    for vm in vms.items:
        if(vm.labels['backup'] == 'true'):
            GCP_API.create_snapshot(project, zone, vm.disks[0])


def backup3(project, zone):
    return 0


def main(mode, zone=0):
    project = 'xcc-assessment-jakub'
    if(mode == "backup-1"):
        backup1(project, zone)
    if(mode == 'backup-2'):
        backup2(project, zone)
    if(mode == 'backup-3'):
        snapshot = "initial-snapshot"
        backup3(project, snapshot)


if(len(str(sys.argv)) == 3):
    main(str(sys.argv[1]), str(sys.argv[2]))
else:
    main(str(sys.argv[1]), 'europe-west4-a')
