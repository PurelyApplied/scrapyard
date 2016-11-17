import math
from itertools import product
from operator import mul, add, sub

# Current errors: I need to account for a gap space in the wall.
# Currently, I'm jumping "around" the wall rather than bouncing off
# it, going (2, 1, -1, -2) and not hitting 0.  Although, incidentally,
# this shouldn't? change the raw count of beams...

# verification currently spits out two failures.  Double check edgecases.


# Dimensions bound 1 < dim < 1000
# Positioned such that 0 < pos < dim
# Maximum distance: int 1 < dis < 10000

# We imagine reflections from walls instead as extensions into a
# reflected space (example below).  Instead of a single target, we
# choose from many targets in this extension.  Likewise, instead
# of a singular position to avoid, we must avoid all reflections
# of ourselves.

# original
# +-----+-----+
# |.....|.....|
# |.x...|...x.|
# |.....|.....|
# |.....|.....|
# |....y|y....|
# +-----+-----+
#        reflection
    
# General outline to this solution:
# * Generate a list of possible target coordinates, constrained
#   by beam distance.
# * Generate a list of possible self coordinates, constrained
#   by beam distance.
# * Convert all coordinates to polar-like coordinates, using the
#   tuple format (dx, dy, dist)
# * For each possible target, accept the beam b=(dx1, dy1, dist1)
#   so long as there exists no self-reflected coordinate s=(dx2,
#   dy2, dist2) such that (dx1, dy1) == (dx2, dy2) and dist2 < dist1

def answer(dimensions, my_position, guard_position, distance):
    ## Provided positions are 1-indexed.  We adjust internally to be
    ## zero-indexed
    my_position = my_position[0]-1, my_position[1]-1, 
    guard_position = guard_position[0]-1, guard_position[1]-1, 
    my_reflections = get_reflections(dimensions, my_position,
                                     my_position, distance)
    guard_reflections = get_reflections(dimensions, my_position,
                                        guard_position, distance)
    beams_map = {}
    # Identify each angle and keep the "closest" guard.
    for dx, dy, r, tx, ty in map(lambda x : to_polar(my_position, x),
                         guard_reflections):
        if (dx, dy) not in beams_map or r < beams_map[(dx, dy)]:
            beams_map[(dx, dy)] = (r, tx, ty)
    # Don't shoot yourself.
    for dx, dy, r, tx, ty in map(lambda x : to_polar(my_position, x),
                         my_reflections):
        if (dx, dy) in beams_map and r < beams_map[(dx, dy)][0]:
            print("Removing {!r}: would hit me first.".format((dx, dy, r)))
            beam_map.pop((dx, dy))
    return beams_map


def get_reflections(dimensions, my_position, target_position, distance):
    '''Returns the coordinates of reflected position within (Euclidean)
distance'''
    # Loose bounds, to be tightened momentarily
    radius_x, radius_y = map(lambda x : distance // x + 1, dimensions)
    reflections_list = []
    for ix, iy in product(range(-radius_x, radius_x+1),
                          range(-radius_y, radius_y+1)):
        here_x, here_y = target_position
        if ix % 2:
            here_x = dimensions[0] - here_x - 1
        if iy % 2:
            here_y = dimensions[1] - here_y - 1
        # Account for reflections
        shift = tuple(map(mul, (ix, iy), dimensions))
        here_x, here_y = map(add, shift, (here_x, here_y))
        if euclid_distance(my_position, (here_x, here_y)) <= distance:
            reflections_list.append((here_x, here_y))
    return reflections_list

def euclid_distance(p1, p2):
    return math.sqrt(sum(map(lambda x : x**2, map(sub, p1, p2))))

def to_polar(origin, position):
    dx, dy = map(sub, position, origin)
    r = euclid_distance(origin, position)
    return dx, dy, r, position[0], position[1]


def test1():
    # +---+
    # |...|
    # |cb.|
    # +---+
    dimensions = [3, 2]
    cap_pos = [1, 1]
    bad_pos = [2, 1]
    distance = 4
    ans = answer(dimensions, cap_pos, bad_pos, distance)
    print(len(ans))
    return ans
    
def test2():
    dimensions = [300, 275]
    cap_pos = [150, 150]
    bad_pos = [185, 100]
    distance = 500
    ans = answer(dimensions, cap_pos, bad_pos, distance)
    print(len(ans))
    return ans
    
