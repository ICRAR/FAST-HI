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
import ConfigParser
import argparse
import casadef
import time

import utils

module_name = 'FASTflagger'

# config file
CONFIG_DEFAULT_FILE = "../conf/flagger.conf"
config = utils.RawConfigParser()

config.add_section('Common')
config.set('Common', 'in_path', '')
config.set('Common', 'out_path', '')

config.add_section('Flagging')
config.set('Flagging', 'outfile_ext', 'ms.flagging')
config.set('Flagging', 'overwrite', 'False')
config.set('Flagging', 'mode', 'manual')
config.set('Flagging', 'autocorr', 'False')
config.set('Flagging', 'inpfile', '')
config.set('Flagging', 'reason', 'any')
config.set('Flagging', 'tbuff', '0.0')
config.set('Flagging', 'spw', '')
config.set('Flagging', 'field', '')
config.set('Flagging', 'antenna', '')
config.set('Flagging', 'uvrange', '')
config.set('Flagging', 'timerange', '')
config.set('Flagging', 'correlation', '')
config.set('Flagging', 'scan', '')
config.set('Flagging', 'intent', '')
config.set('Flagging', 'array', '')
config.set('Flagging', 'observation', '')
config.set('Flagging', 'feed', '')
config.set('Flagging', 'clipminmax', '')
config.set('Flagging', 'datacolumn', 'DATA')
config.set('Flagging', 'clipoutside', 'True')
config.set('Flagging', 'channelavg', 'False')
config.set('Flagging', 'chanbin', '1')
config.set('Flagging', 'timeavg', 'False')
config.set('Flagging', 'timebin', '0')
config.set('Flagging', 'clipzeros', 'False')
config.set('Flagging', 'quackinterval', '1.0')
config.set('Flagging', 'quackmode', 'beg')
config.set('Flagging', 'quackincrement', 'False')
config.set('Flagging', 'tolerance', '0.0')
config.set('Flagging', 'addantenna', '')
config.set('Flagging', 'lowerlimit', '0.0')
config.set('Flagging', 'upperlimit', '90.0')
config.set('Flagging', 'ntime', 'scan')
config.set('Flagging', 'combinescans', 'False')
config.set('Flagging', 'timecutoff', '4.0')
config.set('Flagging', 'freqcutoff', '3.0')
config.set('Flagging', 'timefit', 'line')
config.set('Flagging', 'freqfit', 'poly')
config.set('Flagging', 'maxnpieces', '7')
config.set('Flagging', 'flagdimension', 'freqtime')
config.set('Flagging', 'usewindowstats', 'none')
config.set('Flagging', 'halfwin', '1')
config.set('Flagging', 'extendflags', 'True')
config.set('Flagging', 'winsize', '3')
config.set('Flagging', 'timedev', '')
config.set('Flagging', 'freqdev', '')
config.set('Flagging', 'timedevscale', '5.0')
config.set('Flagging', 'freqdevscale', '5.0')
config.set('Flagging', 'spectralmax', '1e6')
config.set('Flagging', 'spectralmin', '0.0')
config.set('Flagging', 'antint_ref_antenna', '')
config.set('Flagging', 'minchanfrac', '0.6')
config.set('Flagging', 'verbose', 'False')
config.set('Flagging', 'extendpols', 'True')
config.set('Flagging', 'growtime', '50.0')
config.set('Flagging', 'growfreq', '50.0')
config.set('Flagging', 'growaround', 'False')
config.set('Flagging', 'flagneartime', 'False')
config.set('Flagging', 'flagnearfreq', 'False')
config.set('Flagging', 'minrel', '0.0')
config.set('Flagging', 'maxrel', '1.0')
config.set('Flagging', 'minabs', '0')
config.set('Flagging', 'maxabs', '-1')
config.set('Flagging', 'spwchan', 'False')
config.set('Flagging', 'spwcorr', 'False')
config.set('Flagging', 'basecnt', 'False')
config.set('Flagging', 'fieldcnt', 'False')
config.set('Flagging', 'name', 'Summary')
config.set('Flagging', 'action', 'apply')
config.set('Flagging', 'display', '')
config.set('Flagging', 'flagbackup', 'True')
config.set('Flagging', 'savepars', 'False')
config.set('Flagging', 'cmdreason', '')
    
sd.rcParams['verbose'] = True
sd.rcParams['scantable.storage'] = 'memory'

def FASTflagger(infile):

    infile = os.path.normpath(os.path.join(config.get('Common', 'in_path'), infile))
    if not os.path.exists(infile):
        casalog.post('%s does not exist' % infile, priority="SEVERE")
        sys.exit()

    casalog.post('Flagging for %s' % infile)
    # List the contents of the dataset
    listobs(vis=infile)

    head, tail = os.path.splitext(os.path.basename(infile))

    outpath = config.get('Common', 'out_path')
    if os.path.isdir(outpath) == False:
        os.system('mkdir ' + outpath)

    ##########################
    # Flag data
    ##########################
    flagdata(
        vis=infile,
        outfile=os.path.join(outpath, head + config.get('Flagging', 'outfile_ext')),
        overwrite=config.getboolean('Flagging', 'overwrite'),
        mode=config.get('Flagging', 'mode'),
        autocorr=config.getboolean('Flagging', 'autocorr'),
        inpfile=config.get('Flagging', 'inpfile'),
        reason=config.get('Flagging', 'reason'),
        tbuff=config.getfloat('Flagging', 'tbuff'),
        spw=config.get('Flagging', 'spw'),
        field=config.get('Flagging', 'field'),
        antenna=config.get('Flagging', 'antenna'),
        uvrange=config.get('Flagging', 'uvrange'),
        timerange=config.get('Flagging', 'timerange'),
        correlation=config.get('Flagging', 'correlation'),
        scan=config.get('Flagging', 'scan'),
        intent=config.get('Flagging', 'intent'),
        array=config.get('Flagging', 'array'),
        observation=config.get('Flagging', 'observation'),
        feed=config.get('Flagging', 'feed'),
#        clipminmax=config.getfloatlist('Flagging', 'clipminmax'),
        datacolumn=config.get('Flagging', 'datacolumn'),
        clipoutside=config.getboolean('Flagging', 'clipoutside'),
        channelavg=config.getboolean('Flagging', 'channelavg'),
        chanbin=config.getint('Flagging', 'chanbin'),
        timeavg=config.getboolean('Flagging', 'timeavg'),
        timebin=config.get('Flagging', 'timebin'),
        clipzeros=config.getboolean('Flagging', 'clipzeros'),
        quackinterval=config.getfloat('Flagging', 'quackinterval'),
        quackmode=config.get('Flagging', 'quackmode'),
        quackincrement=config.getboolean('Flagging', 'quackincrement'),
        tolerance=config.getfloat('Flagging', 'tolerance'),
        addantenna=config.get('Flagging', 'addantenna'),
        lowerlimit=config.getfloat('Flagging', 'lowerlimit'),
        upperlimit=config.getfloat('Flagging', 'upperlimit'),
        ntime=config.get('Flagging', 'ntime'),
        combinescans=config.getboolean('Flagging', 'combinescans'),
        timecutoff=config.getfloat('Flagging', 'timecutoff'),
        freqcutoff=config.getfloat('Flagging', 'freqcutoff'),
        timefit=config.get('Flagging', 'timefit'),
        freqfit=config.get('Flagging', 'freqfit'),
        maxnpieces=config.getint('Flagging', 'maxnpieces'),
        flagdimension=config.get('Flagging', 'flagdimension'),
        usewindowstats=config.get('Flagging', 'usewindowstats'),
        halfwin=config.getint('Flagging', 'halfwin'),
        extendflags=config.getboolean('Flagging', 'extendflags'),
        winsize=config.getint('Flagging', 'winsize'),
        timedev=config.get('Flagging', 'timedev'),
        freqdev=config.get('Flagging', 'freqdev'),
        timedevscale=config.getfloat('Flagging', 'timedevscale'),
        freqdevscale=config.getfloat('Flagging', 'freqdevscale'),
        spectralmax=config.getfloat('Flagging', 'spectralmax'),
        spectralmin=config.getfloat('Flagging', 'spectralmin'),
        antint_ref_antenna=config.get('Flagging', 'antint_ref_antenna'),
        minchanfrac=config.getfloat('Flagging', 'minchanfrac'),
        verbose=config.getboolean('Flagging', 'verbose'),
        extendpols=config.getboolean('Flagging', 'extendpols'),
        growtime=config.getfloat('Flagging', 'growtime'),
        growfreq=config.getfloat('Flagging', 'growfreq'),
        growaround=config.getboolean('Flagging', 'growaround'),
        flagneartime=config.getboolean('Flagging', 'flagneartime'),
        flagnearfreq=config.getboolean('Flagging', 'flagnearfreq'),
        minrel=config.getfloat('Flagging', 'minrel'),
        maxrel=config.getfloat('Flagging', 'maxrel'),
        minabs=config.getint('Flagging', 'minabs'),
        maxabs=config.getint('Flagging', 'maxabs'),
        spwchan=config.getboolean('Flagging', 'spwchan'),
        spwcorr=config.getboolean('Flagging', 'spwcorr'),
        basecnt=config.getboolean('Flagging', 'basecnt'),
        fieldcnt=config.getboolean('Flagging', 'fieldcnt'),
        name=config.get('Flagging', 'name'),
        action=config.get('Flagging', 'action'),
        display=config.get('Flagging', 'display'),
        flagbackup=config.getboolean('Flagging', 'flagbackup'),
        savepars=config.getboolean('Flagging', 'savepars'),
        cmdreason=config.get('Flagging', 'cmdreason')
    )

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
            config_file = args.config
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
        casalog.post('File with a list of measurementsets must to be provided. Use --infile.', priority="SEVERE")

    FASTflagger(infile=args.infile)

if __name__ == "__main__":
    main()
