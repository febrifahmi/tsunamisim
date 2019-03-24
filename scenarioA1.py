"""Simple for running tsunami inundation scenario in Purworejo, Indonesia, using ANUGA

Prepared by febri fahmi <febrifahmi.hakim@tum.de>, 2015, based on ANUGA examples scripts.
(c) Geoscience Australia
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
path_to_data_dir = 'C:/anuga/thesis/pwrj_initcond/'
if project.verbose: print 'Reading DEM data from pwrj.dem'

# create PTS file from onshore DEM
anuga.dem2pts(path_to_data_dir+project.name_stem+'.dem', use_cache=project.cache, verbose=project.verbose)

#------------------------------------------------------------------------------
# Create the triangular mesh and domain based on overall clipping
# polygons with a tagged boundary and interior regions as defined
# in project.py
#------------------------------------------------------------------------------
domain = anuga.create_domain_from_regions(project.bounding_polygon,
											boundary_tags={'onshore': [0],
														'east': [1],
														'bottom_ocean': [2],
														'west': [3]},
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
domain.set_name('pwrj_' + project.scenario) # Name of sww file
domain.set_datadir('.') # Store sww output here
domain.set_minimum_storable_height(0.01) # Store only depth > 1cm
domain.set_flow_algorithm('DE0')

#------------------------------------------------------------------------------
# Setup initial condition
#------------------------------------------------------------------------------
tide = project.tide
domain.set_quantity('stage', tide)
domain.set_quantity('friction', 0.0 )

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

Bd = anuga.Dirichlet_boundary([tide, 0, 0]) # Mean water level
Bs = anuga.Transmissive_stage_zero_momentum_boundary(domain) # Neutral boundary

if project.scenario == 'fixed_wave':
	# Huge 10m wave starting after 60 seconds and lasting 1 hour.
	Bw = anuga.Transmissive_n_momentum_zero_t_momentum_set_stage_boundary(
																		domain=domain,
																		function=lambda t: [(60<t<3660)*10.94, 0, 0])

	domain.set_boundary({'east': Bs,
						'bottom_ocean': Bw,
						'west': Bs,
						'onshore': Bd})

if project.scenario == 'slide':
	# Boundary conditions for slide scenario
	domain.set_boundary({'east': Bs,
							'bottom_ocean': Bw,
							'west': Bs,
							'onshore': Bd})

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
	for t in domain.evolve(yieldstep=2*60, finaltime=5000):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')
	# Save every 30 secs as wave starts inundating ashore
	for t in domain.evolve(yieldstep=60*0.5, finaltime=10000,
		skip_initial_step=True):
		print domain.timestepping_statistics()
		print domain.boundary_statistics(tags='bottom_ocean')
print 'That took %.2f seconds' %(time.time()-t0)