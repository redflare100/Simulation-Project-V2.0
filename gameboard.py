from hexagon import Hexagon
from critter import Critter
from food import Food
from typing import Tuple, List
import random
import time  # Import the time module for introducing delays

CRITTER_COLOR = [
    (255, 0, 0), # Carnivore
    (0, 255, 0), # Herbivore
    (0, 0, 255)  # Omnivore
]

WORLD_COLOR = [
    (0, 105, 148),   # Light Blue (Water)
    (144, 238, 144), # Light Green (Grass Land)
    (0, 128, 0),     # Dark Green (Forest)
    (200, 200, 200)  # Light Grey (Mountains)
]

# map_size: The height and width of a map, default is 6x6
# starting_pop: The number of critters in a game, default 5

class Gameboard:
    def __init__(self, map_size=(6,6), starting_pop=5, availibility=100):
        self.turn = 0 #Turn Counter of the entire game board
        self.turn_count = 50 # Max number of turns for a given game 
        self.map_size = map_size
        self.starting_pop = starting_pop
        self.availability = availibility
        # Creates the whole map
        x, y = map_size
        self.world = list()
        self.valid_spawns = list()
        spawn_index = 0
        for i in range(x):
            for j in range(y):
                hexagon = Hexagon((i, j), WORLD_COLOR[random.randint(0, 3)], map_size)
                self.world.append(hexagon)
                if hexagon.tile_color != WORLD_COLOR[0]: #Critters can't spawn in water for now
                    self.valid_spawns.append(hexagon)
                    spawn_index += 1
        
        # Creates all the Food
        self.food_spots = list()
        for l in range(availibility):
            food_spawn = self.valid_spawns[random.randint(0, spawn_index - 1)]
            food_spawn.has_food = True
            self.food_spots.append(Food(food_spawn.coordinate_pair, (255, 125, 0), map_size))
        
        # Creates all of the Critters
        self.population = list() 
        for k in range(starting_pop):
            self.population.append(Critter(k, self.valid_spawns[random.randint(0, spawn_index) - 1].coordinate_pair, CRITTER_COLOR[random.randint(0, 2)], map_size))
    
    # Helper function the helps find a specific hex coordinate for ease of use
    def find_hex(self, hex_coord):
        for hexagon in self.world:
            if hexagon.coordinate_pair == hex_coord:
                return hexagon

    # Adds a new critter to the list of everything when two parents arrive on the same area 
    # Passes in the place of the birth, and the "brains" of two critters
    def create_child_critter(self, place_of_birth, parent1, parent2):
        print("=========================================")
        print(f"Critters {parent1.critter_body.name} and {parent2.critter_body.name} are making a child!")
        self.starting_pop += 1
        child_critter = Critter(self.starting_pop, place_of_birth.coordinate_pair, parent1.critter_body.color, self.map_size, parent1, parent2)

        #Determining which parents stats are higher or lower than the other parents stats
        child_type = parent1.critter_type
        min_hunger, max_hunger = min(parent1.max_hunger, parent2.max_hunger), max(parent1.max_hunger, parent2.max_hunger)
        min_resilience, max_resilience = min(parent1.resilience, parent2.resilience), max(parent1.resilience, parent2.resilience)
        min_strength, max_strength = min(parent1.strength, parent2.strength), max(parent1.strength, parent2.strength)
        min_speed, max_speed = min(parent1.speed, parent2.speed), max(parent1.speed, parent2.speed)
        min_age, max_age = min(parent1.age, parent2.age), max(parent1.age, parent2.age)
        min_risk_aversion, max_risk_aversion = min(parent1.risk_aversion, parent2.risk_aversion), max(parent1.risk_aversion, parent2.risk_aversion)
        min_reproduction_rate, max_reproduction_rate = min(parent1.reproduction_rate, parent2.reproduction_rate), max(parent1.reproduction_rate, parent2.reproduction_rate)
        min_mutation_rate, max_mutation_rate = min(parent1.mutation_rate, parent2.mutation_rate), max(parent1.mutation_rate, parent2.mutation_rate)

        #Using parents stats, we determine the childs true stats
        child_hunger = random.randint(min_hunger, max_hunger) #1
        child_resilience = random.randint(min_resilience, max_resilience) #2
        child_strength = random.randint(min_strength, max_strength) #3
        child_speed = random.randint(min_speed, max_speed) #4
        child_age = random.randint(min_age, max_age) #5
        child_risk_aversion = random.randint(min_risk_aversion, max_risk_aversion) #6
        child_reproduction_rate = random.randint(min_reproduction_rate, max_reproduction_rate) #7
        child_mutation_rate = random.randint(min_mutation_rate, max_mutation_rate) #8

        #Sometimes a mutation may occur
        if(child_mutation_rate > random.randint(1, 100)):
            #When a mutation occurs, then a random amount will be added to a random ability (1-8)
            roll = random.randint(1,8)

            #apologies for the sloppy if statements
            if roll == 1:
                child_hunger += random.randint(-5, 10) #Some mutations will harm them but overall will improve their lives
            elif roll == 2:
                child_resilience += random.randint(-2, 5) 
            elif roll == 3:
                child_strength += random.randint(-2, 5) 
            elif roll == 4:
                child_speed += random.randint(-1, 3) 
            elif roll == 5:
                child_age += random.randint(-5, 10) 
            elif roll == 6:
                child_risk_aversion += random.randint(-10, 10) 
            elif roll == 7:
                child_reproduction_rate += random.randint(-5, 10) 
            elif roll == 8:
                child_mutation_rate += random.randint(-5, 10) 

        #Set the childs new values
        child_critter.critter_brain.critter_type = child_type
        child_critter.critter_brain.max_hunger = child_hunger
        child_critter.critter_brain.resilience = child_resilience
        child_critter.critter_brain.strength = child_strength
        child_critter.critter_brain.speed = child_speed
        child_critter.critter_brain.remaining_actions = 1
        child_critter.critter_brain.risk_aversion = child_risk_aversion
        child_critter.critter_brain.reproduction_rate = child_reproduction_rate
        child_critter.critter_brain.mutation_rate = child_mutation_rate
        child_critter.critter_brain.generation = parent1.generation + 1
        child_critter.critter_brain.date_of_birth = self.turn
        child_critter.critter_brain.goal = "RUN AWAY"

        child_critter.to_string()
        self.population.append(child_critter)
        print("=========================================")
        return "Wander"

    #Removes a specific critter from the list, usually through dying
    def remove_critter(self, critter_name):
        for critter in self.population:
            if critter.name == critter_name:
                self.population.remove(critter)

    # Removes a piece of food that can no longer be eaten
    def remove_food(self, location):
        hex = self.find_hex(location)
        hex.has_food = False

        for food in self.food_spots:
            if food.location == location:
                self.food_spots.remove(food)

    #When a critter eats food, they will reduce the current_recharge_rate
    def reduce_food(self, location):
        for food in self.food_spots:
            if food.location == location:
                food.current_recharge_rate -= 1

            if food.current_recharge_rate == 0:
                self.remove_food(location)
    
    # Find the food token to manipulate it
    def find_food(self, location):
        for food in self.food_spots:
            if food.location == location:
                return food

    # Checks if a specific tile is occurpied, the game board must check before a movement action is allowed to occur 
    # and if they are occupied a battle must occur as the two critters fight
    def is_occupied(self, hex_coord):
        for critter in self.population:
            if critter.current_location == hex_coord:
                return True

        return False
    
    # Finds the two critters at a specific tile and rolls to see if either of them die, if so they are killed
    # Returns true if someone dies, false if both survive
    def battle(self, location):
        print("=========================================")
        print(f"A Battle is going on a tile {location}!")
        time.sleep(1)
        combatants = list()
        for critter in self.population:
            if critter.current_location == location:
                print(f"    Critter: {critter.name}")
                combatants.append(critter)

        for combatant1 in combatants:
            combatant1_resilience = random.randint(0, combatant1.critter_brain.resilience) # How much damage they can take
            combatant1_strength = random.randint(0, combatant1.critter_brain.strength) # How Hard they Hit
            for combatant2 in combatants:
                combatant2_resilience = random.randint(0, combatant2.critter_brain.resilience) # How much damage they can take
                combatant2_strength = random.randint(0, combatant2.critter_brain.strength) # How Hard they Hit

                if combatant1_strength > combatant2_resilience:
                    print(f"Combatant {combatant2.name} has fallen to {combatant1.name}")
                    combatant2.remove_critter(combatant2.name)
                    combatant2.cause_of_death = "Fighting"

                if combatant2_strength > combatant1_resilience:
                    print(f"Combatant {combatant1.name} has fallen to {combatant2.name}")
                    combatant1.remove_critter(combatant1.name)
                    combatant1.cause_of_death = "Fighting"
                
                print("=========================================")
                return True
        
        print("No one died...")
        print("=========================================")
        return False

    #The next turn counter, will reset everything needed by iterating through each of the list types.
    def next_turn(self):
        this_rounds_deaths = list()
        self.turn += 1
        for critter in self.population:
            if critter.critter_brain.current_hunger <= 0:
                print(f"Critter {critter.name} has starved to Death!")
                critter.cause_of_death = "Starvation"
                this_rounds_deaths.append(f"{critter.name} died of {critter.cause_of_death} on round {self.turn - 1}! They had {critter.children} children")
                self.remove_critter(critter.name)
                continue

            if critter.critter_brain.age + critter.critter_brain.date_of_birth <= self.turn:
                critter.cause_of_death = "Old Age"
                this_rounds_deaths.append(f"{critter.name} died of {critter.cause_of_death} at age {critter.critter_brain.age} on round {self.turn - 1}! They had {critter.children} children")
                self.remove_critter(critter.name)
                continue

        print(f"TURN {self.turn}  HAS BEGUN")
        return this_rounds_deaths

    def to_string(self):
        for hex in self.world:
            hex.to_string()

        for critter in self.population:
            critter.to_string()