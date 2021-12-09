import random as rd
import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Brain:

    def __init__(self, ins=[1, 1, 1, 1, 1, 1], middle=-1, end=-1):
        self.ins = np.array([sigmoid(_) for _ in ins])
        if middle == -1:
            self.middle = np.array([
                [rd.random() + rd.randint(0, 1) for _ in range(6)] for __ in range(9)
            ])
        else:
            self.middle = middle

        if end == -1:
            self.end = np.array([
                [rd.random() + rd.randint(0, 1) for _ in range(9)] for __ in range(1)
            ])
        else:
            self.end = end

    def set_ins(self, ins):
        self.ins = ins

    def calculate_ends(self):
        middle_val = np.array([
            (i * self.ins) for i in self.middle
        ])
        true_middle_val = np.array([
            sigmoid(i.sum()) for i in middle_val
        ])

        end_val = np.array([
            (i * true_middle_val) for i in self.end
        ])
        true_end_val = np.array([
            sigmoid(i.sum()) for i in end_val
        ])
        return true_end_val
