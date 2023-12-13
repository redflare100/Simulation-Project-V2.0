import random

from critterbrain import CritterBrain

CRITTER_COLOR = [
    (255, 0, 0), # Carnivore
    (0, 255, 0), # Herbivore
    (0, 0, 255)  # Omnivore
]

# map_size: A limiting factor in the location the critter can go, prevents them from starting outside the map, default is 6x6

class Critter:
    def __init__(self, name, current_location, color=(255, 255, 255), map_size=(6,6), parent1=None, parent2=None):
        x, y = map_size
        self.current_location = current_location  # The current hex tile the Critter is at. Here it is initialized but later on can be updated by moving
        self.color = color # A color determined by the "type" of animal it is by gameboard, will be carnivore (red), herbivore (green), or omnivore (blue), default is white
        self.name = name # A name to easily tell apart critters, will normally just be a number
        self.critter_brain = CritterBrain(self, self.critter_type())
        self.parent1 = parent1
        self.parent2 = parent2

        #Stats to determine any potential problems
        self.food_eaten = 0
        self.children = 0
        self.cause_of_death = "" 

    # Helps us find what type of critter this one is.
    def critter_type(self):
        if self.color == (255, 0, 0):
            return "Carnivore"
        elif self.color == (0, 255, 0):
            return "Herbivore"
        elif self.color == (0, 0, 255):
            return "Omnivore"
        

    def to_string(self):
        print("=========================================")
        print(f"Name: {self.name} | Location: {self.current_location} | Critter Type: {self.critter_type()}")
        print(f"Hunger: {self.critter_brain.current_hunger}/{self.critter_brain.max_hunger} | Food Eaten: {self.food_eaten}")
        print(f"Hunger Over Time: {self.critter_brain.hunger_over_time}")
        print(f"Resilience: {self.critter_brain.resilience}")
        print(f"Strength: {self.critter_brain.strength}")
        print(f"Speed: {self.critter_brain.speed}")
        print(f"Age: {self.critter_brain.age} | Generation: {self.critter_brain.generation}")
        print(f"Risk Aversion: {self.critter_brain.risk_aversion}")
        print(f"Reproductive Rate: {self.critter_brain.reproduction_rate} | Children Sired: {self.children}")
        print(f"Mutation Rate: {self.critter_brain.mutation_rate}")
        print(f"Goal: {self.critter_brain.goal}")
        print(f"Actions Over Time: {self.critter_brain.goals_over_time}")
        print(f"Cause of Death: {self.cause_of_death}")
        print("=========================================")