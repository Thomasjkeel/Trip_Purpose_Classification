import sys
import geopandas as gpd

def main(filename):
    print(filename)
    # try:
        # gdf = gpd.read_file(filename)
    # except:
        # return print("Please enter the path to the MTL Trajet Shapefile")
    

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)