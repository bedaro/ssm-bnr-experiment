#!/bin/bash

set -e

. "$HOME/mambaforge/etc/profile.d/conda.sh"
. "$HOME/mambaforge/etc/profile.d/mamba.sh"
conda activate ssm-analysis
export PATH=$HOME/src/ssm-analysis:$PATH

if ! ncdump -v controlB1 phyto.nc &> /dev/null; then
	rawcdf_extract.py -v --invar B1:phyto --invar B2:phyto -s AdmInlet1 SwinomishChannelSouth DeceptionPassEast -- control/wqm/outputs/ssm_FVCOMICM_*.nc phyto.nc control
fi
if ! ncdump -v c2936B1 phyto.nc &> /dev/null; then
	rawcdf_extract.py -v --invar B1:phyto --invar B2:phyto control/wqm_u29.36/outputs/ssm_FVCOMICM_*.nc phyto.nc c2936
fi

for q in 1 3 5 7 9; do
	echo Q=0.$q
	for c in 4.54 10 15 20 25 29.36; do
		echo -n " C=$c"
		if [ ! -f q0.$q/wqm_$c/outputs/ssm_FVCOMICM_00365.nc ]; then
			echo ' (skipped, no data)'
			continue
		fi
		var=q${q}c${c/./}
		if ncdump -v ${var}B1 phyto.nc &> /dev/null; then
			echo ' (skipped, already extracted)'
			continue
		fi
		echo
		rawcdf_extract.py -v --invar B1:phyto --invar B2:phyto q0.$q/wqm_$c/outputs/ssm_FVCOMICM_*.nc phyto.nc $var
	done
done
