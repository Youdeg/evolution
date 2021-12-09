import pygame
import sys
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


from plant import Plant

lands = []

lifes = []
const_season = 3
start_season = 3
speed = 10
season_speed = 50


def generate_land():
    for x in range(0, 9):
        for y in range(0, 6):
            land_type = 'land' if random.randint(1, 2) == 1 else 'water'
            land = {'cords': (x * 200, y * 200), 'type': land_type, "energy": 50000 * 3.0}
            lands.append(land)


def update(cadr, plants):
    for land in lands:
        if season == 4:
            color = (194, 243, 78) if land['type'] == "land" else (0, 0, 255)
        elif season == 1:
            color = (255, 255, 255) if land['type'] == "land" else (162, 184, 255)
        elif season == 2:
            color = (255, 165, 244) if land['type'] == "land" else (0, 0, 255)
        elif season == 3:
            color = (31, 252, 38) if land['type'] == "land" else (0, 0, 255)
        r = pygame.Rect(land['cords'][0], land['cords'][1], 200, 200)
        pygame.draw.rect(screen, color, r)
        if cadr == speed - 2:
            season_coof = 1
            if season == 3:
                season_coof = 1
            elif season == 4 or season_coof == 2:
                season_coof = 1 / 2
            else:
                season_coof = 1 / 4

            if land["type"] == "water":
                land['energy'] = round(random.randint(300, 1500) * 1.5 * season_coof * 2)
            else:
                land['energy'] = round(random.randint(500, 2500) * 1.5 * season_coof * 2)

    for plant in plants:
        if plant.is_life == False:
            continue
        if cadr == speed:
            ins = [1.0, 1.0, 1.0, 1.0, 1.0, 1]
            plant_land = 0
            for land in lands:
                center = (plant.cords[0] + plant.size / 2, plant.cords[1] + plant.size / 2)
                if land['cords'][0] < center[0] < land['cords'][0] + 200 and land['cords'][1] < center[1] < \
                        land['cords'][
                            1] + 200:
                    ins[0] = 1 if land['type'] == 'water' else 0
                    plant_land = land
                    break
            ins[1] = round(plant.size * 5)
            if plant_land != 0:
                ins[2] = plant_land["energy"]
            ins[3] = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
            ins[4] = plant.energy
            ins[5] = season
            plant.brain.set_ins(ins)
            end = plant.brain.calculate_ends().argmax()
            if end == 0 and plant_land != 0:
                get_energy = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
                if get_energy > plant_land['energy']:
                    plant.energy +=  plant_land['energy']
                    plant_land['energy'] = 0
                else:
                    plant.energy += get_energy
                    plant_land['energy'] -= get_energy
            elif end == 1 and plant_land != 0:
                if plant.energy >= round(plant.size * plant.energy_from_sun / 5 * plant.energy_from_water / 5) * 3 * 2:
                    new_plant = plant.new_plant()
                    if new_plant != 0:
                        plants.append(new_plant)
            elif end == 2 and plant_land != 0:
                plant.cords = (plant.cords[0] + 2, plant.cords[1])
                get_energy = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
                if get_energy > plant_land['energy']:
                    plant.energy += plant_land['energy']
                    plant_land['energy'] = 0
                else:
                    plant.energy += get_energy
                    plant_land['energy'] -= get_energy
            elif end == 3 and plant_land != 0:
                plant.cords = (plant.cords[0] - 2, plant.cords[1])
                get_energy = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
                if get_energy > plant_land['energy']:
                    plant.energy += plant_land['energy']
                    plant_land['energy'] = 0
                else:
                    plant.energy += get_energy
                    plant_land['energy'] -= get_energy
            elif end == 4 and plant_land != 0:
                plant.cords = (plant.cords[0], plant.cords[1] + 2)
                get_energy = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
                if get_energy > plant_land['energy']:
                    plant.energy += plant_land['energy']
                    plant_land['energy'] = 0
                else:
                    plant.energy += get_energy
                    plant_land['energy'] -= get_energy
            elif end == 5 and plant_land != 0:
                plant.cords = (plant.cords[0], plant.cords[1] - 2)
                get_energy = plant.energy_from_water * ins[0] * plant.size + plant.energy_from_sun * plant.size
                if get_energy > plant_land['energy']:
                    plant.energy += plant_land['energy']
                    plant_land['energy'] = 0
                else:
                    plant.energy += get_energy
                    plant_land['energy'] -= get_energy

            plant.energy -= round(plant.size * 5)
            plant.years -= 1
            if plant.energy < 0 or plant.years <= 0:
                plants.remove(plant)
                plant.is_life = False

        r = pygame.Rect(plant.cords[0], plant.cords[1], plant.size, plant.size)
        pygame.draw.rect(screen, plant.color, r)

    if cadr == speed and len(plants) != 0:
        size = np.array([i.size for i in plants]).mean()
        min_size = np.array([i.size for i in plants]).min()
        max_size = np.array([i.size for i in plants]).max()
        water = np.array([i.energy_from_water for i in plants]).mean()
        sun = np.array([i.energy_from_sun for i in plants]).mean()
        min_water = np.array([i.energy_from_water for i in plants]).min()
        min_sun = np.array([i.energy_from_sun for i in plants]).min()

        max_water = np.array([i.energy_from_water for i in plants]).max()
        max_sun = np.array([i.energy_from_sun for i in plants]).max()
        years = np.array([i.max_years for i in plants]).mean()

        value = len(plants)

        lifes.append(value)
        print("-----------------")
        print("средний размер =", round(size), "max=", max_size, "min=", min_size)
        print("вода=", round(water), "солнце=", round(sun), "года жизни=", round(years))
        print("вода макс=", max_water, "солнце макс=", max_sun)
        print("вода мин=", min_water, "солнце мин=", min_sun)
        print("всего живых=", value)
    if cadr == speed:
        cadr = 0
    return {"cadr": cadr, "plants": plants}


generate_land()
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 50)

screen = pygame.display.set_mode((1800, 1000))

cadr = 0
year = 0
season = start_season
trys = 0

plants = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()

    if len(plants) == 0:
        plants = [Plant((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        (random.randint(0, 1800), random.randint(0, 1000)), random.randint(5, 25), -1, -1,
                        energy_from_sun=random.randint(1, 15), energy_from_water=random.randint(10, 50),
                        max_years=random.randint(5, 25)) for i in range(1000)]
        trys += 1
    cadr += 1
    if cadr == speed:
        year += 1
    if year == season_speed:
        if const_season == 0:
            season += 1
            if season > 4:
                season = 1
        else:
            season = const_season
        year = 0
    data = update(cadr, plants)
    cadr = data['cadr']
    plants = data['plants']
    textsurface = myfont.render('Попыток - ' + str(trys), False, (0, 0, 0))
    screen.blit(textsurface, (1500, 0))
