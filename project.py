""" Common filenames and locations for topographic data, meshes and outputs.
This file defines the parameters of the scenario you wish to run.
Prepared by febri fahmi <febrifahmi.hakim@tum.de>, 2015, based on ANUGA examples scripts
by Geoscience Australia
"""
#------------------------------------------------------------------------------
# import anuga module
import anuga

#------------------------------------------------------------------------------
# Runtime parameters
#------------------------------------------------------------------------------
cache = False
verbose = True

#------------------------------------------------------------------------------
# Define scenario as either slide or fixed_wave. Choose one.
#------------------------------------------------------------------------------
scenario = 'fixed_wave' 		# Wave applied at the boundary
#scenario = 'slide' # Slide wave form applied inside the domain

#------------------------------------------------------------------------------
# Filenames
#------------------------------------------------------------------------------
name_stem = 'fixed_topobathy'
meshname = name_stem + '.msh'
# Filename for tide gauges locations
gauge_filename = 'gauges_.csv'

#------------------------------------------------------------------------------
# Domain definitions
#------------------------------------------------------------------------------
# bounding polygon for study area
bounding_polygon = anuga.read_polygon('study_area3.csv')
A = anuga.polygon_area(bounding_polygon) / 1000000.0
print 'Area of bounding polygon = %.2f km^2' % A

#------------------------------------------------------------------------------
# Interior region definitions (to create different resolution triangular mesh)
#------------------------------------------------------------------------------
# Read interior polygons

poly_extent1 = anuga.read_polygon('extent_pwrj02.csv')
poly_extent2 = anuga.read_polygon('extent_b_e.csv')
poly_extent3 = anuga.read_polygon('extent_b_w.csv')
poly_extent4 = anuga.read_polygon('extent_c_n_e.csv')
poly_extent5 = anuga.read_polygon('extent_c_n_w.csv')
poly_extent6 = anuga.read_polygon('extent_c_s_e.csv')
poly_extent7 = anuga.read_polygon('extent_c_s_w.csv')
poly_extent8 = anuga.read_polygon('extent_s_e.csv')
poly_extent9 = anuga.read_polygon('extent_s_w.csv')
poly_extent10 = anuga.read_polygon('extent_v_e.csv')
poly_extent11 = anuga.read_polygon('extent_v_w.csv')
poly_extent0 = anuga.read_polygon('extent_pwrj01.csv')
poly_extent_river = anuga.read_polygon('extent_river.csv')
poly_extent_river1 = anuga.read_polygon('extent_river1.csv')
poly_extent_river2 = anuga.read_polygon('extent_river2.csv')
poly_extent_add1 = anuga.read_polygon('extent_add_b_e.csv')
poly_extent_add2 = anuga.read_polygon('extent_add_b_w.csv')
poly_extent_add3 = anuga.read_polygon('extent_add_c_e.csv')
poly_extent_add4 = anuga.read_polygon('extent_add_c_w.csv')
# poly_extent_add5 = anuga.read_polygon('extent_add_s_w.csv')

# Optionally plot points making up these polygons
#plot_polygons([bounding_polygon, poly_extent, poly_extent0, poly_extent1],
#				style='boundingpoly', verbose=False)

# Define resolutions (max area per triangle) for each polygon
# Make these numbers larger to reduce the number of triangles in the model,
# and hence speed up the simulation
# bigger base_scale == less triangles
just_fitting = False
#base_scale = 25000 # 635763 # 112sec fit
base_scale = 50000 # 321403 # 69sec fit
#base_scale = 100000 # 162170 triangles # 45sec fit
#base_scale = 400000 # 42093
default_res = 5 * base_scale # Background resolution
extent_res = 2 * base_scale
extent0_res = 0.05 * base_scale
extent_river_res = 0.01 * base_scale
extent1_res = 0.5 * base_scale
# Define list of interior regions with associated resolutions
interior_regions = [[poly_extent1, extent1_res],
					[poly_extent2, extent1_res],
					[poly_extent3, extent1_res],
					[poly_extent4, extent1_res],
					[poly_extent5, extent1_res],
					[poly_extent6, extent1_res],
					[poly_extent7, extent1_res],
					[poly_extent8, extent1_res],
					[poly_extent9, extent1_res],
					[poly_extent10, extent1_res],
					[poly_extent11, extent1_res],
					[poly_extent0, extent0_res],
					[poly_extent_river, extent_river_res],
					[poly_extent_river1, extent_river_res],
					[poly_extent_river2, extent_river_res],
					[poly_extent_add1, extent_res],
					[poly_extent_add2, extent_res],
					[poly_extent_add3, extent_res],
					[poly_extent_add4, extent_res]]

#------------------------------------------------------------------------------
# Data for exporting ascii grid
#------------------------------------------------------------------------------
eastingmin = 371993.59529
eastingmax = 388005.08533
northingmin = 9123996.6679
northingmax = 9140000.2614
#------------------------------------------------------------------------------
# Data for landslide
#------------------------------------------------------------------------------
#slide_origin = [451871, 8128376] # Assume to be on continental shelf
#slide_depth = 500.
#------------------------------------------------------------------------------
# Data for Tides
#------------------------------------------------------------------------------
tide = 0.0