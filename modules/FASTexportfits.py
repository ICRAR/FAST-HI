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
FAST-HI export an image as FITS module
"""

import os
import sys
import ConfigParser
import argparse
import casadef
import time

import utils

module_name = 'FASTexportfits'

#config file
CONFIG_DEFAULT_FILE="../conf/exportfits.conf"
config = ConfigParser.RawConfigParser()

config.add_section('ExportFITS')
config.set('ExportFITS', 'velocity', 'False') 
config.set('ExportFITS', 'optical', 'False') 
config.set('ExportFITS', 'bitpix', '-32') 
config.set('ExportFITS', 'minpix', '0') 
config.set('ExportFITS', 'maxpix', '-1') 
config.set('ExportFITS', 'overwrite', 'True') 
config.set('ExportFITS', 'dropstokes', 'False') 
config.set('ExportFITS', 'stokeslast', 'True') 
config.set('ExportFITS', 'history', 'False') 
config.set('ExportFITS', 'dropdeg', 'False') 
    
sd.rcParams['verbose'] = True
sd.rcParams['scantable.storage'] = 'memory'

def FASTexportfits(imagename, fitsimage):

    casalog.post('FITS export for %s' % imagename)

    exportfits(imagename  = imagename,
                 fitsimage  = fitsimage,
                 velocity   = config.getboolean('ExportFITS', 'velocity'), 
                 optical    = config.getboolean('ExportFITS', 'optical', 'False'),
                 bitpix     = config.getint('ExportFITS', 'bitpix'),
                 minpix     = config.getint('ExportFITS', 'minpix'),
                 maxpix     = config.getint('ExportFITS', 'maxpix'),
                 overwrite  = config.getboolean('ExportFITS', 'overwrite'), 
                 dropstokes = config.getboolean('ExportFITS', 'dropstokes'), 
                 stokeslast = config.getboolean('ExportFITS', 'stokeslast'), 
                 history    = config.getboolean('ExportFITS', 'history'), 
                 dropdeg    = config.getboolean('ExportFITS', 'dropdeg') 
                 )

def write_default_config():   
    # Writing out configuration file
    with open(CONFIG_DEFAULT_FILE, 'wb') as configfile:
        config.write(configfile)
    casalog.post('No configuration file found. Default configuration file has been created: ' + CONFIG_DEFAULT_FILE)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Configuration file")
    parser.add_argument("--imagename", help="Image measurement set")
    parser.add_argument("--fitsimage", help="Output FITS file")
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

    if not args.imagename:
        casalog.post('Infile must to be provided. Use --imagename.', priority="SEVERE")

    FASTexportfits(imagename=args.imagename, fitsimage=args.fitsimage)

if __name__ == "__main__":
    main()