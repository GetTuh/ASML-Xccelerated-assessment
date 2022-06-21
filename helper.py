from datetime import datetime
import GCP_API


def string_to_timestamp(string):
    string = string.replace("T", " ")[:-6]
    return(datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f'))


def backup_done_today(project, vm):
    snapshots = GCP_API.fetch_snapshots(project)
    has_backup_been_done_today = False
    for item in snapshots.items:
        if(string_to_timestamp(item.creation_timestamp).date() == datetime.now().date()):
            has_backup_been_done_today = True
    return has_backup_been_done_today


def find_duplicates_within_day(all_dates):
    duplicate_snapshots_to_delete = []
    for index in range(len(all_dates)):
        current = all_dates.pop(0)
        timedelta = (datetime.now().date()-current[2]).days
        if(timedelta < 7):
            for date in all_dates:
                if current[2] == date[2]:
                    if(current[1] < date[1]):
                        duplicate_snapshots_to_delete.append(date)
                    else:
                        duplicate_snapshots_to_delete.append(current)
        else:
            current_week = current[1].isocalendar().week
            for date in all_dates:
                if current_week == date[1].isocalendar().week:
                    print(f'Duplicate in week {week}!')
                    if(current[1] < date[1]):
                        duplicate_snapshots_to_delete.append(date)
                    else:
                        duplicate_snapshots_to_delete.append(current)

    return duplicate_snapshots_to_delete
