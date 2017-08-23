#!/usr/bin/env python

import argparse
import os
import subprocess

import ConfigParser

CONFIG_DEFAULTS = {'host': 'localhost', 'port': '7777', 'timeout': '10'}

def read_from_ngas(config_file):

    config = ConfigParser.ConfigParser(CONFIG_DEFAULTS)
    config.read(os.path.expanduser(config_file))

    host = config.get('ngas', 'host')
    port = config.getint('ngas', 'port')
    timeout = config.getfloat('ngas', 'timeout')
    file_id = config.get('fetch', 'file_id')
    output_dir = config.get('fetch', 'output_dir')

    cmd = ['ngamsPClient', 'RETRIEVE', '-H', host, '-p', str(port),
            '-f', file_id, '-o', output_dir]
    try:
        subprocess.check_output(cmd, shell=False)
    except subprocess.CalledProcessError as e:
        print("Command '%s' returned with non-zero return code %d:\n%s" %
              (' '.join(cmd), e.returncode, e.output))

parser = argparse.ArgumentParser()
parser.add_argument('--logfile', help="The configuration file for this module")
args = parser.parse_args()
read_from_ngas(args.config_file)
