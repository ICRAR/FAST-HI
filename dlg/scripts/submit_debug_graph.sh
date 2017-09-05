#!/bin/bash

function print_usage {
	echo "$0 [-h | -?] [-c <config_dir>] [-f <in_file>]  [-o <out_dir>]"
	echo
	echo "-h, -?: Show this help"
	echo "-c <config_dir>: Provide a directory with all configuration files"
	echo "-f <in_file>: Provide the observation file name"
	echo "-o <out_dir>: Provide a directory for the output"
}

# Where are we?
this_dir=`dirname $0`

# The logical graph we want to submit
lg_dir="$this_dir"/../logical_graphs
lg_file="$lg_dir"/debug/cal_nongas.json

# Handle command-line arguments
IN_FILE=input.ms
OUT_DIR=.
CONFIG_DIR="$this_dir"/../../conf

while getopts "c:f:o:h?" opt
do
	case "$opt" in
		c)
			CONFIG_DIR="$OPTARG"
			;;
		f)
			IN_FILE="$OPTARG"
			;;
		o)
			OUT_DIR="$OPTARG"
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
sed "s|\${CONFIG_DIR}|${CONFIG_DIR}|g; s|\${IN_FILE}|${IN_FILE}|g; s|\${OUT_DIR}|${OUT_DIR}|g" "$lg_file" \
	| dlg unroll-and-partition | dlg map | dlg submit
