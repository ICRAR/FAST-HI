#!/bin/bash

function print_usage {
	echo "$0 [-h | -?] [-A]"
	echo
	echo "-h, -?: Show this help"
	echo "-A: Expose the manager processes through all network interfaces"
}

# Handle command-line arguments
ALL_IFACES=no

while getopts "Ah?" opt
do
	case "$opt" in
		A)
			ALL_IFACES=yes
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

iface_spec=""
if [ "${ALL_IFACES}" = "yes" ]
then
	iface_spec="-H 0.0.0.0"
fi

# Where are we?
this_dir="`dirname $0`"

# Move to the directory where the python modules are
# That way we can refer to them in the graph using simply their file basenames
cd "$this_dir"/../../modules

# Start the Node Manager
# -vv gives DEBUG output. More v is more verbose. Use "-q" for quiteness
# -d starts the process as a daemon, can be stopped via -s later on
dlg nm ${iface_spec} -vv -d --cwd

# Start the Data Island Manager
# -N localhost makes it point to our Node Manager running on localhost
# -d works as above
# Use -v as above if required
dlg dim ${iface_spec} -N localhost -v -d --cwd
