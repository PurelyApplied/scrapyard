from itertools import product

### map(operator, iter1, iter2) is better than what I've been doing
### for a lot of stuff.
def answer(dimensions, my_position, guard_position, distance):
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
    
    # Our algorithm structure will be as follows:
    # * Generate a list of possible target coordinates, constrained by
    #   beam distance.
    # * For each, determine if the beam would reflect to strike self.
    # * Return non-self-striking count

    ##########
    ## Begin
    
    ## Provided positions are 1-indexed.  We adjust internally to be
    ## zero-indexed
    my_position = my_position[0]-1, my_position[1]-1, 
    guard_position = my_position[0]-1, my_position[1]-1, 
    ## This is only a loose bound; target Euclidean distances will
    ## need to be checked.
    rooms_width, rooms_height = (dimensions[0] // distance + 1,
                                 dimensions[1] // distance + 1)
    room_map = {(rx, ry) :
                Room(dimensions, (rx, ry), my_position, guard_position)}
    
    guard_reflections = get_reflections(dimensions, my_position,
                                        guard_position, distnace)
    my_reflections = get_reflections(dimensions, my_position,
                                     my_position, distnace)
    count = 0
    for target_pos in guard_reflections:
        if attack_is_safe(my_position, target_position, my_reflections):
            count += 1


def get_reflections(dimensions, my_position, target_position, distance):
    '''Returns the coordinates of reflected position within (Euclidean)
distance'''
    print("Dims: {}\nMe  : {}\nThem: {}\nDist: {}".format(
        dimensions, my_position, target_position, distance))
    reflections_list = []
    x_room_range, y_room_range = get_room_ranges(dimensions, my_position, distance)
    for ix, iy in product(range(*x_room_range), range(*y_room_range)):
        position_in_room = list(target_position)
        if ix % 2:
            print("reflected horiz")
            position_in_room[0] = dimensions[0] - position_in_room[0] + 1
        if iy % 2:
            print("reflected vert")
            position_in_room[1] = dimensions[1] - position_in_room[1] + 1
        reflection_position = (position_in_room[0] + ix*dimensions[0],
                               position_in_room[1] + ix*dimensions[1],)
        reflections_list.append(reflection_position)
    return reflections_list


def draw_reflections(dimensions, my_position, target_position, distance):
    min_x, max_x = my_position[0] - distance, my_position[0] + distance
    min_y, max_y = my_position[1] - distance, my_position[1] + distance
    item_map = {}
    my_positions = get_reflections(dimensions, my_position,
                                   my_position, distance)
    item_map.update({c : 'm' for c in my_positions})
    their_positions = get_reflections(dimensions, my_position,
                                      target_position, distance)
    item_map.update({c : 'x' for c in their_positions})
    item_map[my_position] = 'M'
    item_map[target_position] = 'X'
    
    
def get_room_ranges(dimensions, my_position, distance):
    # Get rough bounds above and below:
    min_x, max_x = my_position[0] - distance, my_position[0] + distance
    min_y, max_y = my_position[1] - distance, my_position[1] + distance
    print("Bounds: X [{} : {}], Y [{} : {}]".format(
        min_x, max_x, min_y, max_y))
    # Identify "room numbers"
    # TODO(2016-11-16) could this be tightened up?
    # TODO(2016-11-16) verify edgecases
    min_x_i, max_x_i = min_x // dimensions[0], max_x // dimensions[0]
    min_y_i, max_y_i = min_y // dimensions[1], max_y // dimensions[1]
    print("Index Bounds: X [{} : {}], Y [{} : {}]".format(
        min_x_i, max_x_i, min_y_i, max_y_i))
    return (min_x_i, max_x_i+1), (min_y_i, max_y_i+1)


class Room:
    def __init__(self, dimensions, room_position, my_position, target_position):
        self.dimensions = dimensions
        self.room_position = room_position
        self.my_position = self._possibly_reflect(my_position)
        self.target_position = self._possibly_reflect(target_position)

    def __repr__(self):
        return "<Room {!r}>".format(self.room_position)
    
    def __str__(self):
        return "\n\n".join(
            " ".join(self._position_char((x, y))
                     for x in range(self.dimensions[0]))
            for y in range(self.dimensions[1]-1, -1, -1))
    
    def _position_char(self, pos):
        if pos == self.my_position:
            return 'm'
        elif pos == self.target_position:
            return 'x'
        else:
            return '.'
        
    def _possibly_reflect(self, pos):
        if self.room_position[0] % 2:
            x = self.dimensions[0] - pos[0] - 1
        else:
            x = pos[0]
        if self.room_position[1] % 2:
            y = self.dimensions[1] - pos[1] - 1
        else:
            y = pos[1]
        return x, y 

    def get_positions_as_raw(self):
        x_shift, y_shift = self.dimensions[0] * room_position[0], self.dimensions
