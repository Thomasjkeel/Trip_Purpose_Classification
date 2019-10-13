import iris
import iris.pandas as ip
import datetime
import pandas as pd
import numpy as np
import sys
import cdsapi

try:
    print("Please enter required year (2016 or 2017)")
    year = sys.argv[1]
    if not year in ['2017', '2016']:
        print("Invalid. Please enter 2016 or 2017")
        year = sys.argv[1]
except:
    print("defaulting to 2017")
    year = '2017'

required_info = {'2016':,
                '2017':{'year':'2017',
                       'month'}}
## retreive data
c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land',
    {
        'variable':[
            '2m_temperature','total_precipitation'
        ],
        'year':'2017',
        'month':[
            '09','10'
        ],
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31'
        ],
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00'
        ],
        "area": "45/-73/45/-73",    # North America study region
        "grid": "1.0/1.0",  # 1.0 longitude by 1.0 latitude
        'format':'netcdf'
    },
    'mtl_temperature_2017.nc') # save_file

