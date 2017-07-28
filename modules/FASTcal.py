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

module_name = 'FASTcal'
log_name = module_name+'.log'


log = logging.getLogger(log_name)


#config file
CONFIG_DEFAULT_FILE="calibr.cfg"
config = ConfigParser.RawConfigParser()

def FASTcal(infile):

    log.info('FASTcal(Calibrating observations file: %s)', infile)

    sd.rcParams['verbose'] = True
    sd.rcParams['scantable.storage'] = 'memory'

    #initialise
    default('sdlistold')
    default('sdcal')

    infile = os.path.normpath(infile)
    datapath = os.path.dirname(infile)
    head, tail = os.path.splitext(os.path.basename(infile))
    
    outpath = config.get('Calibration', 'out_path')
    if os.path.isdir(outpath) == False:
        os.system('md ' + outpath)
    
    outfile = os.path.join(outpath, head + config.get('Calibration', 'outfile_ext'))
        #remove if one already exists
    if os.path.isfile(outfile) == True:
        os.system('rm -rf ' + outfile)

    listfile = os.path.join(outpath, head +'.listobs')
        #remove if one already exists
    if os.path.isfile(listfile) == True:
        os.system('rm -rf ' + listfile)
    # List the contents of the dataset
    listobs(vis=infile, listfile=listfile)

    ##########################
    # Calibrate data
    ##########################

    # These can be recovered by
    # execfile 'sdcal.infile.save'
    #saveinputs('sdcal', 'sdcal.' + head + '.save')

    # Finallly calibrate
    sdcal(infile=infile,
        #fluxunit = config.get('Calibration', 'fluxunit'),
        #specunit = config.get('Calibration', 'specunit'),
        #timeaverage = config.getboolean('Calibration', 'timeaverage'),
        #polaverage = config.getboolean('Calibration', 'polaverage'),
        #tau = config.getfloat('Calibration', 'tau'),
        calmode = config.get('Calibration', 'calmode'),
        #average = config.getboolean('Calibration', 'average'),
        #scanaverage = config.getboolean('Calibration', 'scanaverage'),

        # Overwrite the output
        overwrite = True,
        #plotlevel = 0,

        # We wish to fit out a baseline from the spectrum
        # We will let ASAP use auto_poly_baseline mode
        # but tell it to drop the 500 edge channels from
        # the beginning and end of the spectrum.
        # A 2nd-order polynomial will suffice for this test.
        # You might try higher orders for fun.
        #blmode = 'auto',
        #blpoly = 2,
        #edge = [500],

        # We will not give it regions as an input mask
        # though you could, with something like
        # masklist=[[1000,3000],[5000,7000]]
        #masklist = [],

        # Select our scans and IFs
        # scanlist = [20, 21, 22, 23],
        # iflist = [0],
        #scan = '0',
        #spw = '0',

        # Now we give the name for the output file
        outfile = outfile,

        # We will write it out in measurement set format
        #outform = config.get('Calibration', 'out_format')
    )

def write_default_config():
    config.add_section('Calibration')
    config.set('Calibration', 'fluxunit', 'K')
    config.set('Calibration', 'specunit', 'channel')
    config.set('Calibration', 'timeaverage', 'False')
    config.set('Calibration', 'polaverage', 'True')
    config.set('Calibration', 'tau', '0.09')
    config.set('Calibration', 'calmode', 'otfraster')
    config.set('Calibration', 'average', 'True')
    config.set('Calibration', 'scanaverage', 'True')
    config.set('Calibration', 'overwrite', 'True')
    config.set('Calibration', 'plotlevel', '0')
    config.set('Calibration', 'outfile_ext', '.calibrated.ms')
    config.set('Calibration', 'out_path', '')
    config.set('Calibration', 'out_format', 'MS2')

    # Writing our configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    log.info('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    #do not add '-c' as CASA doesn't remove its own -c from the command line
    parser.add_argument("--config", help="Configuration file for the spectral-line data reduction pipeline")
    parser.add_argument("--infile", help="Uncalibrated observation data")
    args = parser.parse_args()

    if not args.infile:
        parser.error('Infile must to be provided. Use -i or --infile.')
    elif not os.path.exists(args.infile):
        parser.error('%s does not exist' % args.infile)

    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    log.info('---Starting logger for ' + module_name)
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

    FASTcal(infile=args.infile)

if __name__ == "__main__":
    main()