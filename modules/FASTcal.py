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
FAST-HI Calibration module
"""

import os
import sys
import ConfigParser
import argparse
import casadef
import time

module_name = 'FASTcal'

#config file
CONFIG_DEFAULT_FILE="../conf/calibr.conf"
config = ConfigParser.RawConfigParser()

config.add_section('Common')
config.set('Common', 'in_path', '')
config.set('Common', 'out_path', '')

config.add_section('Calibration')
config.set('Calibration', 'calmode', 'otfraster') 
config.set('Calibration', 'fraction', '10%')
config.set('Calibration', 'noff', '-1')
config.set('Calibration', 'width', '0.5')
config.set('Calibration', 'elongated', 'False')
config.set('Calibration', 'applytable', '')
config.set('Calibration', 'interp', '')
config.set('Calibration', 'overwrite', 'True')
config.set('Calibration', 'spwmap', '')
config.set('Calibration', 'field', '')
config.set('Calibration', 'spw', '')
config.set('Calibration', 'scan', '')
config.set('Calibration', 'intent', 'OBSERVE_TARGET#ON_SOURCE')
config.set('Calibration', 'outfile_ext', '.ms.calibrated')
    
sd.rcParams['verbose'] = True
sd.rcParams['scantable.storage'] = 'memory'

def FASTcal(infile, outfile):

    infile = os.path.normpath(os.path.join(config.get('Common', 'in_path'), infile))
    if not os.path.exists(infile):
        casalog.post('%s does not exist' % infile, priority="SEVERE")
        sys.exit()

    casalog.post('Calibration for %s' % infile)
    # List the contents of the dataset
    listobs(vis=infile)
    
    #initialise
    default('sdcal')

    head, tail = os.path.splitext(os.path.basename(infile))
    if not outfile:
        outfile = os.path.join(outpath, head + config.get('Calibration', 'outfile_ext'))
    
    outpath = config.get('Common', 'out_path')
    if os.path.isdir(outpath) == False:
        os.system('mkdir ' + outpath)

    ##########################
    # Calibrate data
    ##########################
    sdcal(infile=infile,
        calmode = config.get('Calibration', 'calmode'),
        fraction = config.get('Calibration', 'fraction'),
        noff = config.getint('Calibration', 'noff'),
        width = config.getfloat('Calibration', 'width'),
        elongated = config.getboolean('Calibration', 'elongated'),
        applytable = config.get('Calibration', 'applytable'),
        interp = config.get('Calibration', 'interp'),
#        spwmap = config.get('Calibration', 'spwmap'),
        field = config.get('Calibration', 'field'),
        spw = config.get('Calibration', 'spw'),
        scan = config.get('Calibration', 'scan'),
        intent = config.get('Calibration', 'intent'),
        outfile = outfile,
        overwrite = config.getboolean('Calibration', 'overwrite')
        )

def write_default_config():   
    # Writing out configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    casalog.post('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    #cleans CASA arguments
    parser.add_argument("-c")
    parser.add_argument("--logfile")
        
    parser.add_argument("--config", help="Configuration file for the spectral-line data reduction pipeline")
    parser.add_argument("--infile", help="Observation measurement set")
    parser.add_argument("--outfile", help="Intermidiate output measurement set")    

    args = parser.parse_args()

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

    if not args.infile:
        casalog.post('Infile must to be provided. Use --infile.', priority="SEVERE")

    FASTcal(infile=args.infile, outfile=args.outfile)

if __name__ == "__main__":
    main()