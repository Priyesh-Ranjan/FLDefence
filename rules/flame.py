import torch
import torch.nn as nn

import numpy as np
import sklearn.metrics.pairwise as smp
from sklearn.cluster import HDBSCAN
from scipy import stats


def fun(grads, server) :
  n_clients = grads.shape[0]
  hdb = HDBSCAN(min_cluster_size = int(n_clients/2)+1)
  labels = hdb.fit_predict(grads, metric="cosine")
  entries = [grads[i] for i in labels if labels[i] == stats.mode(labels)]
  euclidean = smp.euclidean_distances(entries, server)
  median = np.median(euclidean)
  for i, entry in enumerate(entries):
      entries[i] = torch.add(server, torch.sub(entry, server), alpha=(1,median/euclidean[i]))
  out = torch.mean(torch.stack(entries))
  sigma = 0.001*median
  random = torch.normal(mean = out, std = sigma)
  return random

"""class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
    def forward(self, input):
        #         print(input.shape)
        '''
        input: batchsize* vector dimension * n 
        (1 by d by n)
        
        return 
            out : size =vector dimension, will be flattened afterwards
        '''
        x = input.squeeze(0)
        x = x.permute(1, 0)
        out = fun(input)

        return out"""
def Net(client_weights, server_weight):
    x = client_weights.squeeze(0)
    x = x.permute(1,0)
    out = fun(x, server_weight)
    return out    