"""
An example of how to extract timeseries data from point locations
using WRF data stored in AWS.

Author: Michael Lindgren (malindgren@alaska.edu), SNAP
"""

def extract_data():
    dataset = xr.open_dataset('t2_hourly_wrf_GFDL-CM3_historical_1971.nc')
    res = 20000 # grid dimension of this WRF data

    x0, y0 = dataset.xc.min()-(res/2), dataset.yc.max()+(res/2)

    # get an affine transform to make the point lookups faster
    affine_dataset = rasterio.transform.from_origin(x0, y0, res, res)

    # point locations we are going to extract from the NetCDF file
    # these locations are in WGS1984 EPSG:4326
    location = {
        'Fairbanks' : (-147.716, 64.8378),
        'Greely' : (-145.6076, 63.8858),
        'Whitehorse' : (-135.074, 60.727),
        'Coldfoot' : (-150.1772, 67.2524)
    }

    # reproject the points to the wrf-polar-stereo using geopandas
    location = {location_name:Point(lng_lat) for location_name, lng_lat in location.items()}
    dataframe = pd.Series(location).to_frame('geometry')
    wrf_crs = dataset.proj_parameters
    pts_proj = gpd.GeoDataFrame(dataframe, crs={'init':'epsg:4326'}).to_crs(wrf_crs)

    # loop through the locations for extraction
    extracted = {}
    for location_name, point in pts_proj.geometry.to_dict().items():
        # get row/col from x/y using affine
        col, row = ~affine_dataset * (point.x, point.y)
        pprint(col)
        pprint(row)
        col, row = [int(i) for i in [col, row]]
        #pprint(col, row)

        # extract
        extracted[location_name] = dataset['t2'][:, row, col].values # extract t2 = temp at 2m

    pprint(extracted)
    # make a dataframe with the extracted outputs
    extracted_df = pd.DataFrame(extracted, index=dataset.time.to_index())
    extracted_df.to_csv('extracted.csv')

if __name__ == "__main__":
    from shapely.geometry import Point
    from pprint import pprint
    import xarray as xr
    import pandas as pd
    import geopandas as gpd
    import rasterio
    extract_data()
