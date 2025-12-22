#!/bin/bash

set -e

outfile=results/ts.nc

. "$HOME/mambaforge/etc/profile.d/conda.sh"
. "$HOME/mambaforge/etc/profile.d/mamba.sh"
conda activate ssm-analysis
export PATH=$HOME/src/ssm-analysis:$PATH

if ! ncdump -v controltemp_surf $outfile &> /dev/null; then
	rawcdf_extract.py -v --invar temp:surf --invar temp:bottom --invar salinity:surf --invar salinity:bottom -s AdmInlet1 SwinomishChannelSouth DeceptionPassEast -- control/hydro/OUTPUT/netcdf/ssm_*.nc $outfile control
fi

for q in 1 3 5 7 9; do
	echo Q=0.$q
	if [ ! -f q0.$q/hydro/OUTPUT/netcdf/ssm_00365.nc ]; then
		echo ' (skipped, no data)'
		continue
	fi
	var=q$q
	if ncdump -v ${var}temp_surf $outfile &> /dev/null; then
		echo ' (skipped, already extracted)'
		continue
	fi
	echo
	rawcdf_extract.py -v --invar temp:surf --invar temp:bottom --invar salinity:surf --invar salinity:bottom q0.$q/hydro/OUTPUT/netcdf/ssm_*.nc $outfile $var
done
