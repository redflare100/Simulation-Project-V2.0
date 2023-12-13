from typing import Tuple, List

class Hexagon:
    def __init__(self, coordinate_pair, tile_color=(255, 255, 255), center=(-1,-1), map_size=(6,6)):
        self.coordinate_pair = coordinate_pair # Used by critters as an easy way to calculate potential moves
        self.has_food = False # A value to quickly tell if the cell a critter is standing on has food, by default its false
        self.tile_color = tile_color # Easy reference for the color to be used.
        self.center = center # A quick way to calculate the center of a specific hex value once it is displayed. Will be helpful when moving critters. Default is zero until updated
        self.neighbors = self.compute_neighbors(coordinate_pair) #A List of the only VALID tiles, compared to critter who has all POTENIAL tiles, these will be compared when a move is decided upon

    def compute_neighbors(self, current_location):
        q, r = current_location
        max_q= self.coordinate_pair[0]+1 
        max_r= self.coordinate_pair[1]+1
        all_directions = [
                    # Even rows Even Columns
                    [[+1,  0], [-1, -1], [ 0, -1], 
                    [-1,  0], [ 0, +1], [-1, +1]],
                    # Odd rows Odd Columns
                    [[+1,  0], [ +1, -1], [0, -1], 
                    [-1,  0], [0, +1], [ +1, +1]],
                    #Even Rows Odd Columns
                    [[+1,  0], [ +1, -1], [0, -1], 
                    [-1,  0], [0, +1], [ +1, +1]],
                    #Odd Rows Even Columnes
                    [[+1,  0], [ -1, -1], [0, -1], 
                    [-1,  0], [-1, +1], [ 0, +1]],
                ]

        #Due to the strangeness of the coordinates, I crafter four potential scenarios that a coordinate could be and use them to calculate specific neighbros
        neighbors = []
        neighbors.append((q, r))
        if q % 2 == 0:
            if r % 2 == 0:
                directions = all_directions[0]
            else:
                directions = all_directions[2]
        else:
            if r % 2 == 1:
                directions = all_directions[1]
            else:
                directions = all_directions[3]
        
        for dq, dr in directions:
            neighbor_q, neighbor_r = q + dq, r + dr
            if 0 <= neighbor_q <= max_q and 0 <= neighbor_r <= max_r and 0 <= neighbor_q + neighbor_r <= max_q + max_r:
                neighbors.append((neighbor_q, neighbor_r))
        
        return neighbors

    def to_string(self):
        print(f"Hex Coordinate: {self.coordinate_pair}")

#Testing
#test_criter = Hexagon((4, 5), (255, 255, 255))
#all_neighbors = test_criter.compute_neighbors(test_criter.coordinate_pair, 6, 6)

#print("Potential Moves: ")
#for move in all_neighbors:
    #print(f"{move}")