import sys
from tabulate import tabulate
from datetime import datetime
import time

import GCP_API
import helper


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
    #TODO: zonalOperations (ZoneOperationsClient)
    vms = GCP_API.fetch_vms(project, zone)
    for vm in vms.items:
        if(vm.labels['backup'] == 'true'):
            print(f'{vm.name} has "backup" label')
            if(helper.backup_done_today(project, vm)):
                print(f'Backup has already been done today for {vm.name}.')
            else:
                GCP_API.create_snapshot(
                    project, zone, vm.disks[0], f'{vm.name}-{datetime.now().date()}')
        else:
            print(f'{vm.name} has no "backup" label')


def backup3(project, zone):
    snapshots = GCP_API.fetch_snapshots(project)
    all_dates = []
    for snapshot in snapshots.items:  # convert snapshot date to datestamp
        snapshot_date = helper.string_to_timestamp(snapshot.creation_timestamp)
        all_dates.append(
            [snapshot.name, snapshot_date, snapshot_date.date()])

    duplicate_snapshots_to_delete = helper.find_duplicates(
        all_dates)
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
