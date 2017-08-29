#!/bin/bash

function print_usage {
	echo "$0 [-h | -?] [-c <config_dir>] [-d <data_dir>]"
	echo
	echo "-h, -?: Show this help"
	echo "-c <config_dir>: Indicate the directory containing all configuration files"
	echo "-d <data_dir>: Indicate the directory containing all the data"
}

# Where are we?
this_dir=`dirname $0`

# The logical graph we want to submit
lg_dir="$this_dir"/../logical_graphs
lg_file="$lg_dir"/debug/cal_nongas.json

# Handle command-line arguments
DATA_DIR=.
CONFIG_DIR="$this_dir"/../../conf

while getopts "c:d:h?" opt
do
	case "$opt" in
		c)
			CONFIG_DIR="$OPTARG"
			;;
		d)
			DATA_DIR="$OPTARG"
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

# Replace the placeholder variables (i.e., transition from a Logical Graph
# Template into a Logical Graph).
# Then translate into a physical graph template, partition, etc, and finally submit
sed "s|\${DATA_DIR}|${DATA_DIR}|g; s|\${CONFIG_DIR}|${CONFIG_DIR}|g" "$lg_file" \
	| dlg unroll-and-partition | dlg map | dlg submit
