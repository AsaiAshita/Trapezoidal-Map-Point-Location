# Trapezoidal-Map-Point-Location
A Python implementation of the randomized incremental point location algorithm based on a trapezoidal map.  
The following repository contains 2 versions of the algorithm:  
 - a version that works under general position
 - a version that works without the need for the general position premise
The second version also has a variant that can read segments from a file (`point_location_no_general_position_GRASS.py`) and that was thought to work with data generated from GIS systems like GRASS. If you use this version, the input file is expected to be in the form `x1 y1 x2 y2`, where each line is a segment formed by points (x1,y1) and (x2,y2). If you use GRASS, you can use the `GRASS_parser.py` provided in the repository to parse data obtained from GRASS. For an example on how to use it, see `GRASS_commands.txt` - note that we use Voronoi to generate the segments, this introduces a pesky bounding box that may cause problems, so try to remove it if possible. Also, depending on your map size, you will have to adjust the bounding box dimensions in the code.
