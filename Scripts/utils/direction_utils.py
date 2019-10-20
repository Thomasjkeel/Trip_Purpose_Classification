import math
import numpy as np
import shapely
import windrose  # use the WindroseAxes class for plotting windrose
from matplotlib import cm
import matplotlib.pyplot as plt


def calc_magnitude(pnt1, pnt2):
    """
    Function to calculate the magnitude or length of the vector between pnt 1 and pnt 2
    
    Parameters
    ----------
    pnt1 & pnt2 : numpy.array, list or tuple
        Contains two items (x,y) which are of type int or float
    Returns
    -------
    float
        magnitude or Euclidean distance between the two points
    """
    return math.sqrt(((pnt2[0] - pnt1[0])**2 + (pnt2[1] - pnt1[1])**2))


def calculate_initial_compass_bearing(pointA, pointB):
    """
    THIS FUNCTION IS FROM: https://gist.github.com/jeromer/2005586
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[1])
    lat2 = math.radians(pointB[1])

    diffLong = math.radians(pointB[0] - pointA[0])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def cardinal_direction(val):
    """
    Returns the cardinal direction of degrees between 0–360
    
    Parameters
    ----------
    val : float or int
        between 0–360 degrees
    Returns
    -------
    string
        cardinal direction
    """
    if val >= 348.75 or val < 11.25:
        direction = 'N'
    elif val >= 11.25 and val < 33.75:
        direction = 'NNE'
    elif val >= 33.75 and val < 56.25:
        direction = 'NE'
    elif val >= 56.25 and val < 78.75:
        direction = 'ENE'
    elif val >= 78.75 and val < 101.25:
        direction = 'E'
    elif val >= 101.25 and val < 123.75:
        direction = 'ESE'
    elif val >= 123.75 and val < 146.25:
        direction = 'SE'
    elif val >= 146.25 and val < 168.75:
        direction = 'SSE'
    elif val >= 168.75 and val < 191.25:
        direction = 'S'
    elif val >= 191.25 and val < 213.75:
        direction = 'SSW'
    elif val >= 213.75 and val < 236.25:
        direction = 'SW'
    elif val >= 236.25 and val < 258.75:
        direction = 'WSW'
    elif val >= 258.75 and val < 281.25:
        direction = 'W'
    elif val >= 281.25 and val < 303.75:
        direction = 'WNW'
    elif val >= 303.75 and val < 326.25:
        direction = 'NW'
    elif val >= 326.25 and val < 348.75:
        direction = 'NNW'
    return direction

# from my IGS work and someone on stackoverflow (cannot find source)


def find_resultant(from_dir, mag):
    """
    Finds the mean/resultant direction and magnitude of a list of vector angles and magnitudes
    
    Parameters
    ----------
    from_dir : numpy.array
        collection of degrees between pairs of two points 
    mag : numpy.array
        collection of magnitudes between pairs of two points
        
    Returns
    -------
    mean_dir : float
        average (mean) direction of the input
    resultant_magnitude : float
        resultant magnitude in the given direction of the input
    """
    V_east = mag * np.mean(np.sin(from_dir * np.pi/180))
    V_north = mag * np.mean(np.cos(from_dir * np.pi/180))

    mean_dir = np.arctan2(V_east, V_north) * 180/np.pi
    mean_dir = (360 + mean_dir) % 360
    mean_dir = np.mean(mean_dir)

    C = (1. / len(from_dir)) * (np.sum(np.cos(from_dir * np.pi/180)))
    S = (1. / len(from_dir)) * (np.sum(np.sin(from_dir * np.pi/180)))
    resultant_magnitude = (C**2 + S**2)*(1./2.)
    return mean_dir, resultant_magnitude


def mean_direction(linestring, plot_windrose=False):
    """
    Calculates the mean vector direction of an linestring.
    
    Divides the linestring into each point then calculates the direction and magnitude of each
    
    Parameters
    ----------
    linestring : shapely.geometry.LineString or shapely.geometry.MultiLineString
    plot_windrose : boolean
    
    Returns
    -------
    res_dir : float
        resultant direction
    res_mag : float
        resultant magnitude
    
    """
    if type(linestring) == shapely.geometry.LineString:
        # get all the x,y coordinates in an array of arrays
        xys = np.array(linestring.xy).T
    elif type(linestring) == shapely.geometry.MultiLineString:
        xys = []
        for line in linestring:
            for xy in np.array(line.xy).T:
                xys.append(xy)
        xys = np.array(xys)
   # else:
    #    return "The input needs to be a shapely.geometry.LineString or shapely.geometry.MultiLineString Object"

    line_to_bearings = []  # direction that the linestring is going in
    line_mag = []
    for ind, xy in enumerate(xys):
        if ind == len(xys)-1:
            break
        pnt1, pnt2 = tuple(xys[ind]), tuple(xys[ind+1])
        # calculate vector bearing and magnitude
        bearing = calculate_initial_compass_bearing(pnt1, pnt2)
        magnitude = calc_magnitude(pnt1, pnt2)
        # append to the lists
        line_mag.append(magnitude)
        line_to_bearings.append(bearing)
    # convert to numpy array for calculation of resultant
    line_to_bearings = np.array(line_to_bearings)
    line_mag = np.array(line_mag)
    # calculate the resultant for mean direction
    res_dir, res_mag = find_resultant(line_to_bearings, line_mag)

    if plot_windrose:
        ax = windrose.WindroseAxes.from_ax()
        max_mag = max(line_mag)
        ax.contourf(line_to_bearings,
                    line_mag, bins=np.arange(0, max_mag, (max_mag/10)), cmap=cm.hot)
        ax.set_legend()
        ax.legend(loc=6, bbox_to_anchor=(1.0, 0.2))
        plt.show()

    return res_dir, res_mag
