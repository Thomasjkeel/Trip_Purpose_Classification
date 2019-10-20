import sys
import geopandas as gpd
import Scripts.utils.spatial_utils as spatial_utils
import Scripts.preprocessing.cleaning as cleaning
import Scripts.preprocessing.create_metrics as create_metrics
import Scripts.preprocessing.join_data as join_data
import Scripts.preprocessing.subset as subset
import Scripts.preprocessing.translate as translate


def preprocessing(filename):
    # try:
        # gdf = gpd.read_file(filename)
    # except:
        # return print("Please enter the path to the MTL Trajet Shapefile")
    # gdf = spatial_utils.change_projection(gdf)
    # gdf = translate.make_translations(gdf)
    # gdf = create_metrics(gdf)
    # gdf = join_data(gdf)
    # gdf = cleaning(gdf)
    # return gdf
    return


def main():
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    print(filename)
    # gdf_16 = preprocessing(filename)
    # gdf_17 = preprocessing(filename2)
    # gdf_main = subset(gdf_16, gdf_17)
    # save to file
    # output_filename = input("Enter output filename (note: .csv will be added)")
    # TODO: Think about adding some model preparation stuff here (i.e. factorisation and One-hot encoding here instead of in models/)


if __name__ == '__main__':
    main();
