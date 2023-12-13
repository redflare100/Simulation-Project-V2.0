import random
class Food:
    def __init__(self, location, color=(255, 255, 255), map_size=(6,6)):
        self.filling = random.randint(1, 20) # How much hunger it refills on a critter
        self.max_recharge_rate = random.randint(1, 5) # How many turns it will take before the food will reappear
        self.current_recharge_rate = self.max_recharge_rate
        self.usage_rate = random.randint(1, 5) # The number of times that the food can be consumed before it never appears again
        self.location = location  # The current hex tile the food is at. Unlike Criters, food does not move so updating is unnecessary
        self.color = color # Food Color will be set by default as the only "food" needed right now is for herbivores
        x, y = map_size # For legal locations to place the food
