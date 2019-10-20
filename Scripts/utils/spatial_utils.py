# GLOBALS
# Canada Lambert Projection (https://epsg.io/3347)
CAN_LAM = {'init': 'epsg:3347'}
WGS_84 = {'init': 'epsg:4326'}

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


def get_point_from_linestring(geom_row, X=0, behaviour='last'):
    """
    Function for extracting the Xth point of a linestring.
    Default X is the first point, default behaviour is the last

    Parameters
    ----------
    geom_row : shapely.geometry.linestring.LineString or shapely.geometry.multilinestring.MultiLineString
        A geometry row containing the route

    X : int or float
        The index of the point. Note: rounded if float

    behaviour:
        The behaviour if the index given doesn't exist
        args={'last': 'return the last available value i.e. -1', 'ignore':'ignore the row and return None'}

    Returns
    -------
    float
        lat, lng: tuple of floats
    """

    lat = None
    lng = None
    try:
        X = round(X)
    except Exception as e:
        raise TypeError(
            "Please enter a number for the index of the point within the linestring (X)")

    if behaviour in ['last', 'ignore']:
        pass
    else:
        behaviour = 'last'

    if type(geom_row) == shapely.geometry.multilinestring.MultiLineString:
        total_linestrings = len(geom_row)
        lengths = {}
        total_len = 0
        for line in range(total_linestrings):
            len_line = len(geom_row[line].xy[0])
            lengths[line] = len_line
            total_len += len_line
        if X > total_len and behaviour == 'ignore':
            return lng, lat
        elif X > total_len and behaviour == 'last' or X == -1:
            lat = geom_row[-1].xy[1][-1]
            lng = geom_row[-1].xy[0][-1]
        else:
            total = 0
            for key, val in lengths.items():
                # find the location of X within the dictionary by looking if its in a given key
                total += val
                if total >= X:
                    ind_key = key
                    # minus 1 as Python has a base-0 index
                    dict_ind = (val - (total - X)) - 1
                    break
            lat = geom_row[ind_key].xy[1][dict_ind]
            lng = geom_row[ind_key].xy[0][dict_ind]

    elif type(geom_row) == shapely.geometry.linestring.LineString:
        len_line = len(geom_row.xy)
        lng = geom_row.xy[0][X]
        lat = geom_row.xy[1][X]

    return lng, lat


def remove_third_dimension(geom):
    # from: https://gis.stackexchange.com/questions/67210/convert-3d-wkt-to-2d-shapely-geometry

    if geom.is_empty:
        return geom

    if isinstance(geom, shapely.geometry.Polygon):
        exterior = geom.exterior
        new_exterior = remove_third_dimension(exterior)

        interiors = geom.interiors
        new_interiors = []
        for int in interiors:
            new_interiors.append(remove_third_dimension(int))

        return shapely.geometry.Polygon(new_exterior, new_interiors)

    elif isinstance(geom, shapely.geometry.LinearRing):
        return shapely.geometry.LinearRing([xy[0:2] for xy in list(geom.coords)])

    elif isinstance(geom, shapely.geometry.LineString):
        return shapely.geometry.LineString([xy[0:2] for xy in list(geom.coords)])

    elif isinstance(geom, shapely.geometry.Point):
        return shapely.geometry.Point([xy[0:2] for xy in list(geom.coords)])

    elif isinstance(geom, shapely.geometry.MultiPoint):
        points = list(geom.geoms)
        new_points = []
        for point in points:
            new_points.append(remove_third_dimension(point))

        return shapely.geometry.MultiPoint(new_points)

    elif isinstance(geom, shapely.geometry.MultiLineString):
        lines = list(geom.geoms)
        new_lines = []
        for line in lines:
            new_lines.append(remove_third_dimension(line))

        return shapely.geometry.MultiLineString(new_lines)

    elif isinstance(geom, shapely.geometry.MultiPolygon):
        pols = list(geom.geoms)

        new_pols = []
        for pol in pols:
            new_pols.append(remove_third_dimension(pol))

        return shapely.geometry.MultiPolygon(new_pols)

    elif isinstance(geom, shapely.geometry.GeometryCollection):
        geoms = list(geom.geoms)

        new_geoms = []
        for geom in geoms:
            new_geoms.append(remove_third_dimension(geom))

        return shapely.geometry.GeometryCollection(new_geoms)
