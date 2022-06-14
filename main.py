import sys
from tabulate import tabulate
from datetime import datetime
import time

import GCP_API

date_today = str(datetime.now())[0:10]


def stringToTimestamp(string):
    string = string.replace("T", " ")[:-6]
    return(datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f'))


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


def backup_done_today(project, vm):
    # Check if first 9 characters are the same
    dt = date_today
    snapshots = GCP_API.fetch_snapshots(project)
    has_backup_been_done_today = False
    for item in snapshots.items:
        # TODO: change date checking logic to timestamps instead of string
        if(item.creation_timestamp[0:10] == dt):
            has_backup_been_done_today = True
    return has_backup_been_done_today


def backup2(project, zone):
    #TODO: zonalOperations (ZoneOperationsClient)
    vms = GCP_API.fetch_vms(project, zone)
    for vm in vms.items:
        if(vm.labels['backup'] == 'true'):
            print(f'{vm.name} has "backup" label')
            if(backup_done_today(project, vm)):
                print("Backup has already been done today.")
            else:
                GCP_API.create_snapshot(
                    project, zone, vm.disks[0], f'{vm.name}-{date_today}')
        else:
            print(f'{vm.name} has no "backup" label')


def backup3(project, zone):
    vms = GCP_API.fetch_vms(project, zone)
    for vm in vms.items:
        print(vm.creation_timestamp)
    # GCP_API.delete_snapshot(project, snapshot_name)
    return 0


def main(mode, zone=0):
    project = 'xcc-assessment-jakub'
    if(mode == "backup-1"):
        backup1(project, zone)
    if(mode == 'backup-2'):
        backup2(project, zone)
    if(mode == 'backup-3'):
        backup3(project, zone)


if(len(str(sys.argv)) == 3):
    main(str(sys.argv[1]), str(sys.argv[2]))
else:
    main(str(sys.argv[1]), 'europe-west4-a')
