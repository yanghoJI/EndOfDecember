# https://github.com/pytorch/examples/blob/master/mnist/main.py
## add image normalization

from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision.transforms import RandomCrop, Resize, Compose, ToTensor, Normalize
from torchvision.datasets import ImageFolder
import matplotlib.pyplot as plt
import numpy as np
import time
import cv2
import random as r
import os
from PIL import Image


from game2048V1 import Game2048

class Net(nn.Module):

    def __init__(self, outsize):
        super(Net, self).__init__()
        self.imagesize = (4,4,1)
        self.labeldict = {'0' : 'Left', '1' : 'Right', '2' : 'Up', '3' : 'Down'}

        self.conv2x = nn.Conv2d(1, 40, kernel_size=2, padding=0)     #out 10,3,3
        self.conv3x = nn.Conv2d(1, 40, kernel_size=3, padding=0)     # out 10,2,2
        self.conv4x = nn.Conv2d(1, 40, kernel_size=4, padding=0)  # out 10,1,1


        self.fc1 = nn.Linear(90*4 + 40*4 + 10*4, outsize)


    def forward(self, x):
        in_size = x.size(0)

        x2 = F.relu(self.conv2x(x))
        x3 = F.relu(self.conv3x(x))
        x4 = F.relu(self.conv4x(x))

        x2 = x2.view(in_size, -1)  # flatten the tensor
        x3 = x3.view(in_size, -1)  # flatten the tensor
        x4 = x4.view(in_size, -1)  # flatten the tensor

        out = torch.cat((x2, x3, x4), 1)
        out = self.fc1(out)             # batch, outsize

        return out

    def predict(self, filepath, device, trF):
        inimage = Image.open(filepath)
        inimage = inimage.convert('RGB')
        inimage = trF(inimage)
        inimage = inimage.view(1,3,224,224)
        '''
        inimage = cv2.cvtColor(imgarr, cv2.COLOR_BGR2RGB)
        inimage = cv2.resize(inimage, (self.imagesize[0], self.imagesize[1]))
        inimage = np.transpose(inimage, (2, 0, 1)) / 255
        inimage = np.expand_dims(inimage, axis=0)
        inimage = torch.tensor(inimage.astype('float32'))
        '''
        inimage = inimage.to(device)
        netout = self.forward(inimage)
        label = str(netout.argmax().item())
        return self.labeldict[label]



def weight_init(m):
    if isinstance(m, torch.nn.Conv2d) or isinstance(m, torch.nn.Linear):
        torch.nn.init.xavier_uniform_(m.weight)


def plotdata(epi, score, max_prob):
    xlist = epi
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(xlist, score, 'r-', label='score')
    plt.ylabel('score')
    plt.title('episode - score')
    plt.legend(loc=1)

    ax2 = plt.subplot(2, 1, 2)
    plt.plot(xlist, max_prob, 'b-', label='maximum prob')
    #plt.ylim(0, 100)
    plt.grid(True)
    plt.ylabel('max action prob')
    plt.title('episode - max action prob')
    plt.legend(loc=1)

    plt.tight_layout()

    plt.savefig('TrainGraph2048#2.png', dpi=300)
    plt.close()


def test(model_, loader, device):
    model_.eval()
    test_loss = 0
    correct = 0
    for data, target in loader:
        #data, target = Variable(data, volatile=True), Variable(target)
        data = data.to(device)
        target = target.to(device)
        output = model_(data)
        # sum up batch loss
        test_loss += F.nll_loss(output, target, reduction='sum').item()
        # get the index of the max log-probability
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(loader.dataset),
        100. * correct / len(loader.dataset)))
    test_acc = 100. * correct / len(loader.dataset)
    model_.train()
    return (test_loss, test_acc)



def preprocess(state, device):
    state[np.nonzero(state)] = np.log2(state[np.nonzero(state)])
    datum = torch.tensor(state)
    datum = datum.view((1, 1, 4, 4))
    datum = datum.to(device, dtype=torch.float)
    return datum


def getAction(actorout):
    action = np.random.choice(4, 1, p=actorout.detach().numpy()[0])[0]

    if action == 0:
        actkey = 'l'
    elif action == 1:
        actkey = 'r'
    elif action == 2:
        actkey = 'u'
    elif action == 3:
        actkey = 'd'

    return action, actkey


if __name__ == "__main__":
    ## parameter setting
    mode = 'train'
    max_episode = 100000
    lr = 0.0001
    render = False
    discount_factor = 0.9



    ## device check
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    print('runing device : {}'.format(device))


    ## build enviroment
    #env = Game2048(4)


    # model build
    model_actor = Net(outsize=4)
    model_actor.to(device)

    model_critic = Net(outsize=1)
    model_critic.to(device)

    '''
    ## test seq
    init_mat = np.copy(env.stat)
    arr = preprocess(init_mat, device)

    out_actor = model_actor(arr)
    out_critic = model_critic(arr)

    action = getAction(out_actor)
    print(action)
    '''

    ## train seq
    if mode == 'train':
        scores, episodes, max_probs = [], [], []

        optimizer_actor = optim.Adam(model_actor.parameters(), lr=lr)
        optimizer_critic = optim.Adam(model_critic.parameters(), lr=lr)

        softF = torch.nn.Softmax()

        for e in range(max_episode):
            env = Game2048(4)
            done = 0
            score = 0
            stepcnt = 0
            avg_max_prob = 0
            state = preprocess(np.copy(env.stat), device)


            while not done:
                if render == True:
                    env.setDispInit()
                    env.setDispArray()
                    cv2.imshow('epi : {}'.format(e), env.disp)

                actor_out = model_actor(state)
                actor_out_soft = softF(actor_out)
                actionidx, action = getAction(actor_out_soft)
                actor_out_logsoft = F.log_softmax(actor_out)


                next_state, reward, done = env.step(action)
                stepcnt += 1
                score += reward
                #reward = reward if not done else - abs(score//stepcnt * 10)
                reward = reward if not done else - 100
                #print(next_state, reward, action, done)
                next_state = preprocess(np.copy(next_state), device)
                reward = torch.tensor(reward, dtype=torch.float)

                value = model_critic(state)
                next_value = model_critic(next_state)


                if done:
                    advantage = reward - value[0]
                    target = reward
                else:
                    tempv = reward + discount_factor * next_value[0]
                    advantage = (reward + tempv) - value[0]
                    target = tempv


                ## update actor
                optimizer_actor.zero_grad()
                action_prob = actor_out_logsoft[0, actionidx]
                cross_entropy = action_prob * advantage.item()
                actor_loss = - cross_entropy
                actor_loss.backward()
                optimizer_actor.step()

                ## update critic
                optimizer_critic.zero_grad()
                critic_loss = F.mse_loss(value[0], target)
                critic_loss.backward()
                optimizer_critic.step()

                avg_max_prob += torch.max(actor_out_soft).item()

            episodes.append(e)
            scores.append(score)
            max_probs.append(avg_max_prob / stepcnt)

            if e % 20 == 0:
                print('epi : {}\tscore : {}\tmax_probs = {}\tend_step = {}'.format(episodes[-1], scores[-1], max_probs[-1], stepcnt))
                print(env.stat)
                plotdata(episodes, scores, max_probs)
            #print(11)