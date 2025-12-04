In-progress experiments with the Salish Sea Model that perform a cross
sensitivity test between point source nutrient loadings and river
flows/loadings.

The necessary code to generate the experimental boundary condition files is in
`exp_setup`.

The model runs are in the control and q\* directories, with each q\*
corresponding to a river flow quantile from a long-term Puget Sound
climatology. `hydro` directories are for the offline-coupled hydrodynamic model
which is only run once per river flow condition. `spinup` directories are for
running a 10-year water quality model spin-up period, at the end of which a
restart file is generated for day 3650. That file is then converted into an
initial condition for the 1-year `wqm` model instances.

More details on performing the experiment are in the `model running.txt` file.

# Missing Files

These files can be downloaded from [WA Ecology](https://fortress.wa.gov/ecy/ezshare/EAP/SalishSea/SalishSeaModelBoundingScenarios.html#Opt2), they are too large to upload to Github:

 * `data/2014_ssm_riv.dat`
 * `data/2014_ssm_pnt_wq.dat`
 * `data/2014_Exist_10_looped_ssm_pnt_wq.dat`
 * `wqm_inputs/2014_10_looped_ssm_obc_wq.dat`
 * `wqm_inputs/2014_ssm_obc_wq.dat`
