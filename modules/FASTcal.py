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
import logging
import ConfigParser
import argparse
import casadef
import time

module_name = 'FASTcal'
log_name = time.strftime("%Y%m%d-%H%M%S-") + module_name+'.log'
log = logging.getLogger(log_name)

#config file
CONFIG_DEFAULT_FILE="calibr.cfg"
config = ConfigParser.RawConfigParser()

def FASTcal(infile):

    log.info('FASTcal(Calibrating observations file: %s)', infile)

    sd.rcParams['verbose'] = True
    sd.rcParams['scantable.storage'] = 'memory'

    #initialise
    #default('sdlistold')
    default('sdcal')

    infile = os.path.normpath(infile)
    datapath = os.path.dirname(infile)
    head, tail = os.path.splitext(os.path.basename(infile))
    
    outpath = config.get('Calibration', 'out_path')
    if os.path.isdir(outpath) == False:
        os.system('mkdir ' + outpath)
    
    outfile = os.path.join(outpath, head + config.get('Calibration', 'outfile_ext'))

    listfile = os.path.join(outpath, head +'.listobs')
        #remove if one already exists
    if os.path.isfile(listfile) == True:
        os.system('rm -rf ' + listfile)
    # List the contents of the dataset
    listobs(vis=infile, listfile=listfile)

    ##########################
    # Calibrate data
    ##########################
    sdcal(infile=infile,
        calmode = config.get('Calibration', 'calmode'),
        overwrite = config.getboolean('Calibration', 'overwrite'),
        fraction = config.get('Calibration', 'fraction'),
        noff = config.getint('Calibration', 'noff'),
        width = config.getfloat('Calibration', 'width'),
        elongated = config.getboolean('Calibration', 'elongated'),
        applytable = config.get('Calibration', 'applytable'),
        interp = config.get('Calibration', 'interp'),
        field = config.get('Calibration', 'field'),
        spw = config.get('Calibration', 'spw'),
        scan = config.get('Calibration', 'scan'),
        intent = config.get('Calibration', 'intent'),
        outfile = outfile,
        )

def write_default_config():
    config.add_section('Calibration')
    config.set('Calibration', 'calmode', 'otfraster') 
    config.set('Calibration', 'fraction', '10%')
    config.set('Calibration', 'noff', '-1')
    config.set('Calibration', 'width', '0.5')
    config.set('Calibration', 'elongated', 'False')
    config.set('Calibration', 'applytable', '')
    config.set('Calibration', 'interp', '')
    config.set('Calibration', 'overwrite', 'True')
    config.set('Calibration', 'field', '')
    config.set('Calibration', 'spw', '')
    config.set('Calibration', 'scan', '')
    config.set('Calibration', 'intent', 'OBSERVE_TARGET#ON_SOURCE')
    config.set('Calibration', 'outfile_ext', '.calibrated.ms')
    config.set('Calibration', 'out_path', 'output')
    config.set('Calibration', 'out_format', 'MS2')

    # Writing our configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    log.info('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    #removes '-c' leftover CASA argument
    parser.add_argument("-c")
    
    parser.add_argument("--config", help="Configuration file for the spectral-line data reduction pipeline")
    parser.add_argument("--infile", help="Uncalibrated observation data")
    args = parser.parse_args()

    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    log.info('\n---Starting logger for ' + module_name)
    log.info(args)
    log.info('CASA version: ' + casadef.casa_version)

    config_file = CONFIG_DEFAULT_FILE
    if args.config:
        if os.path.isfile(args.config):
            config_file=args.config
        else:
            log.exception('Configuration ' + args.config + ' does not exist.') 
            sys.exit()
    else:
        if not os.path.isfile(config_file):
            write_default_config()
            log.info('Check configuration and re-run the module.')
            sys.exit()

    # read configuration file
    log.info('Using configuration from %s', config_file)
    config.read(config_file)

    if not args.infile:
        parser.error('Infile must to be provided. Use --infile.')
    elif not os.path.exists(args.infile):
        parser.error('%s does not exist' % args.infile)

    FASTcal(infile=args.infile)

if __name__ == "__main__":
    main()