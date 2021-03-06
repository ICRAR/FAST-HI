####################################
#
#    ICRAR - International Centre for Radio Astronomy Research
#    (c) UWA - The University of Western Australia
#    Copyright by UWA (in the framework of the ICRAR)
#    All rights reserved
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston,
#    MA 02111-1307  USA
#
"""
FAST-HI Baseline subtraction module
"""

import os
import sys
import argparse
import casadef
import time

import utils

module_name = 'FASTbaseline'

#config file
CONFIG_DEFAULT_FILE="../conf/baseline.conf"
config = utils.RawConfigParser()
config.add_section('Baseline')
config.set('Baseline', 'datacolumn', 'corrected') 
config.set('Baseline', 'antenna', '')
config.set('Baseline', 'field', '')
config.set('Baseline', 'spw', '')
config.set('Baseline', 'timerange', '')
config.set('Baseline', 'scan', '')
config.set('Baseline', 'pol', '')
config.set('Baseline', 'intent', '')
config.set('Baseline', 'maskmode', 'auto')
config.set('Baseline', 'thresh', '5.0')
config.set('Baseline', 'avg_limit', '4')
config.set('Baseline', 'minwidth', '4')
config.set('Baseline', 'edge', '[0, 0]')
config.set('Baseline', 'blmode', 'fit')
config.set('Baseline', 'dosubtract', 'True')
config.set('Baseline', 'blformat', 'cvs')
config.set('Baseline', 'bloutput',  "")
config.set('Baseline', 'bltable', "")
config.set('Baseline', 'blfunc', "poly")
config.set('Baseline', 'order', '5')
config.set('Baseline', 'npiece', '2')
config.set('Baseline', 'applyfft', 'True')
config.set('Baseline', 'fftmethod', "fft")
config.set('Baseline', 'fftthresh', '3.0')
config.set('Baseline', 'addwn', '[0]')
config.set('Baseline', 'rejwn', '[0]')
config.set('Baseline', 'clipthresh', '3.0')
config.set('Baseline', 'clipniter', '0')
config.set('Baseline', 'blparam', "")
config.set('Baseline', 'verbose', 'False')
config.set('Baseline', 'showprogress', 'False')
config.set('Baseline', 'minnrow', '1000')
config.set('Baseline', 'overwrite', 'True') 
    
sd.rcParams['verbose'] = True
sd.rcParams['scantable.storage'] = 'memory'

def FASTbaseline(infile, outfile):

    casalog.post('Baseline subtraction for %s' % infile)

    ##########################
    # Fit and remove the baseline
    ##########################
    sdbaseline(infile  = infile,
    datacolumn         = config.get('Baseline', 'datacolumn'), 
    antenna            = config.get('Baseline', 'antenna'),
    field              = config.get('Baseline', 'field'),
    spw                = config.get('Baseline', 'spw'),
    timerange          = config.get('Baseline', 'timerange'),
    scan               = config.get('Baseline', 'scan'),
    pol                = config.get('Baseline', 'pol'),
    intent             = config.get('Baseline', 'intent'),
    maskmode           = config.get('Baseline', 'maskmode'),
    thresh             = config.getfloat('Baseline', 'thresh'),
    avg_limit          = config.getint('Baseline', 'avg_limit'),
    minwidth           = config.getint('Baseline', 'minwidth'),
    edge               = config.getintlist('Baseline', 'edge'),
    blmode             = config.get('Baseline', 'blmode'),
    dosubtract         = config.getboolean('Baseline', 'dosubtract'),
    blformat           = config.get('Baseline', 'blformat'),
    bloutput           = config.get('Baseline', 'bloutput'),
    bltable            = config.get('Baseline', 'bltable'),
    blfunc             = config.get('Baseline', 'blfunc'),
    order              = config.getint('Baseline', 'order'),
    npiece             = config.getint('Baseline', 'npiece'),
    applyfft           = config.getboolean('Baseline', 'applyfft'),
    fftmethod          = config.get('Baseline', 'fftmethod'),
    fftthresh          = config.getfloat('Baseline', 'fftthresh'),
    addwn              = config.getfloatlist('Baseline', 'addwn'),
    rejwn              = config.getfloatlist('Baseline', 'rejwn'),
    clipthresh         = config.getfloat('Baseline', 'clipthresh'),
    clipniter          = config.getint('Baseline', 'clipniter'),
    blparam            = config.get('Baseline', 'blparam'),
    verbose            = config.getboolean('Baseline', 'verbose'),
    showprogress       = config.getboolean('Baseline', 'showprogress'),
    minnrow            = config.getint('Baseline', 'minnrow'),
    overwrite          = config.getboolean('Baseline', 'overwrite'), 
    outfile            = outfile)

def write_default_config():  
    # Writing out configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    casalog.post('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file for the spectral-line data reduction pipeline")
    parser.add_argument("--infile", help="Observation measurement set")
    parser.add_argument("--outfile", help="Intermidiate output measurement set")
    args = parser.parse_args(utils.cmdline_cleanup())

    casalog.post('---Logging for ' + module_name)
    casalog.post('Command line:' + str(args))
    casalog.post('CASA version: ' + casadef.casa_version)

    config_file = CONFIG_DEFAULT_FILE
    if args.config:
        if os.path.isfile(args.config):
            config_file=args.config
        else:
            casalog.post('Configuration ' + args.config + ' does not exist.', priority="SEVERE")
            sys.exit()
    else:
        if not os.path.isfile(config_file):
            write_default_config()
            casalog.post('Check configuration and re-run the module.')
            sys.exit()

    # read configuration file
    casalog.post('Using configuration from %s' % config_file)
    config.read(config_file)

    utils.check_ioargs(args, casalog)

    FASTbaseline(infile=args.infile, outfile=args.outfile)

if __name__ == "__main__":
    main()