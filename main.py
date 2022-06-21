import sys
from tabulate import tabulate
from datetime import datetime
import time

import GCP_API


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
    snapshots = GCP_API.fetch_snapshots(project)
    has_backup_been_done_today = False
    for item in snapshots.items:
        if(stringToTimestamp(item.creation_timestamp).date() == datetime.now().date()):
            has_backup_been_done_today = True
    return has_backup_been_done_today


def backup2(project, zone):
    #TODO: zonalOperations (ZoneOperationsClient)
    vms = GCP_API.fetch_vms(project, zone)
    for vm in vms.items:
        if(vm.labels['backup'] == 'true'):
            print(f'{vm.name} has "backup" label')
            if(backup_done_today(project, vm)):
                print(f'Backup has already been done today for {vm.name}.')
            else:
                GCP_API.create_snapshot(
                    project, zone, vm.disks[0], f'{vm.name}-{datetime.now().date()}')
        else:
            print(f'{vm.name} has no "backup" label')


def findDuplicatesWithinDay(all_dates):
    duplicate_snapshots_to_delete = []
    for index in range(len(all_dates)):
        current = all_dates.pop(0)
        for data in all_dates:
            if current[2] == data[2]:
                if(current[1] < data[1]):
                    duplicate_snapshots_to_delete.append(data)
                else:
                    duplicate_snapshots_to_delete.append(current)
    return duplicate_snapshots_to_delete


def backup3(project, zone):
    snapshots = GCP_API.fetch_snapshots(project)
    all_dates = []
    for snapshot in snapshots.items:  # convert snapshot date to datestamp
        snapshot_date = stringToTimestamp(snapshot.creation_timestamp)
        timedelta = (datetime.now().date()-snapshot_date.date()).days
        if(timedelta < 7):
            all_dates.append(
                [snapshot.name, snapshot_date, snapshot_date.date()])

    duplicate_snapshots_to_delete = findDuplicatesWithinDay(all_dates)
    for snapshot in duplicate_snapshots_to_delete:
        print(f'Deleting {snapshot[0]}')
        GCP_API.delete_snapshot(project, snapshot[0])


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
