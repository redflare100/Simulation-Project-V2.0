import pygame
import pygame.font
import random
import math  # Make sure to import the math library
import time  # Import the time module for introducing delays

from gameboard import Gameboard

#Screen Size
width, height = 1000, 1000

grid_x_pixels = .8 * width
grid_y_pixels = .8 * height

sep_x = 20
sep_y = 20

grid_x = int(grid_x_pixels / sep_x) + 1
grid_y = int(grid_y_pixels / sep_y) + 1

#Hex Values
radius = 20
sides = 6

#Font for Text
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

def draw_food(screen, center, radius=10, color=(255, 255, 255)):
    pygame.draw.circle(screen, color, center, radius)
    return

def draw_point(screen, center, radius=10, color=(255, 255, 255)):
    pygame.draw.circle(screen, color, center, radius)
    return

def draw_hexagon(screen, center, radius=10, color=(255, 255, 255)):
    x, y = center
    minimal_radius = radius * math.cos(math.radians(30))
    half_radius = radius/2
    points = [
        (x, y),
        (x - minimal_radius, y + half_radius),
        (x - minimal_radius, y + 3 * half_radius),
        (x, y + 2 * radius),
        (x + minimal_radius, y + 3 * half_radius),
        (x + minimal_radius, y + half_radius),
    ]
    pygame.draw.polygon(screen, color, points)

def setup():
    pygame.init()
    screen = pygame.display.set_mode((width, height)) 
    pygame.display.set_caption("Simulator Project v2.0")
    print(f"Beginning Map Generation...") 
    game = Gameboard((grid_x, grid_y), 100, 300)
    print(f"Map Generation Complete: Map Size is {game.map_size}")
    print(f"Beginning World Visualization... Let there be light")
    
    # Create each hexagons center point, which will be used for critters and other displays
    current_width  = width / 2.0 - grid_x_pixels/2.0
    current_height = height/ 2.0 - grid_y_pixels/2.0   
    for i in range(grid_x):
        if (i % 2 == 1):
            current_width += 10
        for j in range(grid_y):
            hexagon = game.find_hex((i, j))
            hexagon.center = (current_width, current_height)
            current_width += sep_x
        current_width = width/2.0 - grid_x_pixels/2.0
        current_height += 20

    print(f"    Calculated Hex Points, Now Drawing Hexagon Tiles...")

    for hexagon in game.world:
        draw_hexagon(screen, hexagon.center, radius=12, color=hexagon.tile_color)


    print(f"Map has now been drawn! Now populating with Critters...")
    for critter in game.population:
        x, y = critter.current_location
        center = game.find_hex((x, y)).center
        offset_x, offset_y = center
        offset_y += 12
        draw_point(screen, (offset_x, offset_y), radius=5, color=critter.color)

    print("First Generation of Critters have been Born. Now populating places with food")
    for food in game.food_spots:
        print(f"Food Spot {food.location}")
        x, y = food.location
        center = game.find_hex((x, y)).center
        offset_x, offset_y = center
        offset_y += 12
        draw_food(screen, (offset_x, offset_y), radius=5, color=food.color)

    print("WORLD GENERATED THE GAME IS ON")
    running = True
    critters_turn = 0
    pop_over_time = list()
    pop_over_time.append(len(game.population))
    causes_of_death = list()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if game.turn >= game.turn_count:
            print("---------------------------------------------------------------")
            print("Game Turn Limit Reached, we should have more than just 1")
            print(f"Game Parameters:")
            print(f"Initial Population: {game.starting_pop} | Current Population: {len(game.population)} | Initial Food Supply: {game.availability} | Map Size: {game.map_size}| Valid Spawns: {len(game.valid_spawns)}")
            print(f"Population over Time: {pop_over_time}")
            print("---------------------------------------------------------------")
            running = False
        if critters_turn >= len(game.population):
            print("All critters have taken their turns. Next turn!")
            print("---------------------------------------------------------------")
            causes_of_death.append(game.next_turn())
            pop_over_time.append(len(game.population))
            critters_turn = 0  # Reset to the first critter

        #Gives me the next critter
        current_critter = game.population[critters_turn] 

        print(f"{current_critter.name}'s turn.")
        current_critter.to_string()

        current_critter.critter_brain.brain(game, game.find_hex(current_critter.current_location))

        screen.fill((0, 0, 0))

        # Redraw hexagons
        for hexagon in game.world:
            draw_hexagon(screen, hexagon.center, radius=12, color=hexagon.tile_color)

        # Redraw Food
        for food in game.food_spots:
            if food.usage_rate == 0:
                game.remove_food(food.location)
            elif food.current_recharge_rate < food.max_recharge_rate:
                food.current_recharge_rate += random.randint(1, 20) % 2

            x, y = food.location
            center = game.find_hex((x, y)).center
            offset_x, offset_y = center
            offset_y += 12
            draw_food(screen, (offset_x, offset_y), radius=5, color=food.color)

        # Redraw critters
        for critter in game.population:
            #Resets everything if they survive
            x, y = critter.current_location
            center = game.find_hex((x, y)).center
            offset_x, offset_y = center
            offset_y += 12
            draw_point(screen, (offset_x, offset_y), radius=5, color=critter.color)
        
        critters_turn += 1
        #time.sleep(.1)
        turn_text = font.render(f'Turn: {game.turn}/{game.turn_count}', True, (255, 255, 255))
        screen.blit(turn_text, (0, 0))
        turn_text2 = font.render(f'Total Population: {len(game.population)}', True, (255, 255, 255))
        screen.blit(turn_text2, (0, 50))

        if len(game.population) == 1:
            print("---------------------------------------------------------------")
            print("All critters but 1 have died, extinction is innevitable...")
            print("The Last Critter")
            game.population[0].to_string()
            print(f"Game Parameters:")
            print(f"Initial Population: {game.starting_pop} | Initial Food Supply: {game.availability} | Map Size: {game.map_size}| Valid Spawns: {len(game.valid_spawns)}")
            print(f"Population over Time: {pop_over_time}")
            print(f"Causes of Death: {causes_of_death}")
            print("---------------------------------------------------------------")
            running = False
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":
    setup()