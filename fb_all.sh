#!/bin/sh

rm -rf analysis/
#mkdir analysis

cp -r ../../../analysis .
# cp -r ../../analysis .


#python -m analysis.turnover_x_Aminus
# nohup srun -p x-men -c 4 --mem 62GB python -m analysis.turnover_x_Aminus > turn_analysis.out &

nohup srun -p sleuths -c 4 --mem 10GB python -m analysis.survival_postprocess > surv_pp.out &


#python -m analysis.survival_pp_x_Aminus
#python -m analysis.survival_fullt_x_Aminus

# srun -p x-men -c 4 --mem 62GB python -m analysis.survival_postprocess 


#python -m analysis.single_wtraces


#python -m analysis.overview_fb

# #srun -p x-men --mem 32GB python analysis/synapse_dynamics_fb.py
# python analysis/synapse_dynamics_fb.py
# python analysis/synapse_weight_snapshots_log_fb.py
# python analysis/synapse_weight_snapshots_fb.py
# python analysis/network_activity_fb.py
# python analysis/turnover_fb.py
#python analysis/turnover_x_Aminus.py

# nohup srun -p x-men -c 4 --mem 62GB python -m analysis.survival_x_Aminus > surv_analysis.out &


#python -m analysis.survival_x_Aminus
# python analysis/turnover_x_Aminus_fitonly_fb.py
# python analysis/active_synapses_x_Aminus_fb.py
