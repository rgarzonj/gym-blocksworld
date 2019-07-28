#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:01:41 2019

@author: rgarzon
"""
import random
import gym

env = gym.make('gym_blocksworld:BlocksWorld-v0')
env.seed(0)
env.reset()       

numBlocks = 3
num_episodes = 10

done = False
ep_lengths = []
n = 0
while (n<num_episodes):    
    steps =1
    done = False
    env.reset()
    next_action = [random.randint(0,numBlocks),random.randint(0,numBlocks)]
    while (done == False):
        obs, reward, done, empty = env.step (next_action)
        print ('Next action ' + str(next_action))
        print ('Obs ' + str(obs))
        next_action = random.randint(0,numBlocks)
        #env.render()
        steps +=1    
        print (done)
    print ('New episode')
    ep_lengths.append(steps)
    n+=1
    
    print ("Average episode length " + str(sum(ep_lengths) / float(len(ep_lengths))))
        #input("Press Enter to continue...")
        