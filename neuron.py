import numpy as np


class Neuron:

    def __init__(self, weights):
        self.weights = weights
        self.value = 0