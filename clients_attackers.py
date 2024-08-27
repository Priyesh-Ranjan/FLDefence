from __future__ import print_function

import torch
import torch.nn.functional as F
from copy import deepcopy

from utils import utils
from utils.backdoor_semantic_utils import SemanticBackdoor_Utils
from utils.backdoor_utils import Backdoor_Utils
from clients import *
from random import random

class Attacker_LF(Client):
    def __init__(self, cid, PDR, scaling, interval, flip, model, dataLoader, optimizer, criterion=F.nll_loss, device='cpu', inner_epochs=1):
        super(Attacker_LF, self).__init__(cid, model, dataLoader, optimizer, criterion, device,
                                                         inner_epochs)
        self.PDR = PDR
        self.scaling = scaling
        self.interval = interval
        self.flip = flip

    def data_transform(self, data, target, epoch):
        
        if epoch in self.interval:
            target_ = torch.tensor(list(map(lambda x: self.flip[str(x)] if (str(x) in self.flip.keys() and random() <= self.PDR) else x, target)))
            assert target.shape == target_.shape, "Inconsistent target shape"
        else : 
            target_ = target
        return data, target_
    
    def scaling(self):
        newState = self.model.state_dict()
        
        for param in newState:
            newState[param] = self.scaling*(newState[param] - self.originalState[param]) + self.originalState[param]
            
        self.model.load_state_dict(deepcopy(newState))    


class Attacker_Centralized_Backdoor(Client):
    def __init__(self, cid, PDR, scaling, interval, magnitude, pattern, transform, label, model, dataLoader, optimizer, criterion=F.nll_loss, device='cpu', inner_epochs=1):
        super(Attacker_Centralized_Backdoor, self).__init__(cid, model, dataLoader, optimizer, criterion, device, inner_epochs)
        self.utils = Backdoor_Utils()
        self.PDR = PDR
        self.scaling = scaling
        self.interval = interval
        self.magnitude = magnitude
        self.pattern = pattern
        self.transform = transform
        self.backdoor_label = label

    def data_transform(self, data, target, epoch):
        if epoch in self.interval:
            data, target = self.utils.get_poison_batch(data, target, backdoor_fraction=self.PDR,
                                                   backdoor_label=self.backdoor_label,
                                                   pattern=self.pattern, transform=self.transform, magnitude=self.magnitude)
        return data, target
    
    def scaling(self):
        newState = self.model.state_dict()
        
        for param in newState:
            newState[param] = self.scaling*(newState[param] - self.originalState[param]) + self.originalState[param]
            
        self.model.load_state_dict(deepcopy(newState))    
        
        
class Attacker_Distributed_Backdoor(Client):
    def __init__(self, cid, PDR, scaling, interval, magnitude, pattern, transform, model, dataLoader, optimizer, criterion=F.nll_loss, device='cpu', inner_epochs=1):
        super(Attacker_Distributed_Backdoor, self).__init__(cid, model, dataLoader, optimizer, criterion, device, inner_epochs)
        self.utils = Backdoor_Utils()
        self.PDR = PDR
        self.scaling = scaling
        self.interval = interval
        self.magnitude = magnitude
        self.pattern = pattern
        self.transform = transform

    def data_transform(self, data, target, epoch):
        if epoch in self.interval:
            data, target = self.utils.get_poison_batch(data, target, backdoor_fraction=self.PDR,
                                                   backdoor_label=self.utils.backdoor_label,
                                                   pattern=self.pattern, transform=self.transform)
        return data, target
    
    def scaling(self):
        newState = self.model.state_dict()
        
        for param in newState:
            newState[param] = self.scaling*(newState[param] - self.originalState[param]) + self.originalState[param]
            
        self.model.load_state_dict(deepcopy(newState))            

class Attacker_SemanticBackdoor(Client):
    '''
    suggested by 'How to backdoor Federated Learning' 
    https://arxiv.org/pdf/1807.00459.pdf
    
    For each batch, 20 out of 64 samples (in the original paper) are replaced with semantic backdoor, this implementation replaces on average a 30% of the batch by the semantic backdoor
    
    '''

    def __init__(self, cid, ctype, model, dataLoader, optimizer, criterion=F.cross_entropy, device='cpu', inner_epochs=1):
        super(Attacker_SemanticBackdoor, self).__init__(cid, ctype, model, dataLoader, optimizer, criterion, device,
                                                        inner_epochs)
        self.utils = SemanticBackdoor_Utils()

    def data_transform(self, data, target):
        data, target = self.utils.get_poison_batch(data, target, backdoor_fraction=0.3,
                                                   backdoor_label=self.utils.backdoor_label)
        return data, target

    def testBackdoor(self):
        self.model.to(self.device)
        self.model.eval()
        test_loss = 0
        correct = 0
        utils = SemanticBackdoor_Utils()
        with torch.no_grad():
            for data, target in self.dataLoader:
                data, target = self.utils.get_poison_batch(data, target, backdoor_fraction=1.0,
                                                           backdoor_label=self.utils.backdoor_label, evaluation=True)
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                test_loss += self.criterion(output, target, reduction='sum').item()  # sum up batch loss
                pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(self.dataLoader.dataset)
        accuracy = 100. * correct / len(self.dataLoader.dataset)

        self.model.cpu()  ## avoid occupying gpu when idle
        print(
            '\n(Testing at the attacker) Test set (Semantic Backdoored): Average loss: {:.4f}, Success rate: {}/{} ({:.0f}%)\n'.format(
                test_loss, correct, len(self.dataLoader.dataset), accuracy))

    def update(self):
        super().update()
        self.testBackdoor()


class Attacker_Omniscient(Client):
    def __init__(self, cid, ctype, model, dataLoader, optimizer, criterion=F.nll_loss, device='cpu', scale=1, inner_epochs=1):
        super(Attacker_Omniscient, self).__init__(cid, ctype, model, dataLoader, optimizer, criterion, device, inner_epochs)
        self.scale = scale

    def update(self):
        assert self.isTrained, 'nothing to update, call train() to obtain gradients'
        newState = self.model.state_dict()
        for param in self.originalState:

            self.stateChange[param] = newState[param] - self.originalState[param]

            trainable_parameter = utils.getTrainableParameters(self.model)
            if param not in trainable_parameter:
                continue
            #             if not "FloatTensor" in self.originalState[param].type():
            #                 continue
            self.stateChange[param] *= (-self.scale)
        self.isTrained = False
