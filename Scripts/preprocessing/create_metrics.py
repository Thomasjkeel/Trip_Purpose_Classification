import pandas as pd 
import Scripts.utils.spatial_utils as spatial_utils

# GLOBALS
# Canada Lambert Projection (https://epsg.io/3347)
CAN_LAM = {'init': 'epsg:3347'}

def create_metrics():
    return


def calc_direction():
    return data


def calc_distance(data):
    """
    Calculate the distance of each journey in the data
    """
    if data.crs != CAN_LAM:
        data = spatial_utils.change_projection(data)
        # return print("please convert the projection to Canada Lambert")
        
    if 'distance_m' not in data.columns:
        print("calculating distance")
        data['distance_m'] = data['geometry'].apply(lambda row: row.length)
    else:
        print('distance already calculated')
    return data


def calc_duration(data):
    """
    Calculate the time of each journey in the data
    """
    if 'duration' not in data.columns:
        data['duration'] = pd.to_datetime(data['endtime']) - pd.to_datetime(data['starttime'])
        data['duration'] = data['duration'].apply(lambda tm: tm.seconds)
    else:
        print('duration already calculated')
    return data


def make_binary_labels():
    return data


def make_temporal_clusters():
    return data


def make_spatial_clusters():
    return data
