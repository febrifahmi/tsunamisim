"""Script used for exporting thesimulation results
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
#scenario = 'slide'
name = 'pwrj_' + scenario

print 'output dir:', name

"""
Produce .tif files extracting results of pwrj simulation.

Can be viewed with qgis
"""
    
from anuga.utilities.plot_utils import Make_Geotif
Make_Geotif(swwFile=name+'.sww', 
             output_quantities=['stage', 'depth', 'velocity', 'elevation'],
             myTimeStep='max', CellSize=100.0, 
             lower_left=None, upper_right=None,
             EPSG_CODE=32355, 
             proj4string=None,
             velocity_extrapolation=True,
             min_allowed_height=1.0e-05,
             output_dir='.',
             bounding_polygon=project.bounding_polygon,
             verbose=True)

Make_Geotif(swwFile=name+'.sww', 
             output_quantities=['stage'],
             myTimeStep=[0],
             CellSize=100.0, 
             lower_left=None, upper_right=None,
             EPSG_CODE=32355, 
             proj4string=None,
             velocity_extrapolation=True,
             min_allowed_height=1.0e-05,
             output_dir='.',
             bounding_polygon=project.bounding_polygon,
             verbose=True)
