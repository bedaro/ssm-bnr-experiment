import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import re

def get_site_info(siteinfo_file):
    siteinfo = pd.read_csv(siteinfo_file, comment='#', sep='\t', header=0,
                           names=['Agency','Site','Full Name','Latitude','Longitude','Accuracy','Datum','Area','Contrib Area']).drop([0])
    for c in ('Latitude','Longitude'):
        siteinfo[c] = pd.to_numeric(siteinfo[c], errors='coerce')
    siteinfo['Site'] = siteinfo['Site'].astype(int)
    siteinfo.set_index('Site', inplace=True)
    namere = re.compile('^([A-Z ]+?(RIVER|CREEK))')
    names = []
    for x in siteinfo['Full Name']:
        name = namere.match(x).group(1)
        names.append(' '.join([w.capitalize() for w in name.split(' ')]))
    siteinfo['Name'] = names
    return siteinfo

def get_site_info_gdf(siteinfo_file):
    siteinfo = get_site_info(siteinfo_file)
    siteinfo_gdf = gpd.GeoDataFrame(siteinfo[['Agency','Full Name','Name']],
                                    crs='epsg:4326',
                                    geometry=[Point(xy) for xy in zip(siteinfo['Longitude'], siteinfo['Latitude'])])
    return siteinfo_gdf

def get_flows(usgsfile):
    df = pd.read_csv(usgsfile, comment="#", sep='\t', header=0,
                     names=['Agency','Site','Date','Flow','Flags'])
    if len(df) == 2:
        return None
    df = df.drop([0, 1])
    site = df['Site'].astype(int).iloc[0]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Flow'] = pd.to_numeric(df['Flow'], errors='coerce') * 0.02832 #cfs to m3/s
    df['Site'] = site
    df.set_index("Date", inplace=True)
    return df

def get_all_flows(flowdir, siteinfo):
    all_flows = {}
    for f in os.scandir("flowdata"):
        if f.name.endswith(".tsv.gz"):
            try:
                df = get_flows(f.path)
            except pd.errors.ParserError as e:
                print("WARNING: ParserError on {0}, skipping".format(f.name))
                continue
            if df is None:
                print("WARNING: {0} has no data".format(f.name))
                continue
            all_flows[siteinfo.loc[df['Site'].iloc[0], 'Name']] = df
    return all_flows
