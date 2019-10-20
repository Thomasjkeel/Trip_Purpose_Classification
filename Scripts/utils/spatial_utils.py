# GLOBALS
# Canada Lambert Projection (https://epsg.io/3347)
CAN_LAM = {'init': 'epsg:3347'}

def change_projection(data):
        """
        Changes the projection of the data to EPSG:3347
        """
        # convert to Canada Lambert Projection (https://epsg.io/3347)
        if data.crs != CAN_LAM:
            print("translating data")
            data = data.to_crs(crs=CAN_LAM)
        else:
            print("correct crs")
        return data
