"""Common utility routines used by the FAST pipeline modules"""

import ConfigParser
import os
import sys

# ConfigParser enhancements to get list of objects

def _list(s):
    return filter(None, map(lambda x: x.strip(), s.strip(' []').split(',')))

def _intlist(s):
    return map(int, _list(s))

def _floatlist(s):
    return map(float, _list(s))

class ListAwareMixIn(object):

    def getlist(self, section, option):
        return self._get(section, _list, option)

    def getintlist(self, section, option):
        return self._get(section, _intlist, option)

    def getfloatlist(self, section, option):
        return self._get(section, _floatlist, option)

class RawConfigParser(ConfigParser.RawConfigParser, ListAwareMixIn): pass
class ConfigParser(ConfigParser.ConfigParser, ListAwareMixIn): pass
#class SafeConfigParser(ConfigParser.SafeConfigParser, ListAwareMixIn): pass

# Command-line cleanup for modules invoked via casa -c "file"
def cmdline_cleanup():
    for i, arg in enumerate(sys.argv):
        if arg == '-c':
            i = i + 2
            break
    return sys.argv[i:]

def check_ioargs(args, casalog, infiles=False):

    # infile and outfile are mandatory
    # if "infiles" is True then the argument is called "infiles" and should be
    # a comma-separated list of filenames
    if infiles and not args.infiles:
        casalog.post('Infiles must be provided. Use --infiles.', priority="SEVERE")
        sys.exit(1)
    elif not infiles and not args.infile:
        casalog.post('Infile must be provided. Use --.', priority="SEVERE")
        sys.exit(1)
    if not args.outfile:
        casalog.post('Outfile must to be provided. Use --outfile.', priority="SEVERE")
        sys.exit(1)

    # Input files should exist
    try:
        infiles = args.infiles.split(',')
    except AttributeError:
        infiles = [args.infile]

    for infile in infiles:
        if not os.path.exists(infile):
            casalog.post('Input data %s does not exist' % args.infile, priority="SEVERE")
            sys.exit(1)

    # Ensure the directory holding outfile exists
    outpath = os.path.dirname(args.outfile)
    if not os.path.isdir(outpath):
        os.makedirs(outpath)