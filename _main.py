from __future__ import print_function

import torch
import torch.nn.functional as F
import torch.optim as optim
from tensorboardX import SummaryWriter

from clients_attackers import *
from server import Server
from utils.adversary import *

def main(args):
    print('#####################')
    print('#####################')
    print('#####################')
    #print(f'Aggregation Rule:\t{args.AR}\nData distribution:\t{args.loader_type}\nAttacks:\t{args.attacks} ')
    print('#####################')
    print('#####################')
    print('#####################')

    torch.manual_seed(args.seed)

    device = args.device

    #attacks = args.attacks

    writer = SummaryWriter(f'./logs/{args.experiment_name}')

    if args.dataset == 'mnist':
        from tasks import mnist
        trainData = mnist.train_dataloader(args.num_clients, loader_type=args.loader_type,
                                           store=False)
        testData = mnist.test_dataloader(args.test_batch_size)
        Net = mnist.Net
        criterion = F.cross_entropy
    elif args.dataset == 'cifar':
        from tasks import cifar
        trainData = cifar.train_dataloader(args.num_clients, loader_type=args.loader_type,
                                           store=False)
        testData = cifar.test_dataloader(args.test_batch_size)
        Net = cifar.Net
        criterion = F.cross_entropy
    elif args.dataset == 'cifar100':
        from tasks import cifar100
        trainData = cifar100.train_dataloader(args.num_clients, loader_type=args.loader_type,
                                              store=False)
        testData = cifar100.test_dataloader(args.test_batch_size)
        Net = cifar100.Net
        criterion = F.cross_entropy
    elif args.dataset == 'fmnist':
        from tasks import fmnist
        trainData = fmnist.train_dataloader(args.num_clients, loader_type=args.loader_type,
                                          store=False)
        testData = fmnist.test_dataloader(args.test_batch_size)
        Net = fmnist.Net
        criterion = F.cross_entropy  

    # create server instance
    model0 = Net()
    server = Server(model0, testData, criterion, device)
    server.set_AR(args.AR)
    
    # create clients instance
    model = Net()
    if args.optimizer == 'SGD':
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    elif args.optimizer == 'Adam':
        optimizer = optim.Adam(model.parameters(), lr=args.lr)

    client_list, labels = adversary_setup(args, model, trainData, optimizer, criterion, device)
    server.attach(client_list)
    server.set_clabels(labels)
    
    loss, accuracy = server.test()
    steps = 0
    writer.add_scalar('test/loss', loss, steps)
    writer.add_scalar('test/accuracy', accuracy, steps)

    if 'BD' in args.type.upper():
        if 'SEMANTIC' in args.attacks.upper():
            loss, accuracy, bdata, bpred = server.test_semanticBackdoor()
        else:
            server.backdoor_testing()
            loss, accuracy = server.test_backdoor()

        writer.add_scalar('test/loss_backdoor', loss, steps)
        writer.add_scalar('test/backdoor_success_rate', accuracy, steps)

    for j in range(args.epochs):
        steps = j + 1

        print('\n\n########EPOCH %d ########' % j)
        print('###Model distribution###\n')
        server.distribute()
        #         group=Random().sample(range(5),1)
        group = range(args.num_clients)
        server.train(group)
        #         server.train_concurrent(group)

        loss, accuracy = server.test()

        writer.add_scalar('test/loss', loss, steps)
        writer.add_scalar('test/accuracy', accuracy, steps)

        if 'BD' in args.type.upper():
            if 'SEMANTIC' in args.attacks.upper():
                loss, accuracy, bdata, bpred = server.test_semanticBackdoor()
            else:
                loss, accuracy = server.test_backdoor()

            writer.add_scalar('test/loss_backdoor', loss, steps)
            writer.add_scalar('test/backdoor_success_rate', accuracy, steps)

    writer.close()
