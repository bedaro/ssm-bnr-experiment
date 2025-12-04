# 0. Setup
 * Get a Stadia Maps API key and add it to a new file apis.py. See apis_example.py.
 * Download a tsv file of site info for all streams of interest from waterdata.usgs.gov and save it as flowdata/siteinfo.tsv. This file should already be present, but that is how it was created.
 * Set up Conda environments. Some notebooks below use the same environment as my "ssm-analysis" code, while others use a special "streamflows" environment based on the included YAML file.

# 1. Assemble stream climatology
 * run notebook USGSStreamflow.ipynb - downloads streamflow data from USGS
 * run notebook WYRank.ipynb - assembles complete climatology using streamflow estimation techniques as data/river_climatology.xlsx; produces representative quantile years as data/quantile_years.xlsx
 * run notebook FraserClimatology.ipynb - converts Fraser River data so it's compatible with the Puget Sound climatology

# 2. Develop the monthly 0.5 quantile normalizations, and the flow ratios between 0.5 and the rest of the quantiles
 * run notebook WYMultipliers_BNR2014.ipynb - generates stream_multipliers_simplemedian_2014.xlsx

# 3. Download the 2014 [Ecology boundary condition files](https://fortress.wa.gov/ecy/ezshare/EAP/SalishSea/SalishSeaModelBoundingScenarios.html#Opt2)

 * 2014_ssm_riv.dat
 * 2014_Exist_ssm_pnt_wq.dat
 * 2014_Exist_10_looped_ssm_pnt_wq.dat
 
These are already present in the repo. They are placed in the top-level "data" directory.

# 4. Alter the BC files for the experimental scenarios

 * run notebook MakeFiles.ipynb
