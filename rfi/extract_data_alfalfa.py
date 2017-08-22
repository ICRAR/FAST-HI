# -*- coding: utf-8 -*-
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
Extract the data into the format required for machine learning
"""
import argparse
from os.path import basename, exists, isdir, join

import casadef
import numpy as np

module_name = 'extract_data'


def extract_data(output_directory, arguments):
    for measurement_set in arguments:
        if exists(measurement_set) and isdir(measurement_set):
            casalog.post('Processing {0}'.format(measurement_set))

            tb.open(measurement_set)

            float_data = tb.getcol('FLOAT_DATA')
            time = tb.getcol('TIME')
            time = np.sort(np.unique(time))

            # Polarisation, Channels, beams, timesteps
            data = float_data.reshape(2, 4096, 8, 600)

            # Reorder to: Polarisation, beams, channels, timesteps
            data = np.transpose(data, (0, 2, 1, 3))
            tb.close()

            measurement_set_name = basename(measurement_set)
            output_name = join(output_directory, '{0}.npz'.format(measurement_set_name))

            count = 1
            while exists(output_name):
                output_name = join(output_directory, '{0}.{1:02d}.npz'.format(measurement_set_name, count))
                count += 1

            np.savez_compressed(output_name, data=data, time=time)


def main():
    parser = argparse.ArgumentParser()
    # cleans CASA arguments
    parser.add_argument('--nologger', action="store_true")
    parser.add_argument('--log2term', action="store_true")
    parser.add_argument('--logfile')
    parser.add_argument('-c', '--call')
    parser.add_argument('output_directory', help='where to store the data')
    parser.add_argument('arguments', nargs='+', help='the measurement sets to process')

    args = parser.parse_args()

    casalog.post('---Logging for ' + module_name)
    casalog.post('Command line:'+str(args))
    casalog.post('CASA version: ' + casadef.casa_version)

    extract_data(args.output_directory, args.arguments)


if __name__ == "__main__":
    main()
