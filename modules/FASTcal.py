#####################################
#
# Calibration based on CASA-cookbook example "ORION-S SDtasks Use Case"
# Position-Switched data
# Version TT 2008-10-14 (updated)
# Version STM 2007-03-04
#
# This is a detailed walk-through
# for using the SDtasks on a
# test dataset.
#
#####################################
import time
import os
# NOTE: you should have already run
# asap_init()
# to import the ASAP tools as sd.<tool>
# and the SDtasks
#
# This is the environment variable
# pointing to the head of the CASA
# tree that you are running
casapath=os.environ['AIPSPATH']
#
# This bit removes old versions of the output files
os.system('rm -rf sdusecase_orions* ')
#
# This is the path to the OrionS GBT ms in the data repository
datapath=casapath+'/data/regression/ATST5/OrionS/OrionS_rawACSmod'
#
# The following will remove old versions of the data and
# copy the data from the repository to your
# current directory. Comment this out if you already have it
# and don't want to recopy
os.system('rm -rf OrionS_rawACSmod')
copystring='cp -r '+datapath+' .'
os.system(copystring)
# Now is the time to set some of the more useful
# ASAP environment parameters (the ones that the
# ASAP User Manual claims are in the .asaprc file).
# These are in the Python dictionary sd.rcParams
# You can see whats in it by typing:
#sd.rcParams
# One of them is the 'verbose' parameter which tells
# ASAP whether to spew lots of verbiage during processing
# or to keep quiet. The default is
#sd.rcParams['verbose']=True
# You can make ASAP run quietly (with only task output) with
#sd.rcParams['verbose']=False
# Another key one is to tell ASAP to save memory by
# going off the disk instead. The default is
#sd.rcParams['scantable.storage']='memory'
# but if you are on a machine with small memory, do
#sd.rcParams['scantable.storage']='disk'
# You can reset back to defaults with
#sd.rcdefaults
##########################
#
# ORION-S HC3N
# Position-Switched data
#
##########################
startTime=time.time()
startProc=time.clock()
##########################
# List data
##########################
# List the contents of the dataset
# First reset parameter defaults (safe)
default('sdlist')
# You can see its inputs with
#inp('sdlist')
# or just
#inp
# now that the defaults('sdlist') set the
# taskname='sdlist'
#
# Set the name of input file
infile = 'wapp.20100920.a2010.0024.fits'
# Set an output file in case we want to
# refer back to it
outfile = 'out.wapp.20100920.a2010.0024.txt'
sdlist()
# You could also just type
#go
# In the logger, you should see something like:
#
#--------------------------------------------------------------------------------
#Scan Table Summary
#--------------------------------------------------------------------------------
#Project: AGBT06A_018_01
#Obs Date: 2006/01/19/01:45:58
#Observer: Joseph McMullin
#Antenna Name: GBT@GREENBANK
#Data Records: 512 rows
#Obs. Type: OffOn:PSWITCHOFF:TPWCAL
#Beams: 1
#IFs: 8
#Polarisations: 2 (circular)
#Channels: 8192
#Flux Unit: K
#Abscissa: Channel
#Selection: none
#
#Scan Source Time range Int[s] Record SrcType FreqIDs MolIDs
# Beam Position (J2000)
#--------------------------------------------------------------------------------
# 20 OrionS 2006/01/19/01:45:58.0 - 01:47:58.2 30.03 64 [PSOFF, PSOFF:CALON] [0, # 0 05:15:13.5 -05.24.08.6
# 21 OrionS 2006/01/19/01:48:38.0 - 01:50:38.2 30.03 64 [PSON, PSON:CALON] [0, 1, # 0 05:35:13.4 -05.24.07.8
# 22 OrionS 2006/01/19/01:51:21.0 - 01:53:21.2 30.03 64 [PSOFF, PSOFF:CALON] [0, # 0 05:15:13.6 -05.24.08.5
# 23 OrionS 2006/01/19/01:54:01.0 - 01:56:01.2 30.03 64 [PSON, PSON:CALON] [0, 1, # 0 05:35:13.4 -05.24.08.1
# 24 OrionS 2006/01/19/02:01:47.0 - 02:03:47.2 30.03 64 [PSOFF, PSOFF:CALON] [4, # 0 05:15:13.5 -05.24.08.5
# 25 OrionS 2006/01/19/02:04:27.0 - 02:06:27.2 30.03 64 [PSON, PSON:CALON] [4, 5, # 0 05:35:13.4 -05.24.08.1
# 26 OrionS 2006/01/19/02:07:10.0 - 02:09:10.2 30.03 64 [PSOFF, PSOFF:CALON] [4, # 0 05:15:13.5 -05.24.08.4
# 27 OrionS 2006/01/19/02:09:51.0 - 02:11:51.2 30.03 64 [PSON, PSON:CALON] [4, 5, # 0 05:35:13.3 -05.24.08.1
#--------------------------------------------------------------------------------
#FREQUENCIES: 4
# ID IFNO Frame RefVal RefPix Increment Channels POLNOs
# 0 0 LSRK 4.5489351e+10 4095.5 6104.233 8192 [0, 1]
# 1 1 LSRK 4.5300782e+10 4095.5 6104.233 8192 [0, 1]
# 2 2 LSRK 4.4074926e+10 4095.5 6104.233 8192 [0, 1]
# 3 3 LSRK 4.4166212e+10 4095.5 6104.233 8192 [0, 1]
# 4 12 LSRK 4.3962123e+10 4095.5 6104.2336 8192 [0, 1]
# 5 13 LSRK 4.2645417e+10 4095.5 6104.2336 8192 [0, 1]
# 6 14 LSRK 4.1594977e+10 4095.5 6104.2336 8192 [0, 1]
# 7 15 LSRK 4.342282e+10 4095.5 6104.2336 8192 [0, 1]
#--------------------------------------------------------------------------------
#MOLECULES:
# ID RestFreq Name
# 0 [4.54903e+10] []
# 1 [4.3963e+10] []
#--------------------------------------------------------------------------------
# The HC3N and CH3OH lines are in IFs 0 and 2 respectively
# of scans 20,21,22,23. We will pull these out in our
# calibration.
##########################
# Calibrate data
##########################
# We will use the sdcal task to calibrate the data.
# Set the defaults
default('sdcal')
# You can see the inputs with
#inp
# Set our infile (which would have been set from our run of
# sdlist if we were not cautious and reset defaults).
infile = 'OrionS_rawACSmod'
fluxunit = 'K'
# Lets leave the spectral axis in channels for now
specunit = 'channel'
# This is position-switched data so we tell sdcal this
calmode = 'ps'
# For GBT data, it is safest to not have scantable pre-average
# integrations within scans.
average = True
scanaverage = False
# We do want sdcal to average up scans and polarization after
# calibration however. The averaging of scans are weighted by
# integration time and Tsys, and the averaging of polarization
# by Tsys.
timeaverage = True
tweight = 'tintsys'
polaverage = True
pweight = 'tsys'
# Do an atmospheric optical depth (attenuation) correction
# Input the zenith optical depth at 43 GHz
tau = 0.09
# Select our scans and IFs (for HC3N)
scanlist = [20,21,22,23]
iflist = [0]
# We do not require selection by field name (they are all
# the same except for on and off)
field = ''
# We will do some spectral smoothing
# For this demo we will use boxcar smoothing rather than
# the default
#kernel='hanning'
# We will set the width of the kernel to 5 channels
kernel = 'boxcar'
kwidth = 5
# We wish to fit out a baseline from the spectrum
# The GBT has particularly nasty baselines :(
# We will let ASAP use auto_poly_baseline mode
# but tell it to drop the 1000 edge channels from
# the beginning and end of the spectrum.
# A 2nd-order polynomial will suffice for this test.
# You might try higher orders for fun.
blmode = 'auto'
blpoly = 2
edge = [1000]
# We will not give it regions as an input mask
# though you could, with something like
#masklist=[[1000,3000],[5000,7000]]
masklist = []
# By default, we will not get plots in sdcal (but
# can make them using sdplot).
plotlevel = 0
# But if you wish to see a final spectrum, set
#plotlevel = 1
# or even
#plotlevel = 2
# to see intermediate plots and baselining output.
# Now we give the name for the output file
outfile = 'sdcal.wapp.20100920.a2010.0024.ms'
# We will write it out in ASAP scantable format
outform = 'ms'
# You can look at the inputs with
#inp
# Before running, lets save the inputs in case we want
# to come back and re-run the calibration.
saveinputs('sdcal','sdcal.orions.save')
# These can be recovered by
#execfile 'sdcal.orions.save'
# We are ready to calibrate
sdcal()

#See some result here

##########################
# List the contents of the calibrated dataset
# Set the input to the just created file
infile = outfile
outfile = ''
sdlist()

##########################
# Plot data
##########################
default('sdplot')
# The file we produced after calibration
# (if we hadn't reset defaults it would have
# been set - note that sdplot,sdfit,sdstat use
# infile as the input file, which is the output
# file of sdcal).
infile = 'sdcal.wapp.20100920.a2010.0024.ms'
# Lets just go ahead and plot it up as-is
specunit='GHz'
fluxunit='Jy'
telescopeparm=''
sdplot()
# Lets save this plot
outfile='sdcal.wapp.20100920.a2010.0024.eps'
sdplot()


##########################
# Off-line Statistics
##########################
# Now do some region statistics
# First the line-free region
# Set parameters
default('sdstat')
infile = 'sdcal.wapp.20100920.a2010.0024.ms'
# Keep the default spectrum and flux units
# K and channel
fluxunit = ''
specunit = ''
# Pick out a line-free region
# You can bring up a default sdplot again
# to check this
masklist = [[5000,7000]]
# This is a line-free region so we don't need
# to invert the mask
invertmask = False
# You can check with
#inp
# sdstat returns some results in
# the Python dictionary. You can assign
# this to a variable
off_stat=sdstat()
# and look at it
off_stat
# which should give
# {'eqw': 38.563105620704945,
# 'max': 0.15543246269226074,
# 'mean': -0.0030361821409314871,
# 'median': -0.0032975673675537109,
# 'min': -0.15754437446594238,
# 'rms': 0.047580458223819733,
# 'stddev': 0.047495327889919281,
# 'sum': -6.0754003524780273}
#You see it has some keywords for the various
#stats. We want the standard deviation about
#the mean, or 'stddev'
print "The off-line std. deviation = ",off_stat['stddev']
# which should give
# The off-line std. deviation = 0.0474953278899
# or better formatted (using Python I/O formatting)
print "The off-line std. deviation = %5.3f K" % (off_stat['stddev'])
# which should give
# The off-line std. deviation = 0.047 K
##########################
# On-line Statistics
##########################
# Now do the line region
# Continue setting or resetting parameters
masklist = [[3900,4200]]
line_stat = sdstat()
# look at these
line_stat
# which gives
# {'eqw': 73.335154614280981,
# 'max': 0.92909121513366699,
# 'mean': 0.22636228799819946,
# 'median': 0.10317134857177734,
# 'min': -0.13283586502075195,
# 'rms': 0.35585442185401917,
# 'stddev': 0.27503398060798645,
# 'sum': 68.135047912597656}
# of particular interest are the max value
print "The on-line maximum = %5.3f K" % (line_stat['max'])
# which gives
# The on-line maximum = 0.929 K
# and the estimated equivalent width (in channels)
# which is the sum/max
print "The estimated equivalent width = %5.1f channels" %\
(line_stat['eqw'])
# which gives
# The estimated equivalent width = 73.3 channels

#no line ftting in this example