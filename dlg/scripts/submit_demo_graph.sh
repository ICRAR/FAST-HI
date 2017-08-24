#!/bin/bash

# Where are we?
this_dir=`dirname $0`

# Move to the directory where the python modules are
lg_dir="$this_dir"/../logical_graphs
lg_file="$lg_dir"/calibration/calibrate_pipeline.json

# Translate into a physical graph template, partition, etc, and finally submit
dlg unroll-and-partition -L "$lg_file" | dlg map | dlg submit
