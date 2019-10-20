import sys
import geopandas as gpd


def main(filename_16, filename_17):
    print(filename_16)
    # try:
        # gdf_2016 = gpd.read_file(filename)
    # except:
        # return print("Please enter the path to the MTL Trajet Shapefile")
    

if __name__ == '__main__':
    filename_16 = sys.argv[1]
    filename_17 = sys.argv[2]
    main(filename_16, filename_17)
