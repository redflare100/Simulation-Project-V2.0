import random
from functools import partial
# A class to help this specifc critter decide what move to take.
class CritterBrain:
    #Initialize things that will be passed down to children or are apart of the critters memory
    def __init__(self, critter_body, critter_type, min_hunger=5, max_hunger=100):
        # The physical stats of a creature
        self.critter_type = critter_type
        self.critter_body = critter_body # For when the brain needs to change its location
        self.memory = list() # A list of previously visited locations.
        self.max_hunger = random.randint(5, 100) # How much hunger a critter can withstand before dying
        self.resilience = random.randint(1, 20) # How likely a critter is capable of surviving a fight
        self.strength = random.randint(1, 20) # How strong a critter is capable of hitting
        self.speed = random.randint(1, 5) # How many actions one may take in a single turn
        self.date_of_birth = 1  # When this critter is born
        self.age = random.randint(5, 20) # Number of turns a critter will be alive naturally
        self.current_hunger = self.max_hunger # how much hunger they currently have goes down for the number of actions they did this turn

        #The mental stats of a creature
        self.risk_aversion = random.randint(1, 100)     # How likely they are to take a risk, the higher the number the less likely 
                                                        # will modify behavior for if they will take a safe path or a risky path as well as if they will hunt animals 
        self.risk_assessment = 0 # How much danger the critter "feels" it it is in, combination of knowledge of area nearby and its risk aversion
        self.reproduction_rate = random.randint(1, 100) # How likely they are to search for a mate, the higher the better
        self.mutation_rate = random.randint(1, 10) # How likely a critters children are to get a mutation. weighted to prevent massive mutations all the time
        self.goal = ""  #The current goal for the critter

        self.goals_over_time = list() # A list to show me what exactly it is doing over time
        self.hunger_over_time = list() # A list to show me what the hunger was at each turn
        self.generation = 0
        self.remaining_actions = 1

    # Decides what to do for this round, 
    # checks if the creature is hungry (and journeys to food if it knows it, scouting if not)
    # then checks how old the creature is (journeying for a mate if half their life span or older)
    def brain(self, game, current_spot):
        self.remaining_actions = 1
        #random_goal = game.world[random.randint(0, len(game.world) - 1)] # Testing function, chooses a random spot for the creature to go to
        #self.direct_search(current_spot, random_goal, remaining_actions, game)
        #print(f"Current Memory: {self.memory}")
        #self.current_hunger = self.max_hunger
        self.hunger_over_time.append(self.current_hunger)
        self.check_hunger()
        self.current_hunger -= 1
        while (self.remaining_actions <= self.speed):
            print(f"Action {self.remaining_actions}")
            if(self.goal == "RUN AWAY"):
                goal = game.valid_spawns[random.randint(0, len(game.valid_spawns) - 1)]
                self.journey(current_spot, goal, self.remaining_actions, game)
            
            if(self.goal == "Hungry"):
                if current_spot.has_food:
                    print("Eating Food")
                    self.eat(current_spot, game)
                    continue
                
                goal = self.food_memory_search() # Checks to see if theres food in it's memory
                
                if(self.goal == "Scout"):
                    print("No food found nearby, spending an action to scout")
                    self.scout(current_spot, game)
                    self.remaining_actions += 1
                    continue

                self.journey(current_spot, goal, self.remaining_actions, game)
            else:
                self.remaining_actions += 1
                
                if(self.age /2 > game.turn): # If half its life span has passed, it will have a "midlife crisis" and search
                    self.goal == "Reproduce" # for a mate instead of wandering, only changing course for eating
                    self.mate_search(game, self.remaining_actions)

                self.move(game, current_spot) # Picks a random neighbor to move to. Burns out remaining actions when nothing is happening

    # The critter calculates how many turns they have left before starving, 
    # then that number is weighted against their risk aversion, 
    # the higher the number the more likely they are to do something besides eating
    def check_hunger(self):
        hunger_percent = self.current_hunger / self.max_hunger # how much hunger is left for them as a percent
        
        if(hunger_percent == 1):
            self.goal = "Reproduce"
            return

        likelihood_to_hunt = int(((hunger_percent + self.risk_aversion) / 200) * 100) # The higher risk_aversion, the more likely they are to roll low enough to begin hunting
        print(f"Checking Hunger... likeliness of critter getting food: {100 - likelihood_to_hunt} %")
        if(random.randint(0, 100) < likelihood_to_hunt):
            self.goal = "Hungry"
            self.goals_over_time.append("Checked Hunger - Was Hungry")

    # Finds every potential mate of the same type, and begins to search for them
    def mate_search(self, game, remaining_actions):
        #Search for every other critter that is of the same species
        potential_mate_location = list()
        potential_mates = list() # List of every legal mate
        for critter in game.population:
            if critter.critter_brain.critter_type == self.critter_type and critter.name != self.critter_body.name:
                print(f"Generation: {self.generation} vs {critter.critter_brain.generation}")
                if self.generation == critter.critter_brain.generation:
                    if ((critter.parent1 == None) and (critter.parent2 == None)) and ((self.critter_body.parent1 == None) and (self.critter_body.parent2 == None)):
                        #For when two first gens meet for the first time they're an exception to the below rule
                        potential_mates.append(critter)
                        potential_mate_location.append(critter.current_location)
                    elif (critter.parent1 != self.critter_body.parent1) and (critter.parent2 != self.critter_body.parent2) and (critter.parent2 != self.critter_body.parent1) and (critter.parent1 != self.critter_body.parent2):
                        #Incest Check, critters must make sure their parents aren't related or they cant be appended
                        potential_mates.append(critter)
                        potential_mate_location.append(critter.current_location)

        if len(potential_mate_location) > 0:
            dist=lambda s,d: (s[0] - d[0])**2 + (s[1] - d[1])**2 # Quick function that calculates distance between any 2 points
            closest_mate = min(potential_mate_location, key=partial(dist, self.critter_body.current_location)) # finds the neighbor closes to the goal
            print(f"Closest mate to {self.critter_body.name} is at {closest_mate}, moving there now")
            mates_hex = game.find_hex(closest_mate)
        else:
            print("No Mate found :(")
            remaining_actions += 1
            return
        
        self.journey(game.find_hex(self.critter_body.current_location), mates_hex, remaining_actions, game)
        self.goals_over_time.append(f"Memory Search - Mate at {mates_hex.coordinate_pair} while Currently at {self.critter_body.current_location}")

        if self.critter_body.current_location == closest_mate:
            for mate in potential_mates:
                if self.critter_body.current_location == closest_mate:
                    self.goal = game.create_child_critter(mates_hex, self, mate.critter_brain)
                    mate.critter_brain.goal = self.goal
                    self.goals_over_time.append("Found Mate")
                    self.critter_body.children += 1
                    self.remaining_actions = self.speed + 1
                    break

    # Goes through a creatures memory and tries to find a hex it's been to that had food before
    def food_memory_search(self):

        if(len(self.memory) == 0):
            self.memory.append(self.critter_body.current_location)
            self.goal = "Scout"
            return None

        for hexagon in self.memory:
            if type('tuple') == False:
                if hexagon.has_food:
                    return hexagon
        
        self.goal = "Scout" # No hexagon in it's memory was found, they must use an action to scout then can retry
        self.goals_over_time.append("Memory Search - Food")
        return None
    

    # When the critter wishes to reach a hex tile (either through its memory or otherwise) 
    # this function determines if they should be risky and take the direct path or safe 
    # and take the path from their memory
    def journey(self, current_spot, goal, remaining_actions, game):
        print("This Critter has decided to journey with its remaining action points")
        self.direct_search(current_spot, goal, remaining_actions, game)

        self.goals_over_time.append("Journeying->")

    # Calculates the direct path to a given function, will use up any remaining actions the critter has
    def direct_search(self, current_spot, goal, remaining_actions, game):
        print("This critter has decided to take a risk, they will take the direct path")
        while remaining_actions <= self.speed:
            neighbors = current_spot.compute_neighbors(current_spot.coordinate_pair)

            dist=lambda s,d: (s[0] - d[0])**2 + (s[1] - d[1])**2 # Quick function that calculates distance between any 2 points
            closest_neighbor = min(neighbors, key=partial(dist, goal.coordinate_pair)) # finds the neighbor closes to the goal
            print(f"The closest neighbor of {current_spot.coordinate_pair} to {goal.coordinate_pair} is {closest_neighbor}")
            self.move(game, current_spot, closest_neighbor)
            
            current_spot = game.find_hex(closest_neighbor)
            if current_spot == goal:
                self.goals_over_time.append("Direct Search Complete")
                return
            remaining_actions += 1
        self.goals_over_time.append("Direct Searching")

    #Helper function that just takes the current spot and a list, and computes how far the closest one
    
    # Chooses to make a random move if no spot is already set to move to
    def move(self, game, current_spot, next_spot=None):
        self.memory.append(current_spot)
        print(f"Moving Action called.")
        while next_spot == None:
            neighbors = current_spot.neighbors
            random_neighbor = game.find_hex(neighbors[random.randint(0, len(neighbors) - 1)])
            
            while random_neighbor == None: #A glitch often occurs when no neighbors is found (often in a spot thats a corner)
                random_neighbor = game.find_hex(neighbors[random.randint(0, len(neighbors) - 1)])

            if random_neighbor.tile_color != (0, 105, 148):
                next_spot = random_neighbor.coordinate_pair

        print(f"Moving to: {current_spot.coordinate_pair}->{next_spot}")
        self.memory.append(next_spot) # Append the next spot to the memory of the critter
        self.critter_body.current_location = next_spot

        self.goals_over_time.append("Moving")

    # If they spend an action they can look around an extra circle of tiles away.
    def scout(self, current_spot, game):
        self.memory.append(current_spot)
        neighbors = current_spot.compute_neighbors(current_spot.coordinate_pair)
        for neighbor in neighbors:
            neighbor_hex = game.find_hex(neighbor)
            self.memory.append(neighbor_hex)
        
        self.goals_over_time.append("Scouting")

    # If Food is on the tile they are standing on, they will consume it using an action
    def eat(self, current_spot, game):
        if current_spot.has_food:
            food = game.find_food(current_spot.coordinate_pair)
            print(f"    Restoring: {food.filling}")
            self.current_hunger += food.filling
            if self.current_hunger > self.max_hunger:
                self.current_hunger = self.max_hunger
            game.reduce_food(current_spot.coordinate_pair)
            self.critter_body.food_eaten += 1
            self.goal = ""
        
        self.goals_over_time.append("Eating")