#!/bin/sh

rm -rf analysis/
mkdir analysis

cp -r ../../analysis/file_based analysis/file_based

# python analysis/file_based/synapse_dynamics_fb.py
# python analysis/file_based/synapse_weight_snapshots_log_fb.py
# python analysis/file_based/synapse_weight_snapshots_fb.py
# python analysis/file_based/network_activity_fb.py
python analysis/file_based/turnover_fb.py
