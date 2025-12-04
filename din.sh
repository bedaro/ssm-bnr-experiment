#!/bin/bash
# FIXME I'm not sure I understand the purpose of this data and what we're looking for, which is important for deciding how to reduce it. ie, should I be extracting all, or just some DIN data (photic)?

set -e

. "$HOME/mambaforge/etc/profile.d/conda.sh"
. "$HOME/mambaforge/etc/profile.d/mamba.sh"
conda activate ssm-analysis
export PATH=$HOME/src/ssm-analysis:$PATH

if ! ncdump -v controlNO32 din.nc &> /dev/null; then
	rawcdf_extract.py -v --invar NH4:all --invar NO32:all -s AdmInlet1 SwinomishChannelSouth DeceptionPassEast -- control/wqm/outputs/ssm_FVCOMICM_*.nc din.nc control
fi
if ! ncdump -v c2936NO32 din.nc &> /dev/null; then
	rawcdf_extract.py -v --invar NH4:all --invar NO32:all control/wqm_u29.36/outputs/ssm_FVCOMICM_*.nc din.nc c2936
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
		if ncdump -v ${var}NO32 din.nc &> /dev/null; then
			echo ' (skipped, already extracted)'
			continue
		fi
		echo
		rawcdf_extract.py -v --invar NH4:all --invar NO32:all q0.$q/wqm_$c/outputs/ssm_FVCOMICM_*.nc din.nc $var
	done
done
