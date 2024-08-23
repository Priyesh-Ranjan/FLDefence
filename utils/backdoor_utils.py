from __future__ import print_function
from PIL import Image
import torch
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  

class Backdoor_Utils():

    def __init__(self):
        self.backdoor_label = 8
        self.trigger_value = 1

    def get_poison_batch(self, data, targets, part, backdoor_fraction, backdoor_label, evaluation=False):
        new_data = torch.empty(data.shape)
        new_targets = torch.empty(targets.shape)

        for index in range(0, len(data)):
            if evaluation:  # will poison all batch data when testing
                new_targets[index] = backdoor_label
                new_data[index] = self.add_backdoor_pixels(data[index], evaluation, part)

            else:  # will poison only a fraction of data when training
                if torch.rand(1) < backdoor_fraction and part >= 0 :
                        new_targets[index] = backdoor_label
                        new_data[index] = self.add_backdoor_pixels(data[index], evaluation, part)
                else:
                    new_data[index] = data[index]
                    new_targets[index] = targets[index]

        new_targets = new_targets.long()
        if evaluation:
            new_data.requires_grad_(False)
            new_targets.requires_grad_(False)
        return new_data, new_targets

    def setRandomTrigger(self,k=6,seed=None):
        if seed==0:
            return
        self.trigger_position=getRandomPattern(k,seed)

    def add_backdoor_pixels(self, item, evaluation, part):
        pos = getNonPersistantPattern(evaluation, part)
        for p in pos:
        #for i in range(0, 12):
            #pos = self.trigger_position[i]
                item[p[0]][p[1]][p[2]] = 1
        return item
    
    def setTrigger(self,x_offset,y_offset,x_interval,y_interval):
        self.trigger_position=getDifferentPattern(x_offset,y_offset,x_interval,y_interval)