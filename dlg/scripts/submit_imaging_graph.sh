#!/bin/bash

function print_usage {
	echo "$0 [-h | -?] [-c <config_dir>] [-d <data_dir>]  [-o <obs_list>]"
	echo
	echo "-h, -?: Show this help"
	echo "-c <config_dir>:  Provide the directory with the configuration files"
	echo "-d <data_dir>:    Provide the directory where the data resides (or will reside)"
	echo "-o <obs_list>:    Provide the lists of calibrated observations"
}

# Where are we?
this_dir=`dirname $0`

# The logical graph we want to submit
lg_dir="$this_dir"/../logical_graphs
lg_file="$lg_dir"/imaging/imaging.json

# Handle command-line arguments
OBS_NAME=observations
DATA_DIR=.
CONFIG_DIR="$this_dir"/../../conf

while getopts "c:d:o:h?" opt
do
	case "$opt" in
		c)
			CONFIG_DIR="$OPTARG"
			;;
		d)
			DATA_DIR="$OPTARG"
			;;
		o)
			OBS_LIST="$OPTARG"
			;;
		[h?])
			print_usage
			exit 0
			;;
		:)
			print_usage 1>&2
			exit 1
	esac
done

now="$(date -u +%F_%T)"

# Replace the placeholder variables (i.e., transition from a Logical Graph
# Template into a Logical Graph).
# Then translate into a physical graph template, partition, etc, and finally submit
sed "s|\${CONFIG_DIR}|${CONFIG_DIR}|g; s|\${DATA_DIR}|${DATA_DIR}|g; s|\${OBS_LIST}|${OBS_LIST}|g" "$lg_file" \
	| dlg unroll-and-partition | dlg map | dlg submit -s "${OBS_NAME}_${now}"
