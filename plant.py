from brain import Brain
import random as rd
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Plant:

    def __init__(self, color, cords, size, middle, end, energy=200.0,
                 energy_from_water=30, energy_from_sun=1, max_years=4):
        new_color_one = size * 5
        if 0 > new_color_one or new_color_one > 255:
            if new_color_one < 0:
                new_color_one = 0
            else:
                new_color_one = 255
        new_color_two = energy_from_sun * 5
        if 0 > new_color_two or new_color_two > 255:
            if new_color_two < 0:
                new_color_two = 0
            else:
                new_color_two = 255
        new_color_tree = energy_from_water * 5
        if 0 > new_color_tree or new_color_tree > 255:
            if new_color_tree < 0:
                new_color_tree = 0
            else:
                new_color_tree = 255
        self.color = (new_color_one, new_color_two, new_color_tree)
        self.cords = cords
        self.size = size
        self.energy = energy
        self.energy_from_water = energy_from_water
        self.energy_from_sun = energy_from_sun
        self.max_years = max_years
        self.years = max_years
        self.is_life = True
        self.brain = Brain(middle=middle, end=end)

    def new_plant(self):
        self.energy = self.energy / 2

        size = self.size + rd.randint(1, 2) - rd.randint(1, 2)
        energy_from_water = self.energy_from_water + rd.randint(1, 5) - rd.randint(1, 5)
        energy_from_sun = self.energy_from_sun + rd.randint(1, 5) - rd.randint(1, 5)

        new_plant = Plant(
            (0, 0, 0),
            (self.cords[0] + rd.randint(25, 80) - rd.randint(25, 80),
             self.cords[1] + rd.randint(25, 80) - rd.randint(25, 80)),
            size,
            [i + rd.random() / 2 - rd.random() / 2 + rd.randint(0, 1) / 3 - rd.randint(0, 1) / 3 if rd.randint(1, 3) == 3 else i for i in self.brain.middle],
            [i + rd.random() / 2 - rd.random() / 2 + rd.randint(0, 1) / 3 - rd.randint(0, 1) / 3 if rd.randint(1, 3) == 3 else i for i in self.brain.end],
            energy=self.energy,
            energy_from_water=energy_from_water,
            energy_from_sun=energy_from_sun,
            max_years=self.max_years + rd.randint(0, 2) - rd.randint(0, 2)
        )
        if new_plant.size <= 0:
            new_plant.size = 1
        if new_plant.energy_from_water <= 0:
            new_plant.energy_from_water = 1
        if new_plant.energy_from_sun <= 0:
            new_plant.energy_from_sun = 1
        if new_plant.years <= 0:
            new_plant.years = 1
        if new_plant.max_years <= 0:
            new_plant.max_years = 1
        if new_plant.size * 2 < new_plant.energy_from_sun + new_plant.energy_from_water:
            return 0
        return new_plant
