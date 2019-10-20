import datetime
import pandas as pd
import sys
sys.path.append('../')  # link to scripts
import preprocessing.retrieve_temp_data as retrieve_temp_data
import utils.temporal_utils as temporal_utils


def calc_mean_weather(subset):
    #     print(len(subset), "hours worth of weather")
    return subset.precipitation.mean(), subset.temperature.mean()


def extract_weather_subset(row, weather_df):
    assert type(weather_df.index) == pd.core.indexes.datetimes.DatetimeIndex, (
        "the weather data needs a datetime index")

    start = row['starttime']
    end = row['endtime']
    subset_weather = weather_df.loc[start.strftime(
        "%Y-%m-%d %H:%M:%S"):end.strftime("%Y-%m-%d %H:%M:%S")]
    if len(subset_weather) < 1:
        start = start - datetime.timedelta(hours=1)
        subset_weather = weather_df.loc[start.strftime(
            "%Y-%m-%d %H:%M:%S"):end.strftime("%Y-%m-%d %H:%M:%S")]
    return subset_weather


def join_land_use_data():
    return data


def join_poi_data():
    return data


def join_weather_data(weather_filename, data):
    # weather_filename should be "../../../Data/supplementary_data/weather/mtl_temp_prec.csv"
    # TODO: if not temp_data_exists then retrieve_temp_data()
    weather_data = pd.read_csv(weather_filename)
    weather_data['dt'] = weather_data['dt'].apply(pd.to_datetime)
    weather_data = weather_data.set_index('dt')
    data = temporal_utils.convert_timestamps_to_datetime(data)

    data['av_weather'] = data.apply(lambda row: calc_mean_weather(
        extract_weather_subset(row, weather_data)), axis=1)

    # join weather data
    temp_prec = data.av_weather.apply(pd.Series)
    temp_prec.columns = ['precip', 'temperature']
    data = pd.concat([data, temp_prec], axis=1)
    return data


