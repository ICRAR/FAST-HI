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
FAST-HI Imaging module
"""

import os
import sys
import argparse
import casadef
import time

import utils

module_name = 'FASTimaging'

#config file
CONFIG_DEFAULT_FILE="../conf/imaging.conf"
config = utils.RawConfigParser()

config.add_section('Imaging')
config.set('Imaging', 'overwrite', 'False')
config.set('Imaging', 'field', '')
config.set('Imaging', 'spw', '')
config.set('Imaging', 'antenna', '')
config.set('Imaging', 'scan', '')
config.set('Imaging', 'intent', 'OBSERVE_TARGET#ON_SOURCE')
config.set('Imaging', 'mode', 'channel')
config.set('Imaging', 'nchan', '-1')
config.set('Imaging', 'start', '0')
config.set('Imaging', 'width', '1')
config.set('Imaging', 'veltype', 'radio')
config.set('Imaging', 'outframe', '')
config.set('Imaging', 'gridfunction', 'BOX')
config.set('Imaging', 'convsupport', '-1')
config.set('Imaging', 'truncate', '-1')
config.set('Imaging', 'gwidth', '-1')
config.set('Imaging', 'jwidth', '-1')
config.set('Imaging', 'imsize', '[]')
config.set('Imaging', 'cell', '')
config.set('Imaging', 'phasecenter', '')
config.set('Imaging', 'ephemsrcname', '')
config.set('Imaging', 'pointingcolumn', 'direction')
config.set('Imaging', 'restfreq', '')
config.set('Imaging', 'stokes', '')
config.set('Imaging', 'minweight', '0.1')
config.set('Imaging', 'clipminmax', 'False')
    
sd.rcParams['verbose'] = True
sd.rcParams['scantable.storage'] = 'memory'

def FASTimage(infiles, outfile):

    infiles = infiles.split(',')

    casalog.post('Imaging for %s' % infiles)

    # List the contents of the datasets
    for infile in infiles:
        listobs(vis=infile)

    ##########################
    # Perform imaging
    ##########################
    sdimaging(
        infiles            = infiles,
        outfile            = outfile,
        overwrite          = config.getboolean('Imaging', 'overwrite'),
        field              = config.get('Imaging', 'field'),
        spw                = config.get('Imaging', 'spw'),
        antenna            = config.get('Imaging', 'antenna'),
        scan               = config.get('Imaging', 'scan'),
        intent             = config.get('Imaging', 'intent'),
        mode               = config.get('Imaging', 'mode'),
        nchan              = config.getint('Imaging', 'nchan'),
        start              = config.get('Imaging', 'start'),
        width              = config.get('Imaging', 'width'),
        veltype            = config.get('Imaging', 'veltype'),
        outframe           = config.get('Imaging', 'outframe'),
        gridfunction       = config.get('Imaging', 'gridfunction'),
        convsupport        = config.getint('Imaging', 'convsupport'),
        truncate           = config.getfloat('Imaging', 'truncate'),
        gwidth             = config.getfloat('Imaging', 'gwidth'),
        jwidth             = config.getfloat('Imaging', 'jwidth'),
        imsize             = config.getintlist('Imaging', 'imsize'),
        cell               = config.get('Imaging', 'cell'),
        phasecenter        = config.get('Imaging', 'phasecenter'),
        ephemsrcname       = config.get('Imaging', 'ephemsrcname'),
        pointingcolumn     = config.get('Imaging', 'pointingcolumn'),
        restfreq           = config.get('Imaging', 'restfreq'),
        stokes             = config.get('Imaging', 'stokes'),
        minweight          = config.getfloat('Imaging', 'minweight'),
        clipminmax         = config.getboolean('Imaging', 'clipminmax'),
    )

def write_default_config():
    # Writing out configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    casalog.post('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file for imaging")
    parser.add_argument("--infiles", help="List of calibrated measurement sets")
    parser.add_argument("--outfile", help="Output image")
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

    utils.check_ioargs(args, casalog, infiles=True)

    FASTimage(infiles=args.infiles, outfile=args.outfile)

if __name__ == "__main__":
    main()