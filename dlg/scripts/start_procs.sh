#!/bin/bash

# Where are we?
this_dir="`dirname $0`"

# Move to the directory where the python modules are
# That way we can refer to them in the graph using simply their file basenames
cd "$this_dir"/../../modules

# Start the Node Manager
# -v 5 gives DEBUG output, lower values are less verbose
# -d starts the process as a daemon, can be stopped via -s later on
dlg nm -v 5 -d

# Start the Data Island Manager
# -N localhost makes it point to our Node Manager running on localhost
# -d works as above
# Use -v as above if required
dlg dim -N localhost -d
