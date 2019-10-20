import pandas as pd
import datetime

def remove_timezone(data):
    if not type(data.starttime[0]) == datetime.datetime:
        data = convert_timestamps_to_datetime(data)
    data['starttime'] = data['starttime'].apply(lambda dt: dt.replace(tzinfo=None))
    data['endtime'] = data['starttime'].apply(lambda dt: dt.replace(tzinfo=None))
    return data


def convert_timestamps_to_datetime(data):
    print("converting start and end timestamps to datetime objects")
    if not type(data['starttime'][0]) == datetime.datetime:
        data['starttime'] = pd.to_datetime(data['starttime'])
    if not type(data['endtime'][0]) == datetime.datetime:
        data['endtime'] = pd.to_datetime(data['endtime'])
    return data
