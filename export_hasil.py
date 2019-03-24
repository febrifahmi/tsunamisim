"""Script used for exporting the simulation results
based on cairns example
"""
#---------------------------------------------------------------------------
# Import necessary modules
#---------------------------------------------------------------------------
import os
import sys
import project

# important module
import anuga

scenario = 'fixed_wave'
name = 'pwrj_SA282_CF_' + scenario

print 'output dir:', name
which_var = 2

if which_var == 0:    # Stage
    outname = name + '_stage'
    quantityname = 'stage'

if which_var == 1:    # Absolute Momentum
    outname = name + '_momentum'
    quantityname = '(xmomentum**2 + ymomentum**2)**0.5'    #Absolute momentum

if which_var == 2:    # Depth
    outname = name + '_depth'
    quantityname = 'stage-elevation'  #Depth

if which_var == 3:    # Speed
    outname = name + '_speed'
    quantityname = '(xmomentum**2 + ymomentum**2)**0.5/(stage-elevation+1.e-3)'  #Speed

if which_var == 4:    # Elevation
    outname = name + '_elevation'
    quantityname = 'elevation'  #Elevation

print 'start sww2dem'

anuga.sww2dem(name+'.sww',
        outname+'.asc',
        quantity=quantityname,
        cellsize=10,      
        #easting_min=project.eastingmin,
        #easting_max=project.eastingmax,
        #northing_min=project.northingmin,
        #northing_max=project.northingmax,        
        reduction=max, 
        verbose=True)
# klo error spt dibawah ini
"""Traceback (most recent call last):
  File "../export_hasil.py", line 51, in <module>
    verbose=True)
  File "C:\Python27\lib\site-packages"\/anuga\/file_conversion\sww2dem.py", line 18
2, in sww2dem
    log.critical('    Start time: .....fid.starttime[0])
IndexError: invalid index to scalar variable.
"""
# remove [0] di sww2dem.py, trus coba lagi, trus klo udah balikin lagi ke semula pake [0]