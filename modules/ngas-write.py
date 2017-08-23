#!/usr/bin/env python

import argparse
import os
import subprocess

import ConfigParser

CONFIG_DEFAULTS = {'host': 'localhost', 'port': '7777', 'timeout': '10'}

def write_to_ngas(config_file):

    config = ConfigParser.ConfigParser(CONFIG_DEFAULTS)
    config.read(os.path.expanduser(config_file))

    host = config.get('ngas', 'host')
    port = config.getint('ngas', 'port')
    timeout = config.getfloat('ngas', 'timeout')
    fname = config.get('archive', 'filename')

    cmd = ['ngamsPClient', 'ARCHIVE', '-H', host, '-p', str(port),
            '--file-uri', fname]
    try:
        subprocess.check_output(cmd, shell=False)
    except subprocess.CalledProcessError as e:
        print("Command '%s' returned with non-zero return code %d:\n%s" %
              (' '.join(cmd), e.returncode, e.output))

parser = argparse.ArgumentParser()
parser.add_argument('--config', help="The configuration file for this module")
args = parser.parse_args()
write_to_ngas(args.config_file)
