import random
import matplotlib.pyplot as plt
import networkx as nx


class Point:
    """
    Defines a point, composed of a x and a y coordinate
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def print_self(self):
        print("("+str(self.x)+","+str(self.y)+")")

class Segment:
    """
    Defines a segment, characterised by two Points, their difference in the x and y coordinate and the corresponding slope.
    """
    def __init__(self, p:Point, q:Point):
        #we assume they are always given in the correct order, will change this in the future
        self.p = p
        self.q = q
        self.dx = self.q.x - self.p.x 
        self.dy = self.q.y - self.p.y
        self.slope = self.dy / self.dx
    
    def equals(self, seg_two):
        """Checks if two segments are the same"""
        if self.p.x == seg_two.p.x and self.p.y == seg_two.p.y and self.q.x == seg_two.q.x and self.q.y == seg_two.q.y:
            return True
        else:
            return False
    
    def describe_itself(self):
        print("left point: (" + str(self.p.x)+ "," + str(self.p.y)  +") - right point: (" + str(self.q.x)+ "," + str(self.q.y) + ")")


    def y_at(self, x): 
        """y at x along the infinite line through the segment.""" 
        return self.p.y + self.slope * (x - self.p.x)
        
    def above(self, point:Point, rightp:Point):
        if point.y >= self.y_at(point.x):
            if point.y != self.y_at(point.x):
                return True
            else:
                if rightp.y > self.y_at(rightp.x):
                    #segment goes down, thus ends up below segment
                    return True
                else:
                    #we do not need to check for horizontal ones, because we will never enter in this if...else... in that case
                    return False
        else:
            return False
    
    def above_query(self, point:Point):
        if point.y >= self.y_at(point.x):
            return True
        else:
            return False
    
    def above_degenerate(self, point: Point): 
        """Return True if point lies above or on the segment at point.x. Used in degenerate cases to decide in which
        condition we actually found ourselves in.""" 
        if point.y == self.y_at(point.x):
            return True
        else:
            return False

class Trapezoid:
    _counter = 0

    def __init__(self, bottom, top, leftp, rightp):
        self.top = top #segment delimiting the trapezoid above
        self.bottom = bottom #segment delimiting the trapezoid below
        self.leftp = leftp #left point defining the edge of the trapezoid
        self.rightp = rightp #right point defining the edge of the trapezoid
        self.leaf = None #for DAG visits, has the ref to the leaf in the DAG corresponding to it
        self.upper_left_neighbour = None #top upper_left_neighbour = top trapezoid
        self.lower_left_neighbour = None #bottom lower_left_neighbour = bottom trapezoid
        self.upper_right_neighbour = None #symmetric to above
        self.lower_right_neighbour = None #symmetric to above
        self.id = Trapezoid._counter
        Trapezoid._counter += 1

    def neighbour_description(self):
        print("Upper left neigbour:")
        if self.upper_left_neighbour is not None:
            self.upper_left_neighbour.top.describe_itself()
            self.upper_left_neighbour.bottom.describe_itself()
        else:
            print("None")
        print("Upper right neighbour:")
        if self.upper_right_neighbour is not None:
            self.upper_right_neighbour.top.describe_itself()
            self.upper_right_neighbour.bottom.describe_itself()
        else:
            print("None")
        print("Lower left neighbour:")
        if self.lower_left_neighbour is not None:
            self.lower_left_neighbour.top.describe_itself()
            self.lower_left_neighbour.bottom.describe_itself()  
        else:
            print("None")
        print("Lower right neighbour:")
        if self.lower_right_neighbour is not None:
            self.lower_right_neighbour.top.describe_itself()
            self.lower_right_neighbour.bottom.describe_itself()
        else:
            print("None")

class TrapezoidalMap:
    def __init__(self, segments, xmin, xmax, ymin, ymax):
        self.segments = list(segments) #redundant, but why not
        self.top = Segment(Point(xmin, ymax), Point(xmax, ymax)) #t initialization, top of the bounding box
        self.bottom = Segment(Point(xmin, ymin), Point(xmax, ymin)) #at initialization, bottom of the bounding box
        self.starting_trapezoid = Trapezoid(self.bottom, self.top, Point(xmin, ymin), Point(xmax, ymax)) #at initialization, only bounding box
        self.root = Leaf(self.starting_trapezoid)
        self.trapezoid_list = [self.starting_trapezoid]
    
    def locate_trapezoid(self, q, right):
        """
        The following function takes the right endpoint of the segment we want to insert and finds the first trapezoid that
        intersects it. Depending on the node we find while navigating the DAG, we differ our behaviour.
        - if we encounter a NodeX, we check to know whether we have to go left or right of the node's endpoint
        - if we encounter a NodeY, we check to know whether we have to go above or below of the node's segment
        When we encounter a Leaf (so a reference to a trapezoid), we return the trapezoid it is linking to.
        -------------------------------------------------------------------------------------------------------
        This function is also used to perform the point location query.
        """
        node = self.root
        while not isinstance(node, Leaf):
            if isinstance(node, NodeX):
                if q.x < node.point.x:
                    node = node.left
                else:
                    node = node.right
            elif isinstance(node, NodeY):
                if node.segment.above(q, right):
                    node = node.left
                else:
                    node = node.right
            else:
                raise RuntimeError("Error: Unknown type of node encountered")
        return node.trapezoid
    
    def locate_trapezoid_query(self, q):
        """
        The following function takes the right endpoint of the segment we want to insert and finds the first trapezoid that
        intersects it. Depending on the node we find while navigating the DAG, we differ our behaviour.
        - if we encounter a NodeX, we check to know whether we have to go left or right of the node's endpoint
        - if we encounter a NodeY, we check to know whether we have to go above or below of the node's segment
        When we encounter a Leaf (so a reference to a trapezoid), we return the trapezoid it is linking to.
        -------------------------------------------------------------------------------------------------------
        This function is also used to perform the point location query.
        """
        node = self.root
        while not isinstance(node, Leaf):
            if isinstance(node, NodeX):
                if q.x < node.point.x:
                    node = node.left
                else:
                    node = node.right
            elif isinstance(node, NodeY):
                if node.segment.above_query(q):
                    node = node.left
                else:
                    node = node.right
            else:
                raise RuntimeError("Error: Unknown type of node encountered")
        return node.trapezoid
            
    def follow_segment(self, segment):
        """
        The following functions finds all the trapezoids that intersect the given segment and returns its list.
        """
        trapezoids = []
        trap = self.locate_trapezoid(segment.p, segment.q)
        trapezoids.append(trap)
        j = 0
        while j < len(trapezoids) and segment.q.x > trapezoids[j].rightp.x:
            if(segment.above_query(trapezoids[j].rightp)):
                if trapezoids[j].lower_right_neighbour != None:
                    print("Niet")
                    trapezoids.append(trapezoids[j].lower_right_neighbour)
            else:
                if trapezoids[j].upper_right_neighbour != None:
                    print("Da")
                    trapezoids.append(trapezoids[j].upper_right_neighbour)
            j += 1
        return trapezoids
    
    def create_trap(self, top, bottom, leftp, rightp): 
        """Helper: create trapezoid + leaf, add to registry.""" 
        trap = Trapezoid(bottom, top, leftp, rightp) 
        leaf = Leaf(trap)
        trap.leaf = leaf 
        self.trapezoid_list.append(trap)
        print("Added new trapezoid with: leftp = ", leftp.print_self(), " and rightp = ", rightp.print_self())
        return trap, leaf
    
    def remove_leaf(self, trap, new_node):
        old_leaf = trap.leaf
        parent = old_leaf.parent

        if parent is None:
            # old leaf was root
            self.root = new_node
            new_node.parent = None
        else:
            if parent.left is old_leaf:
                parent.left = new_node
            else:
                parent.right = new_node
            new_node.parent = parent

        old_leaf.parent = None

    
    def add_segments(self, segments):
        """
        The following function adds a set of previously randomized segments into a trapezoidal map, creating and destroying
        the trapezoids at each step and handling the update of the tree data structure that gets used to execute
        queries.
        It executes the following steps: for each segment
        -find the trapezoids that it intersects
        -removes them from the trapezoidal map
        -checks which of the two cases it falls under and handles it accordingly
         -CASE 1: the segment is self-contained in a single trapezoid
         -CASE 2: the segment intersects more than one trapezoid
         In this step, the new trapezoids are created and the tree structure update is handled
        The following steps get executed until all the segments have been inserted into the trapezoidal map.
        """
        for seg in segments:
            #we find the trapezoids that intersect with the segment
            trapezoids = self.follow_segment(seg)
            #we remove them from the TrapezoidalMap
            for trap in trapezoids:
                if trap not in self.trapezoid_list: 
                    print("ERROR: DAG returned a stale trapezoid:", trap.bottom.describe_itself(), trap.top.describe_itself(),trap.leftp.print_self(), trap.rightp.print_self()) 
                    raise RuntimeError("Stale trapezoid in DAG")
                self.trapezoid_list.remove(trap)
            #first case: segment completely contained in a single trapezoid. This leads to at most 4 new ones being created
            if len(trapezoids) == 1:
                print("Number of trapezoids before creation: " + str(len(self.trapezoid_list)))
                leaf_A = None 
                leaf_B = None
                trap_A = None
                trap_B = None
                #left trapezoid
                if trapezoids[0].leftp.x < seg.p.x:
                    trap_A, leaf_A = self.create_trap(trapezoids[0].top, trapezoids[0].bottom, trapezoids[0].leftp, seg.p)
                #right trapezoid
                if trapezoids[0].rightp.x > seg.q.x:
                    trap_B, leaf_B = self.create_trap(trapezoids[0].top, trapezoids[0].bottom, seg.q, trapezoids[0].rightp)
                #above trapezoid
                trap_C, leaf_C = self.create_trap(trapezoids[0].top, seg, seg.p, seg.q)
                #below trapezoid
                trap_D, leaf_D = self.create_trap(seg, trapezoids[0].bottom, seg.p, seg.q)
                #we need to modify the tree data structure
                #we get the leaf to remove
                #leaf_to_remove = trapezoids[0].leaf
                #we construct the new tree, with the following structure:
                #      first_nodex
                #         /   \
                #   leaf_A     second_nodex
                #                  / \
                #        first_nodey  leaf_B
                #            / \
                #      leaf_C   leaf_D
                #if leaf_A is None:
                #    leaf_A = trapezoids[0].leaf   # or the leaf you are replacing
                #    trap_A = trapezoids[0]
                #if leaf_B is None:
                #    leaf_B = trapezoids[0].leaf
                #    trap_B = trapezoids[0]

                first_nodey = NodeY(seg, leaf_C, leaf_D)
                second_nodex = NodeX(seg.q, first_nodey, leaf_B)
                first_nodex = NodeX(seg.p, leaf_A, second_nodex)
                #first_nodex.parent = leaf_to_remove.parent
                #we finally remove the not needed leaf from the tree (OPTIONALLY: destroy the trapezoid directly to free space)
                #however, we need to handle the case in which we are removing the root, otherwise the algorithm breaks
                self.remove_leaf(trapezoids[0], first_nodex)
                #lastly, we need to add the neighbours for each new trapezoid. The new trapezoids should look something like the sketch below (if not degenerate)
                #  _ _ _ _ _ _ _
                # |  |      |   |
                # |  |------|   |
                # |_ |_ _ _ |_ _|
                # 
                if trap_A is not None:
                    trap_A.upper_left_neighbour = trapezoids[0].upper_left_neighbour
                    trap_A.upper_right_neighbour = trap_C
                    trap_A.lower_left_neighbour = trapezoids[0].lower_left_neighbour
                    trap_A.lower_right_neighbour = trap_D
                    #we update the reference to the delete trapezoid in those that are adjacent with it on the left side
                    if trapezoids[0].lower_left_neighbour is not None:
                        if trapezoids[0].lower_left_neighbour.bottom.equals(trap_A.bottom):
                            trapezoids[0].lower_left_neighbour.lower_right_neighbour = trap_A
                        if trapezoids[0].lower_left_neighbour.top.equals(trap_A.top):
                            trapezoids[0].lower_left_neighbour.upper_right_neighbour = trap_A
                        if trapezoids[0].upper_left_neighbour is not None and trapezoids[0].upper_left_neighbour.top.equals(trap_A.top):
                            trapezoids[0].upper_left_neighbour.upper_right_neighbour = trap_A 

                if trap_B is not None:
                    trap_B.upper_left_neighbour = trap_C
                    trap_B.upper_right_neighbour = trapezoids[0].upper_right_neighbour
                    trap_B.lower_left_neighbour = trap_D
                    trap_B.lower_right_neighbour = trapezoids[0].lower_right_neighbour
                    #we update the reference in the neighbours to the destroyed trapezoid    
                    if trapezoids[0].lower_right_neighbour is not None:
                        if trapezoids[0].lower_right_neighbour.bottom.equals(trap_B.bottom):
                            trapezoids[0].lower_right_neighbour.lower_left_neighbour = trap_B
                        if trapezoids[0].lower_right_neighbour.top.equals(trap_B.top):
                            trapezoids[0].lower_right_neighbour.upper_left_neighbour = trap_B 
                        if trapezoids[0].upper_right_neighbour is not None and trapezoids[0].upper_right_neighbour.top.equals(trap_B.top):
                            trapezoids[0].upper_right_neighbour.upper_left_neighbour = trap_B     

                if trap_A is not None:
                    trap_C.upper_left_neighbour = trap_A
                    trap_C.lower_left_neighbour = None
                    trap_D.lower_left_neighbour = trap_A
                    trap_D.upper_left_neighbour = None
                else:
                    #degenerate case, left endpoint of segments coincides
                    #we need to see whether we are above or below the already present segment
                    if seg.p.x == trapezoids[0].leftp.x and seg.p.y == trapezoids[0].leftp.y:
                        #segments starts exactly at another endpoint of a segment
                        if trapezoids[0].upper_left_neighbour is not None and trapezoids[0].upper_left_neighbour.top.equals(trap_C.top):
                            trap_C.upper_left_neighbour = trapezoids[0].upper_left_neighbour
                            trap_C.lower_left_neighbour = None
                            trapezoids[0].upper_left_neighbour.upper_right_neighbour = trap_C
                        else:
                            trap_C.upper_left_neighbour = None
                            trap_C.lower_left_neighbour = None
                        if trapezoids[0].lower_left_neighbour is not None and trapezoids[0].lower_left_neighbour.bottom.equals(trap_D.bottom):
                            trap_D.upper_left_neighbour = None
                            trap_D.lower_left_neighbour = trapezoids[0].lower_left_neighbour
                            trapezoids[0].lower_left_neighbour.lower_right_neighbour = trap_D 
                        else:
                            trap_D.upper_left_neighbour = None
                            trap_D.lower_left_neighbour = None
                    
                    elif trapezoids[0].top.above_degenerate(seg.p):
                        trap_C.upper_left_neighbour = None
                        trap_C.lower_left_neighbour = None
                        trap_D.upper_left_neighbour = None
                        trap_D.lower_left_neighbour = trapezoids[0].lower_left_neighbour
                        if trapezoids[0].lower_left_neighbour is not None and trapezoids[0].lower_left_neighbour.bottom.equals(trap_D.bottom):
                            trapezoids[0].lower_left_neighbour.lower_right_neighbour = trap_D
                    else:
                        trap_C.upper_left_neighbour = trapezoids[0].upper_left_neighbour
                        trap_C.lower_left_neighbour = None
                        trap_D.upper_left_neighbour = None
                        trap_D.lower_left_neighbour = None  
                        if trapezoids[0].upper_left_neighbour is not None and trapezoids[0].upper_left_neighbour.top.equals(trap_C.top):
                            trapezoids[0].upper_left_neighbour.uppe_right_neighbour = trap_C                        

                if trap_B is not None:
                    trap_C.upper_right_neighbour = trap_B
                    trap_C.lower_right_neighbour = None
                    trap_D.lower_right_neighbour = trap_B 
                    trap_D.upper_right_neighbour = None
                else:
                    #degenerate case, right endpoint of segments coincides
                    #we need to see whether we are above or below the already present segment
                    if seg.q.x == trapezoids[0].rightp.x and seg.q.y == trapezoids[0].rightp.y:
                        #segment rightpoint lies exactly on the vertex of another segment
                        if trapezoids[0].upper_right_neighbour is not None and trapezoids[0].upper_right_neighbour.top.equals(trap_C.top):
                            trap_C.upper_right_neighbour = trapezoids[0].upper_right_neighbour
                            trap_C.lower_right_neighbour = None
                            trapezoids[0].upper_right_neighbour.upper_left_neighbour = trap_C                              
                        else:
                            trap_C.upper_right_neighbour = None
                            trap_C.lower_right_neighbour = None

                        if trapezoids[0].lower_right_neighbour is not None and trapezoids[0].lower_right_neighbour.bottom.equals(trap_D.bottom):
                            trap_D.upper_right_neighbour = None
                            trap_D.lower_right_neighbour = trapezoids[0].lower_right_neighbour 
                            trapezoids[0].lower_right_neighbour.lower_left_neighbour = trap_D
                        else:    
                            trap_D.upper_right_neighbour = None
                            trap_D.lower_right_neighbour = None
                    
                    elif trapezoids[0].top.above_degenerate(seg.q):
                        trap_C.upper_right_neighbour = None
                        trap_C.lower_right_neighbour = None
                        trap_D.upper_right_neighbour = None
                        trap_D.lower_right_neighbour = trapezoids[0].lower_right_neighbour
                        if trapezoids[0].lower_right_neighbour is not None and trapezoids[0].lower_right_neighbour.bottom.equals(trap_D.bottom):
                            trapezoids[0].lower_right_neighbour.lower_left_neighbour = trap_D                        
                    else:
                        trap_C.upper_right_neighbour = trapezoids[0].upper_right_neighbour
                        trap_C.lower_right_neighbour = None
                        trap_D.upper_right_neighbour = None
                        trap_D.lower_right_neighbour = None 
                        if trapezoids[0].upper_right_neighbour is not None and trapezoids[0].upper_right_neighbour.top.equals(trap_C.top):
                            trapezoids[0].upper_right_neighbour.upper_left_neighbour = trap_C  
                   
            #general case: segment intersects multiple trapezoids.
            else:
                #we update the tree structure with the leaves for the new trapezoids
                #substitution follows the following rules:
                # - for first_trap: if left endpoint of segment is in its interior, it gets a x node for seg.p.x and a y node for seg
                # - for in between trapezoids: y node for seg
                # - for last_trap: if right endpoint of segment is in its interior, it gets a x node for seg.q.x and a y node for seg
                
                new_traps = []
                new_upper = []
                new_lower = []
                #first trapezoid
                first_trap = trapezoids[0]
                trap_left = None
                left_leaf = None
                trap_upper, upper_leaf = self.create_trap(first_trap.top, seg, seg.p, first_trap.rightp)
                trap_lower, lower_leaf = self.create_trap(seg, first_trap.bottom, seg.p, first_trap.rightp)
                if first_trap.leftp.x < seg.p.x:
                    trap_left, left_leaf = self.create_trap(first_trap.top, first_trap.bottom, first_trap.leftp, seg.p)

                node_y = NodeY(seg, upper_leaf, lower_leaf)
                if trap_left is not None:
                    node_x = NodeX(seg.p, left_leaf, node_y)
                    self.remove_leaf(first_trap, node_x)
                else:
                    self.remove_leaf(first_trap, node_y)              
                new_traps.append(trap_upper)
                new_traps.append(trap_lower)
                new_upper.append (upper_leaf)
                new_lower.append(lower_leaf)
                #we directly assign the neighbours for the left trapezoid
                if trap_left is not None:
                    trap_left.lower_left_neighbour = first_trap.lower_left_neighbour
                    trap_left.lower_right_neighbour = trap_lower
                    trap_left.upper_left_neighbour = first_trap.upper_left_neighbour
                    trap_left.upper_right_neighbour = trap_upper
                    if first_trap.lower_left_neighbour is not None:
                        if first_trap.lower_left_neighbour.bottom.equals(trap_left.bottom):
                            first_trap.lower_left_neighbour.lower_right_neighbour = trap_left
                        if first_trap.lower_left_neighbour.top.equals(trap_left.top):
                            first_trap.lower_left_neighbour.upper_right_neighbour = trap_left
                        if first_trap.upper_left_neighbour is not None and first_trap.upper_left_neighbour.top.equals(trap_left.top):
                            first_trap.upper_left_neighbour.upper_right_neighbour = trap_left

                #trapezoids in between
                for trap in trapezoids[1:-1]:
                    trap_upper, upper_leaf = self.create_trap(trap.top, seg, trap.leftp, trap.rightp)
                    trap_lower, lower_leaf = self.create_trap(seg, trap.bottom, trap.leftp, trap.rightp)
                    node_y = NodeY(seg, upper_leaf, lower_leaf)
                    #node_y.parent = trap.leaf.parent
                    self.remove_leaf(trap, node_y)
                    new_traps.append(trap_upper)
                    new_traps.append(trap_lower)
                    new_upper.append (upper_leaf)
                    new_lower.append(lower_leaf)
            
                #last trapezoid
                last_trap = trapezoids[-1]
                trap_right = None
                right_leaf = None
                trap_upper, upper_leaf = self.create_trap(last_trap.top, seg, last_trap.leftp, seg.q)
                trap_lower, lower_leaf = self.create_trap(seg, last_trap.bottom, last_trap.leftp, seg.q)
                if last_trap.rightp.x > seg.q.x:
                    trap_right, right_leaf = self.create_trap(last_trap.top, last_trap.bottom, seg.q, last_trap.rightp)
                #parent = last_trap.leaf.parent
                #parent = last_trap.leaf.parent
                node_y = NodeY(seg, upper_leaf, lower_leaf)
                if trap_right is not None:
                    node_x = NodeX(seg.q, node_y, right_leaf)
                    self.remove_leaf(last_trap, node_x)
                else:
                    self.remove_leaf(last_trap, node_y)
                new_traps.append(trap_upper)
                new_traps.append(trap_lower)
                new_upper.append (upper_leaf)
                new_lower.append(lower_leaf)
                #we directly assign the neighbours to the right trapezoid
                if trap_right is not None:
                    trap_right.lower_left_neighbour = trap_lower
                    trap_right.lower_right_neighbour = last_trap.lower_right_neighbour
                    trap_right.upper_left_neighbour = trap_upper
                    trap_right.upper_right_neighbour = last_trap.upper_right_neighbour
                    if last_trap.lower_right_neighbour is not None:
                        if last_trap.lower_right_neighbour.bottom.equals(trap_right.bottom):
                            last_trap.lower_right_neighbour.lower_left_neighbour = trap_right
                        if last_trap.lower_right_neighbour.top.equals(trap_right.top):
                            last_trap.lower_right_neighbour.upper_left_neighbour = trap_right 
                        if last_trap.upper_right_neighbour is not None and last_trap.upper_right_neighbour.top.equals(trap_right.top):
                            last_trap.upper_right_neighbour.upper_left_neighbour = trap_right 
                    
                #we now assign the correct neighbours to all the intermediate trapezoids
                for i in range(len(new_upper)):
                    upper_trapezoid = new_upper[i].trapezoid
                    lower_trapezoid = new_lower[i].trapezoid

                    # LEFT NEIGHBOURS
                    if i == 0:
                        if trap_left is not None:
                        # first trapezoid: connect to left remainder, if it exist
                            upper_trapezoid.upper_left_neighbour = trap_left
                            upper_trapezoid.lower_left_neighbour = trap_left
                            lower_trapezoid.upper_left_neighbour = trap_left
                            lower_trapezoid.lower_left_neighbour = trap_left
                        else:
                            # borderline case, left endpoint of added segments coincides with the one of an already present segment.
                            # In this case, we have two cases, with different behaviour:
                            # - if we created trapezoids above the original first trapezoid right point, the upper trapezoid is the one that has left neighbours, while the lower one has none
                            # - if we created trapezoids below the original first trapezoid right point, the lower trapezoid is the one that has left neighbours, while the upper one doesn't
                            if seg.p.x == first_trap.leftp.x and seg.p.y == first_trap.leftp.y:
                                #segment left point lies exactly on the vertex of another segment
                                if first_trap.upper_left_neighbour is not None and first_trap.upper_left_neighbour.top.equals(upper_trapezoid.top):
                                    upper_trapezoid.upper_left_neighbour = first_trap.upper_left_neighbour
                                    upper_trapezoid.lower_left_neighbour = None
                                    first_trap.upper_left_neighbour.upper_right_neighbour = upper_trapezoid                              
                                else:
                                    upper_trapezoid.upper_left_neighbour = None
                                    upper_trapezoid.lower_left_neighbour = None
                                if first_trap.lower_left_neighbour is not None and first_trap.lower_left_neighbour.bottom.equals(lower_trapezoid.bottom):
                                    lower_trapezoid.upper_left_neighbour = None
                                    lower_trapezoid.lower_left_neighbour = first_trap.lower_left_neighbour
                                    first_trap.lower_left_neighbour.lower_right_neighbour = lower_trapezoid 
                                else:
                                    lower_trapezoid.upper_left_neighbour = None
                                    lower_trapezoid.lower_left_neighbour = None

                            elif first_trap.top.above_degenerate(seg.p):
                                upper_trapezoid.upper_left_neighbour = None
                                upper_trapezoid.lower_left_neighbour = None
                                lower_trapezoid.upper_left_neighbour = None
                                lower_trapezoid.lower_left_neighbour = first_trap.lower_left_neighbour
                                if first_trap.lower_left_neighbour is not None and first_trap.lower_left_neighbour.bottom.equals(lower_trapezoid.bottom):
                                    first_trap.lower_left_neighbour.lower_right_neighbour = lower_trapezoid                                
                            else:
                                upper_trapezoid.upper_left_neighbour = first_trap.upper_left_neighbour
                                upper_trapezoid.lower_left_neighbour = None
                                lower_trapezoid.upper_left_neighbour = None
                                lower_trapezoid.lower_left_neighbour = None 
                                if first_trap.upper_left_neighbour is not None and first_trap.upper_left_neighbour.top.equals(upper_trapezoid.top):
                                    first_trap.upper_left_neighbour.upper_right_neighbour = upper_trapezoid                                       
                    else:
                        # connect to previous new trapezoids
                        if upper_trapezoid.top.equals(new_upper[i-1].trapezoid.top):
                            upper_trapezoid.upper_left_neighbour = new_upper[i-1].trapezoid
                        else:
                            upper_trapezoid.upper_left_neighbour = None
                        upper_trapezoid.lower_left_neighbour = new_upper[i-1].trapezoid
                        lower_trapezoid.upper_left_neighbour = new_lower[i-1].trapezoid
                        if lower_trapezoid.bottom.equals(new_lower[i-1].trapezoid.bottom):
                            lower_trapezoid.lower_left_neighbour = new_lower[i-1].trapezoid
                        else:
                            lower_trapezoid.lower_left_neighbour = None

                        #connect to already existing trapezoids, updating stale references
                        if trapezoids[i].upper_left_neighbour is not None and trapezoids[i].upper_left_neighbour.top.equals(upper_trapezoid.top):
                            trapezoids[i].upper_left_neighbour.upper_right_neighbour = upper_trapezoid
                            upper_trapezoid.upper_left_neighbour = trapezoids[i].upper_left_neighbour 
                        if trapezoids[i].lower_left_neighbour is not None and trapezoids[i].lower_left_neighbour.bottom.equals(lower_trapezoid.bottom):
                            trapezoids[i].lower_left_neighbour.lower_right_neighbour = lower_trapezoid
                            lower_trapezoid.lower_left_neighbour = trapezoids[i].lower_left_neighbour

                    # RIGHT NEIGHBOURS
                    if i == len(new_upper) - 1:
                        if trap_right is not None:
                            # last trapezoid: connect to right remainder
                            upper_trapezoid.upper_right_neighbour = trap_right
                            upper_trapezoid.lower_right_neighbour = trap_right
                            lower_trapezoid.upper_right_neighbour = trap_right
                            lower_trapezoid.lower_right_neighbour = trap_right
                        else:
                            # borderline case, right endpoint of added segments coincides with the one of an already present segment.
                            # In this case, we have two cases, with different behaviour:
                            # - if we created trapezoids above the original first trapezoid right point, the upper trapezoid is the one that has left neighbours, while the lower one has none
                            # - if we created trapezoids below the original first trapezoid right point, the lower trapezoid is the one that has left neighbours, while the upper one doesn't
                            if seg.q.x == last_trap.rightp.x and seg.q.y == last_trap.rightp.y:
                                #segment right point lies exactly on the endpoint of another segment
                                if last_trap.upper_right_neighbour is not None and last_trap.upper_right_neighbour.top.equals(upper_trapezoid.top):
                                    upper_trapezoid.upper_right_neighbour = trapezoids[i].upper_right_neighbour
                                    upper_trapezoid.lower_right_neighbour = None
                                    last_trap.upper_right_neighbour.upper_left_neighbour = upper_trapezoid                              
                                else:
                                    upper_trapezoid.upper_right_neighbour = None
                                    upper_trapezoid.lower_right_neighbour = None

                                if last_trap.lower_right_neighbour is not None and last_trap.lower_right_neighbour.bottom.equals(lower_trapezoid.bottom):
                                    lower_trapezoid.upper_right_neighbour = None
                                    lower_trapezoid.lower_right_neighbour = trapezoids[i].lower_right_neighbour 
                                    last_trap.lower_right_neighbour.lower_left_neighbour = lower_trapezoid
                                else:    
                                    lower_trapezoid.upper_right_neighbour = None
                                    lower_trapezoid.lower_right_neighbour = None
                               
                            elif last_trap.top.above_degenerate(seg.q):
                                upper_trapezoid.upper_right_neighbour = None
                                upper_trapezoid.lower_right_neighbour = None
                                lower_trapezoid.upper_right_neighbour = None
                                lower_trapezoid.lower_right_neighbour = last_trap.lower_right_neighbour
                                if last_trap.lower_right_neighbour is not None and last_trap.lower_right_neighbour.bottom.equals(lower_trapezoid.bottom):
                                    last_trap.lower_right_neighbour.lower_left_neighbour = lower_trapezoid                                
                            else:
                                upper_trapezoid.upper_right_neighbour = last_trap.upper_right_neighbour
                                upper_trapezoid.lower_right_neighbour = None
                                lower_trapezoid.upper_right_neighbour = None
                                lower_trapezoid.lower_right_neighbour = None
                                if last_trap.upper_right_neighbour is not None and last_trap.upper_right_neighbour.top.equals(upper_trapezoid.top):
                                    last_trap.upper_right_neighbour.upper_left_neighbour = upper_trapezoid                                                             
                    else:
                        # connect to next new trapezoids
                        if upper_trapezoid.top.equals(new_upper[i+1].trapezoid.top):
                            upper_trapezoid.upper_right_neighbour = new_upper[i+1].trapezoid
                        else:
                            upper_trapezoid.upper_right_neighbour = None
                        upper_trapezoid.lower_right_neighbour = new_upper[i+1].trapezoid
                        lower_trapezoid.upper_right_neighbour = new_lower[i+1].trapezoid
                        if lower_trapezoid.bottom.equals(new_lower[i+1].trapezoid.bottom):
                            lower_trapezoid.lower_right_neighbour = new_lower[i+1].trapezoid
                        else:
                            lower_trapezoid.lower_right_neighbour = None
                        #connect to already existing trapezoids
                        if trapezoids[i].upper_right_neighbour is not None and trapezoids[i].upper_right_neighbour.top.equals(upper_trapezoid.top):
                            trapezoids[i].upper_right_neighbour.upper_left_neighbour = upper_trapezoid
                            upper_trapezoid.upper_right_neighbour = trapezoids[i].upper_right_neighbour  
                        if trapezoids[i].lower_right_neighbour is not None and trapezoids[i].lower_right_neighbour.bottom.equals(lower_trapezoid.bottom):
                            trapezoids[i].lower_right_neighbour.lower_left_neighbour = lower_trapezoid
                            lower_trapezoid.lower_right_neighbour = trapezoids[i].lower_right_neighbour

            self.plot_map(self.segments, self.segments.index(seg), title=f"After inserting segment {seg.p.x, seg.p.y}->{seg.q.x, seg.q.y}")
            self.draw_dag()

    def plot_map(self, segments, segment_size, title="Trapezoidal Map"):
        fig, ax = plt.subplots(figsize=(8, 8))

        print("New exec:")
        for T in self.trapezoid_list:
            xl = T.leftp.x
            xr = T.rightp.x

            # If left and right are identical, still draw the vertical line
            yt_l = T.top.y_at(xl)
            yt_r = T.top.y_at(xr)
            yb_l = T.bottom.y_at(xl)
            yb_r = T.bottom.y_at(xr)
            print("BOTTOM:")
            T.bottom.describe_itself()
            print("TOP:")
            T.top.describe_itself()
            print("NEIHBOURS")
            T.neighbour_description()

            # draw top and bottom
            ax.plot([xl, xr], [yt_l, yt_r], 'g-')
            ax.plot([xl, xr], [yb_l, yb_r], 'r-')

            # draw vertical boundaries
            #ax.plot([xl, xl], [self.starting_trapezoid.leftp.y, self.starting_trapezoid.rightp.y], 'k--', alpha=0.4)
            #ax.plot([xr, xr], [self.starting_trapezoid.leftp.y, self.starting_trapezoid.rightp.y], 'k--', alpha=0.4)
            ax.plot([xl, xl], [yt_l, yb_l], 'k--', alpha=0.4)
            ax.plot([xr, xr], [yt_r, yb_r], 'k--', alpha=0.4)
            xc = 0.5 * (xl + xr)
            yc = 0.25 * (yt_l + yt_r + yb_l + yb_r)

            ax.text(
                xc, yc,
                f"T{T.id}",
                fontsize=9,
                ha="center",
                va="center",
                color="black"
            )

        # original segments
        for s in segments[:segment_size+1]:
            ax.plot([s.p.x, s.q.x], [s.p.y, s.q.y], 'b-', linewidth=2)

        print("Trapezoids: " + str(len(self.trapezoid_list)))
        ax.set_title(title)
        ax.set_aspect('equal', adjustable='box')
        plt.show()

    def draw_dag(self, title="Search DAG"):
        G = nx.DiGraph()
        node_ids = {}

        class NullLeaf:
            pass

        def get_id(node):
            if node not in node_ids:
                node_ids[node] = f"{type(node).__name__}_{len(node_ids)}"
            return node_ids[node]

        def dfs(node, depth=0):
            nid = get_id(node)
            G.add_node(nid, depth=depth)

            if isinstance(node, Leaf):
                label = f"Leaf\nTrap[{node.trapezoid.id}]"
                G.nodes[nid]["label"] = label
                G.nodes[nid]["color"] = "lightgreen"

            elif isinstance(node, NodeX):
                label = f"X\nx={node.point.x}"
                G.nodes[nid]["label"] = label
                G.nodes[nid]["color"] = "skyblue"
                for child in [node.left, node.right]:
                    if child is None:
                        child = NullLeaf()
                    cid = get_id(child)
                    G.add_edge(nid, cid)
                    dfs(child, depth+1)

            elif isinstance(node, NodeY):
                seg = node.segment
                label = f"Y\n({seg.p.x},{seg.p.y})→({seg.q.x},{seg.q.y})"
                G.nodes[nid]["label"] = label
                G.nodes[nid]["color"] = "orange"
                for child in [node.left, node.right]:
                    if child is None:
                        child = NullLeaf()
                    cid = get_id(child)
                    G.add_edge(nid, cid)
                    dfs(child, depth+1)
            else:
                G.nodes[nid]["color"] = "gray"

        dfs(self.root)

        # --- Tree-like layout (minimal addition) ---
        pos = {}
        x_counter = 0

        def assign_pos(node):
            nonlocal x_counter
            nid = get_id(node)
            depth = G.nodes[nid]["depth"]

            children = list(G.successors(nid))

            if not children:
                pos[nid] = (x_counter, -depth)
                x_counter += 1
                return pos[nid][0]

            child_xs = []
            for c in children:
                cx = assign_pos(next(k for k, v in node_ids.items() if v == c))
                child_xs.append(cx)

            pos[nid] = (sum(child_xs) / len(child_xs), -depth)
            return pos[nid][0]

        assign_pos(self.root)

        labels = nx.get_node_attributes(G, "label")
        colors = [G.nodes[n]["color"] for n in G.nodes]

        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, with_labels=False, arrows=True, node_color=colors, node_size=2000)
        nx.draw_networkx_labels(G, pos, labels)
        plt.title(title)
        plt.show()


    def query(self, point):
        """
        A wrapper function that executes the point location query by using the locate_trapezoid_query function
        (basically locate_trapezoid, but with only 1 argument instead of 2)
        """
        return self.locate_trapezoid_query(point)

class Leaf():
    def __init__(self, trapezoid, parent=None):
        self.parent = parent
        self.trapezoid = trapezoid
        trapezoid.leaf = self

class NodeX():
    def __init__(self, point, left_child, right_child, parent=None):
        self.parent = parent
        self.point = point
        self.left = left_child
        self.right = right_child
        if left_child is not None:
            left_child.parent = self
        if right_child is not None:
            right_child.parent = self

class NodeY():
    def __init__(self, segment, left_child, right_child, parent=None):
        self.parent = parent
        self.segment = segment
        self.left = left_child
        self.right = right_child
        left_child.parent = self
        right_child.parent = self

def main():
    #Bounding box
    xmin, xmax = -10,10
    ymin, ymax = -10,10
    #we declare the segments we want to insert
    #segments = [Segment(Point(-9,0), Point(3,-7)), Segment(Point(-6,0), Point(9,0)), Segment(Point(-8, -4), Point(-7, -7))]
    #segments = [Segment(Point(-9,9), Point(0,9)), Segment(Point(-9,9), Point(6,5)),Segment(Point(6,5), Point(9,9))]
    segments = [Segment(Point(-9,0), Point(3,-7)), Segment(Point(-9,0), Point(4,7)), Segment(Point(4,7), Point(9,0)), Segment(Point(3,-7), Point(9,0)), Segment(Point(-9,0), Point(9,0))]
    #we randomize them - after all, this is a randomized incremental algorithm
    random.shuffle(segments)
    #we initialize the trapezoidal map
    TMap = TrapezoidalMap(segments, xmin, xmax, ymin, ymax)
    #finally, we insert the segments to create the final trapezoidal map
    TMap.add_segments(segments)
    points_to_test = [Point(1,3), Point(-8,0), Point(-9.9,-9.9), Point(9.9, 7), Point(8,4), Point(5,9), Point(0, 4)]
    for point in points_to_test:
        trap = TMap.query(point)
        print("Point " + str(point.x), str(point.y) + " inside trapezoid: " + str(trap.id))

if __name__ == '__main__':
    main()