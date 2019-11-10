import pandas as pd 
import sys
sys.path.append('../')  # link to scripts

import utils.direction_utils as direction_utils
import utils.spatial_utils as spatial_utils

# GLOBALS
# Canada Lambert Projection (https://epsg.io/3347)
CAN_LAM = {'init': 'epsg:3347'}
WGS_84 = {'init': 'epsg:4326'}

def create_metrics():
    return


def calc_direction(data):
    if not data.crs == WGS_84:
        print("reprojecting data into WGS_84 for direction calculation")
        data = data.to_crs({'init': 'epsg:4326'})    

    print("calculating mean direction (may take 5-10 minutes)")
    data['dir_mag'] = data.geometry.apply(direction_utils.mean_direction)
    data_dir_mag = data.dir_mag.apply(pd.Series)
    data_dir_mag.columns = ["direction", "magnitude"]
    data = pd.concat([data[data.columns[:-1]], data_dir_mag], axis=1)
    # calculate cardinal direction
    data['carddir'] = data.direction.apply(
        direction_utils.cardinal_direction)
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


def get_start_end_points(data):
    ## calculate start and end points (WGS84)
    print("converting data to WGS_84 and getting first points")
    data = data.to_crs(crs=WGS_84)
    data['start_wgs'] = data.geometry.apply(spatial_utils.get_point_from_linestring, X=0)
    data['end_wgs'] = data.geometry.apply(spatial_utils.get_point_from_linestring, X=-1)
    ## calculate start and end points (Canada Lambert)
    print("converting data to CAN_LAM and getting first points")
    data = data.to_crs(CAN_LAM)
    data['start_can'] = data.geometry.apply(spatial_utils.get_point_from_linestring, X=0)
    data['end_can'] = data.geometry.apply(spatial_utils.get_point_from_linestring, X=-1)
    return data
    

def make_binary_labels():
    return data


def make_temporal_clusters():
    return data


def make_spatial_clusters():
    return data
