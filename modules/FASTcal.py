#!/usr/bin/env python
#####################################
#
# FAST-HI Calibration based on CASA-cookbook example
# Position-Switched data
#####################################
import time
import os

def FASTcal(infile):

    if os.path.isfile(infile) == False:
        print 'Error: %s does not exist' % (infile) 
        exit()
    
    datapath = os.path.dirname(infile)
    head, tail = os.path.splitext(infile)
    
    # output
    outfile = head + '.txt'
    
    # ASAP environment parameters (the ones that are in the .asaprc file).
    # These are in the Python dictionary sd.rcParams
    # You can see whats in it by typing:
    # sd.rcParams
    sd.rcParams['verbose'] = True
    sd.rcParams['scantable.storage'] = 'memory'
    
    ##########################
    #
    # Position-Switched data
    #
    ##########################
    startTime = time.time()
    startProc = time.clock()
    ##########################
    # List data
    ##########################
    # List the contents of the dataset
    # First reset parameter defaults (safe)
    default('sdlist')
    # You can see its inputs with
    # inp('sdlist')
    # or just
    # inp
    # now that the defaults('sdlist') set the
    # taskname='sdlist'
    
    # Set an output file in case we want to refer back to it
    sdlist()
    
    ##########################
    # Calibrate data
    ##########################
    # Use the sdcal task to calibrate the data. Set the defaults
    default('sdcal')
    # You can see the inputs with
    # inp
    # Set our infile (which would have been set from our run of
    # sdlist if we were not cautious and reset defaults).
    fluxunit = 'K'
    # Spectral axis in channels for now
    specunit = 'channel'
    # This is position-switched mode
    calmode = 'ps'
    # It is safest to not have scantable pre-average integrations within scans.
    average = True
    scanaverage = False
    # Overwrite the output
    overwrite = True
    # We do want sdcal to average up scans and polarization after
    # calibration however. The averaging of scans are weighted by
    # integration time and Tsys, and the averaging of polarization
    # by Tsys.
    timeaverage = False
    tweight = 'tintsys'
    polaverage = True
    pweight = 'tsys'
    # Do an atmospheric optical depth (attenuation) correction
    # Just a random value at this stage
    tau = 0.09
    # Select our scans and IFs
    scanlist = [20, 21, 22, 23]
    iflist = [0]
    # We do not require selection by field name (they are all
    # the same except for on and off)
    field = ''
    # Spectral smoothing using boxcar smoothing rather than the default
    # kernel='hanning'
    kernel = 'boxcar'
    # We will set the width of the kernel to 5 channels
    kwidth = 5
    # We wish to fit out a baseline from the spectrum
    # We will let ASAP use auto_poly_baseline mode
    # but tell it to drop the 500 edge channels from
    # the beginning and end of the spectrum.
    # A 2nd-order polynomial will suffice for this test.
    # You might try higher orders for fun.
    blmode = 'auto'
    blpoly = 2
    edge = [500]
    # We will not give it regions as an input mask
    # though you could, with something like
    # masklist=[[1000,3000],[5000,7000]]
    masklist = []
    # By default, we will not get plots in sdcal (but
    # can make them using sdplot).
    plotlevel = 0
    # But if you wish to see a final spectrum, set
    # plotlevel = 1
    # or even
    # plotlevel = 2
    # to see intermediate plots and baselining output.
    # Now we give the name for the output file
    outfile = head + '.calibrateded.ms'
    # We will write it out in measurement set format
    outform = 'ms'
    # You can look at the inputs with
    # inp
    # Before running, lets save the inputs in case we want
    # to come back and re-run the calibration.
    saveinputs('sdcal', 'sdcal.' + head + '.save')
    # These can be recovered by
    # execfile 'sdcal.infile.save'
    
    # Finallly calibrate
    sdcal()