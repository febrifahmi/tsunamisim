"""Simple for running tsunami inundation scenario in Purworejo, Indonesia, using ANUGA

Prepared by febri fahmi <febrifahmi.hakim@tum.de>, 2015, based on ANUGA examples scripts 
by Geoscience Australia
"""

#------------------------------------------------------------------------------
# Import necessary modules
#------------------------------------------------------------------------------
# standard module
import os
import time
import sys

# related important module
import anuga

# application specific import
import project         # project.py consists of definition of file names and so on

time00 = time.time()
#------------------------------------------------------------------------------
# Preparation of topographic data
# Convert ASC 2 DEM 2 PTS using source data and store result in source data
#------------------------------------------------------------------------------
# unzip .asc file from zip file
import zipfile as zf
path_to_data_dir = 'C:/anuga/thesis/pwrj_initcond/'
if project.verbose: print 'Reading ASC from fixed_topobathy.zip'
zf.ZipFile(path_to_data_dir+project.name_stem+'.zip').extract(project.name_stem+'.asc')
zf.ZipFile(path_to_data_dir+project.name_stem+'.zip').extract(project.name_stem+'.prj')

# building DEM from ASC data
anuga.asc2dem(project.name_stem+'.asc', use_cache=project.cache, verbose=project.verbose)

# create PTS file from onshore DEM
anuga.dem2pts(project.name_stem+'.dem', use_cache=project.cache, verbose=project.verbose)

#------------------------------------------------------------------------------
# Create the triangular mesh and domain based on overall clipping
# polygons with a tagged boundary and interior regions as defined
# in project.py
#------------------------------------------------------------------------------
domain = anuga.create_domain_from_regions(project.bounding_polygon,
											boundary_tags={'east': [0],
														'onshore': [1],
														'west': [2],
														'bottom_ocean': [3]},
											maximum_triangle_area=project.default_res,
											mesh_filename=project.meshname,
											interior_regions=project.interior_regions,
											use_cache=project.cache,
											verbose=project.verbose)
# Print some stats about mesh and domain
print 'Number of triangles = ', len(domain)
print 'The extent is ', domain.get_extent()
print domain.statistics()

#------------------------------------------------------------------------------
# Setup parameters of computational domain
#------------------------------------------------------------------------------
domain.set_name('pwrj_SA282_CF_' + project.scenario) # Name of sww file
domain.set_datadir('.') # Store sww output here
domain.set_minimum_storable_height(0.01) # Store only depth > 1cm
domain.set_flow_algorithm('DE0')

#------------------------------------------------------------------------------
# Setup initial condition
#------------------------------------------------------------------------------
tide = project.tide
domain.set_quantity('stage', tide)

# setting up fruction value for each interior polygons
import anuga.utilities.quantity_setting_functions
# assign constant manning roughness for each interior polygons
poly_fun_pairs = [[project.bounding_polygon, 0.000],
					[project.poly_extent1, 0.025],
					[project.poly_extent2, 0.031],
					[project.poly_extent3, 0.031],
					[project.poly_extent4, 0.030],
					[project.poly_extent5, 0.030],
					[project.poly_extent6, 0.030],
					[project.poly_extent7, 0.030],
					[project.poly_extent8, 0.060],
					[project.poly_extent9, 0.060],
					[project.poly_extent10, 0.037],
					[project.poly_extent11, 0.037],
					[project.poly_extent0, 0.037],
					[project.poly_extent_river, 0.000],
					[project.poly_extent_river1, 0.000],
					[project.poly_extent_river2, 0.000]]

composite_f = anuga.utilities.quantity_setting_functions.composite_quantity_setting_function(poly_fun_pairs, 
                                        domain,
                                        clip_range = None,
                                        nan_treatment = 'fall_through',
                                        nan_interpolation_region_polygon = None,
                                        default_k_nearest_neighbours = 1,
                                        default_raster_interpolation = 'pixel',
                                        verbose=True)

domain.set_quantity('friction', composite_f)
#
#domain.set_quantity('friction', 0.03)

domain.set_quantity('elevation',
					filename=project.name_stem + '.pts',
					use_cache=project.cache,
					verbose=project.verbose,
					alpha=0.1)

time01 = time.time()
print 'That took %.2f seconds to fit data' %(time01-time00)

if project.just_fitting:
	import sys
	sys.exit()

#------------------------------------------------------------------------------
# Setup information for slide scenario
#------------------------------------------------------------------------------
if project.scenario == 'slide':
	# Function for submarine slide
	tsunami_source = anuga.slide_tsunami(length=35000.0,
										depth=project.slide_depth,
										slope=6.0,
										thickness=500.0,
										x0=project.slide_origin[0],
										y0=project.slide_origin[1],
										alpha=0.0,
										domain=domain,
										verbose=project.verbose)

#------------------------------------------------------------------------------
# Setup boundary condition
#------------------------------------------------------------------------------
print 'Available boundary tags', domain.get_boundary_tags()

# Prepare time series file for introducing wave profile into the model
import anuga.file_conversion.file_conversion
# read the time series text file and convert it to netcdf .tms format
tmsfile = 'tmsfile_SA282_CF.txt'
print 'Converting time series file '+tmsfile+' to NetCDF TMS file format'
file_text = path_to_data_dir+tmsfile
anuga.file_conversion.file_conversion.timefile2netcdf(file_text, file_out='tmsfile_SA282_CF.tms', quantity_names=None,
                                time_as_seconds=True)
TS_file = 'tmsfile_SA282_CF.tms'
print 'TMS file '+TS_file+' created'
# --------

Bd = anuga.Dirichlet_boundary([tide, 0, 0]) # Mean water level
Bs = anuga.Transmissive_stage_zero_momentum_boundary(domain) # Neutral boundary

if project.scenario == 'fixed_wave':
	# Huge 17.135m wave starting after 60 seconds and lasting 60 minutes.
	Bw = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(
																		domain=domain,
																		function=lambda t: [(60<t<3660)*17.135, 0, 0])
	# Option 2: Set boundary stage from predefined TMS file output from EasyWave
	wave_f = anuga.file_function(TS_file,
							domain,
							quantities='Attribute0')
	Btms = anuga.Transmissive_momentum_set_stage_boundary(domain=domain,
								function=lambda t: [wave_f(t), 0, 0])
	# Bt used if transmissive boundary raise too small timestep exception
	Bt = anuga.Time_boundary(domain=domain,
							function=lambda t: [wave_f(t), 0, 0])

	domain.set_boundary({'onshore': Bd,
						'west': Bs,
						'bottom_ocean': Btms,
						'east': Bs})

if project.scenario == 'slide':
	# Boundary conditions for slide scenario
	domain.set_boundary({'bottom_ocean': Bw,
							'west': Bs,
							'onshore': Bd,
							'east': Bs})

#------------------------------------------------------------------------------
# Evolve system through time
#------------------------------------------------------------------------------
import time
t0 = time.time()

from numpy import allclose

# slide tsunami
if project.scenario == 'slide':
	# Initial run without any event
	for t in domain.evolve(yieldstep=10, finaltime=60):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')
	# Add slide to water surface
	if allclose(t, 60):
		domain.add_quantity('stage', tsunami_source)
	# Continue propagating wave
	for t in domain.evolve(yieldstep=10, finaltime=5000,
		skip_initial_step=True):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')

# fixed wave
if project.scenario == 'fixed_wave':
	# Save every two mins leading up to wave approaching land
	for t in domain.evolve(yieldstep=0.5*60, finaltime=600):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')
	# Save every 30 secs as wave starts inundating ashore
	for t in domain.evolve(yieldstep=60*0.5, finaltime=7200,
		skip_initial_step=True):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')
print 'That took %.2f seconds' %(time.time()-t0)