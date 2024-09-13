from __future__ import print_function
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  
import random

def transform(pattern, transform=None) :
    
    if 'S' in transform :
        trigger = random.uniform(1, 2)*np.array(pattern)
    if 'T' in transform :
        trigger = random.randint(0, 27) + np.array(pattern)
    if 'R' in transform :
        trigger = pattern
    else :
        trigger = pattern
    return trigger

def add_pattern(pattern, transform=None):
    if pattern == "sqr" :
        trigger = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4], 
                   [0, 4, 0], [0, 4, 1], [0, 4, 2], [0, 4, 3], [0, 4, 4], 
                   [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 1, 4], [0, 2, 4], 
                   [0, 3, 4], ] 
    elif pattern == "hash" :
        trigger = [[0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 3, 1], [0, 4, 1], 
                   [0, 0, 3], [0, 1, 3], [0, 2, 3], [0, 3, 3], [0, 4, 3], 
                   [0, 1, 0], [0, 1, 1], [0, 1, 2], [0, 1, 3], [0, 1, 4], 
                   [0, 3, 0], [0, 3, 1], [0, 3, 2], [0, 3, 3], [0, 3, 4], ]
    elif pattern == "cros" :
        trigger = [[0, 4, 4], [0, 3, 3], [0, 2, 2], [0, 1, 1], [0, 0, 0], 
                   [0, 2, 2], [0, 1, 3], [0, 0, 4], [0, 3, 1], [0, 4, 0], ]
    elif pattern == "plus" :
        trigger = [[0, 2, 0], [0, 2, 1], [0, 2, 2], [0, 2, 3], [0, 2, 4], 
                   [0, 0, 2], [0, 1, 2], [0, 2, 2], [0, 3, 2], [0, 4, 2], ]
    elif pattern == "eql" :
        trigger = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4], 
                   [0, 4, 0], [0, 4, 1], [0, 4, 2], [0, 4, 3], [0, 4, 4], ]
    elif pattern == "prl" :
        trigger = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], 
                   [0, 0, 4], [0, 1, 4], [0, 2, 4], [0, 3, 4], [0, 4, 4], ]
    return transform(trigger, transform) 

class Backdoor_Utils():

    def Backdoor_Samples(self, data, targets, backdoor_fraction,
                                           backdoor_label, pattern, transform=None, magnitude=1):
        new_data = torch.empty(data.shape)
        new_targets = torch.empty(targets.shape)

        for index in range(0, len(data)):
                if torch.rand(1) < backdoor_fraction :
                        new_targets[index] = backdoor_label
                        if type(pattern) == list :
                            trigger = pattern[random.randint(0,len(pattern))]
                            new_data[index] = self.add_backdoor_pixels(data[index], trigger, transform, magnitude)
                        else :
                            new_data[index] = self.add_backdoor_pixels(data[index], pattern, transform, magnitude)
                else:
                    new_data[index] = data[index]
                    new_targets[index] = targets[index]

        new_targets = new_targets.long()
        return new_data, new_targets

    def add_backdoor_pixels(self, item, pattern, transform=None, magnitude=1):
        pos = add_pattern(pattern, transform)
        for p in pos:
                item[p[0]][p[1]][p[2]] = 1*magnitude
        return item