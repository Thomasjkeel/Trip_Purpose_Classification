import sys
import geopandas as gpd

def preprocessing(filename):
    # try:
        # gdf = gpd.read_file(filename)
    # except:
        # return print("Please enter the path to the MTL Trajet Shapefile")

    return


def main():
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    # preprocessing(filename)
    # preprocessing(filename2)
    print(filename)


if __name__ == '__main__':
    main();
