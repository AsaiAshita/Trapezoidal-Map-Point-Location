# Trapezoidal-Map-Point-Location
A Python implementation of the randomized incremental point location algorithm based on a trapezoidal map, based on the *Computational Geometry: Algorithms and Applications* book written by Mark Berg, Marc Kreveld, Mark Overmars and Otfried Schwarzkopf and on the teachings offered by the *Spatial Databases* course.  

The following repository contains 2 versions of the algorithm:  
 - a version that works under general position
 - a version that works without the need for the general position premise (meaning we allow multiple endpoints to lie on the same x coordinate and query points to be found on vertical lines, the two premises discussed in the reference book *Computational Geometry: Algorithms and Applications*)

# Requirements
In order for the visualization part of the code to work correctly, you will need to install `matplotlib` and `networkx`. You can install them by using pip as follows:  
```
pip install matplotlib networkx
```

# Usage
`python3 point_location.py`  
Segments and points are defined in the `main` of each file (except for `point_location_no_general_position_GRASS.py`, which takes segments as inputs from a file called `segments.txt`, stored in the same directory as the script, and generates a set number of random points - by default 200 - to test).

# Notes
The second version also has a variant that can read segments from a file (`point_location_no_general_position_GRASS.py`) and that was thought to work with data generated from GIS systems like GRASS. If you use this version, the input file is expected to be in the form `x1 y1 x2 y2`, where each line is a segment formed by points (x1,y1) and (x2,y2). If you use GRASS, you can use the `parser_GRASS.py` provided in the repository to parse data obtained from GRASS. For an example on how to use it, you can run the following commands: 
```
v.random output=seeds_3 n=3 #create n random points
v.voronoi input=seeds_3 output=voronoi_3 #creates the voronoi map for the given set of points
v.db.addtable map=voronoi_3 #to permit us to then turn it into an ascii file
v.to.lines input=voronoi_3 output=segments_voronoi_3 --overwrite #convert to lines
v.out.ascii input=segments_voronoi_3 format=standard output=segments_full.txt --overwrite #convert to ascii
python3 parser_GRASS.py #convert to final format for algorithm
```
Note that we use Voronoi to generate the segments, this introduces a pesky bounding box that may cause problems (in theory it shouldn't, in practice it may - from the tests that I have run it should not pose a problem, but be aware of this if you actually face some issues), so try to remove it if possible. Also, depending on your map size, you will have to adjust the bounding box dimensions in the code.  

Both algorithm also offer a visualization of both the trapezoidal map and its associated DAG.  
![Example of Trapezoidal Map](/Trapezoidal_Map_Example.png)
![Example of DAG](/DAG_Example.png)  

Reference: *Mark, D. B., Otfried, C., Marc, V. K., & Mark, O. (2008). Computational geometry algorithms and applications. Spinger.*
