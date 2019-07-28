import gym
from gym.spaces import Discrete, Tuple
from gym.utils import seeding
from six import StringIO
import sys
import random
import subprocess
import numpy as np
import copy

import io
import json
import os

#observation space
#{0,BlocksNum}
#block to move
#{0,BlocksNum -1}
#destination
#{0,BlocksNum}


# IMPORTANT: 
# Before using configure the __init__ function, 
# Configure the variables 'numBlocks' and 'self.bwstates_path'

#The following rewards are considered
#0 when the agent reaches the goal state
#-1 for a valid state
#-10 for reaching a non-valid state (due to the way we code the states some of the combinations are not valid combinations)

DEFAULT_NUM_BLOCKS = 3

class BlocksWorldEnv(gym.Env):
    metadata = {'render.modes': ['human', 'ansi']}
    

    def __init__(self):
        numBlocks = self.readNumBlocksFromFile()
        self.bwstates_path = './BWSTATES/bwstates.1/bwstates'
        #self.bwstates_path = '/home/usuaris/rgarzonj/github/LSTMs/Blocksworld/GENERATOR/bwstates.1/bwstates'

        self.numBlocks = numBlocks
        #The tuple consists on: Block to move, Destination to be moved
        self.action_space = Tuple(
            [Discrete(numBlocks), Discrete(numBlocks)])

        self.observation_space = Tuple(
            [Discrete(numBlocks), Discrete(numBlocks),Discrete(numBlocks)])
        self.episode_total_reward = None
        self.numactions = (numBlocks+1)*(numBlocks+1)
#        self.numactions = (numBlocks+1)*numBlocks


        self._seed()
    
    def readNumBlocksFromFile(self):
        numBlocks = DEFAULT_NUM_BLOCKS
        if (os.path.isfile('numBlocks.json')):
             try:
                 to_unicode = unicode
             except NameError:
                 to_unicode = str
                 # Read JSON file
             with open('numBlocks.json') as data_file:
                 data_loaded = json.load(data_file)
             return (data_loaded['numBlocks'])
        else:
            return numBlocks

    
    def generate_random_initial_OLD(self):
        nBlocks = self.numBlocks
        startState = []
        i=1
        while (i<=nBlocks):
            r = random.randint(0,nBlocks)
            print ('i' + str(i))
            print ('r' + str(r))
            while (r!=0 and ((r==i) or (r in startState) or ((r<i) and (startState[r-1]==i)))):
                r = random.randint(0,nBlocks)
                print ('r' + str(r))
            startState.append(r)
            i += 1
            print (str(startState))
        return startState
    
    def generate_random_state (self):
    #""" Generates valid initial state from the implementation of Slaney & Thiébaux""" 
        bwstates_command = self.bwstates_path + ' -n ' + str(self.numBlocks) 
        #+ ' -r ' + str(seed)
        proc = subprocess.Popen(bwstates_command,stdout=subprocess.PIPE,shell=True)
        (out, err) = proc.communicate()
        out_str = out.decode('utf8')
        lines = out_str.split('\n')
        results = lines[1].strip()
        results = results.split()
        res = list(map(int, results))
        return res
    
    def generate_random_goal(self,initialState):
        goalState = self.generate_random_state()
        while (str(initialState)==str(goalState)):
            goalState = self.generate_random_state()
        return (goalState) 
          
    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def integer_to_action (self,int_action):
    # From an integer returns the encoded format for an action
    # [block to move, destination]
        ret = []
        ret.append(int(int_action/(self.numBlocks+1)))
        ret.append(int_action%(self.numBlocks+1))
        #print ('\nDecoding action' + str(ret))
        return ret
        
    def action_to_integer (self,action):
    # From an encoded action [block to move, destination] 
    # returns a simple integer
        ret = action[0]*(self.numBlocks-1) + action[1]
        #print ('\Encoding action' + str(ret))
        return ret        

    def getObservationAndGoal(self):
        """
        Returns the featurized representation for a state.
        """
        ret = np.concatenate((self.state,self.goal))
        return ret


    def _step(self,action):
        Done = False
        #Move the corresponding block
        #action may come in integer format or as a list [block_to_move,destination]
#        if (type(action)!="list"):
        if ((type(action) is not list)):
            action = self.integer_to_action(action)
        block_to_move, destination = action
        #print (action)
        #print (destination)
        #print (block_to_move)        
        #print (self.state)
        if ((destination<0) or (destination>self.numBlocks) or (block_to_move>self.numBlocks) or (self.state[block_to_move-1]==destination) or  ((block_to_move == destination) and (destination !=0))):
#        if ((self.state[block_to_move]==destination) or ((block_to_move+1 == destination) and (destination !=0))):
            #print ('\nNothing to do')
            #Unuseful move, same position as we have now or we try to move blockX on top of blockX
            #reward = -10
            reward = -1
        else:
#            if (block_to_move in self.state):
            if ((block_to_move in self.state) or (block_to_move==0)):
                #If block_to_move has some block on top, reward = -2 do nothing
                #Impossible move
                #print ('\nBlock ' + str(block_to_move+1) + ' to move is not clear')
                #reward = -10
                reward = -1
            else:
                if ((destination in self.state) and (destination != 0)):
                    #If destination has some block on top and destination is not the table, reward = -1 do nothing
                    #print ('Destination block' + str(destination) + ' is not clear')
                    #reward = -10
                    reward = -1
                else:
                    #self.state [block_to_move] = destination
                    self.state [block_to_move-1] = destination
                    if (destination == 0):
                        dest = " to the table"
                    else:
                        dest = " on top of block " + str(destination)
                    #print ('\nMoving block' + str (block_to_move+1) + dest)
                    if (str(self.state)==str(self.goal)):
                        print ('\n*************** PROBLEM SOLVED!!!!!!!!!!!! **********')
                        #reward = 0
                        reward = 1
                        Done = True
                    else:                 
                        #If we use 0, the Q-learning algorithm is not learning correctly
                        #reward = 0
                        reward = -1
        self.last_reward = reward
        self.episode_total_reward += reward
        return self._get_obs(), reward, Done, {}

    def _reset(self):
#        self.initial = [2,0]
#        self.goal = [0,3,1]
        #self.goal = [0,1]
        self.initial = self.generate_random_state()
        self.goal = self.generate_random_goal(self.initial)
#        self.goal = [0,1]
        self.state = copy.deepcopy(self.initial)
        self.last_reward = 0
        self.episode_total_reward = 0.0
#        high = np.array([np.pi, 1])
#        self.state = self.np_random.uniform(low=-high, high=high)
#        self.last_u = None

        return self._get_obs()

    def _get_obs(self):
        ret = np.concatenate((self.state,self.goal))
        return ret
#        return self.state

    def _render(self, mode='human', close=False):
        if close:
            # Nothing interesting to close
            return

        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write("************** New Step ***************\n") 
        outfile.write("[block_to_move, destination]; b [0,numBlocks-1], d[0,numBlocks]\n")                         
        outfile.write("Initial state: " + str(self.initial)+ "\n")
        outfile.write("Current state: " + str(self.state)+ "\n")
#       outfile.write (str(self.state))
        outfile.write("Goal state:    "+ str(self.goal) + "\n")
        outfile.write ("Reward: " + str(self.last_reward)+ "\n")
        outfile.write ("Total Episode Reward: " + str(self.episode_total_reward)+ "\n")
        return outfile

    def plot_row (self,blocksList):
        lines = []
        oneLine = ""
        for block in blocksList:                
            oneLine = oneLine + " ¯¯¯ "
        lines.append(oneLine)
        
        oneLine = ""
        for block in blocksList:                
            oneLine = oneLine + "| " + str(block+1) + " |"                                            
        lines.append(oneLine)

        oneLine = ""
        for block in blocksList:                
            oneLine = oneLine + " ___ "
        lines.append(oneLine)
        return lines
        
    def _render_v2(self, mode='human', close=False):
        if close:
            # Nothing interesting to close
            return

        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write("************** New Step ***************\n") 
        # List the files in the table
        on_table = sorted([i for i, e in enumerate(self.state) if e == 0])
        lines = []
        #lines.append("==============================================================\n")                             
        lines.extend(self.plot_row(on_table))

#        oneLine = ""
#        for block in on_table:                
#            oneLine = oneLine + " ¯¯¯ "
#        lines.append(oneLine)
#        
#        oneLine = ""
#        for block in on_table:                
#            oneLine = oneLine + "| " + str(block+1) + " |"                                            
#        lines.append(oneLine)
#
#        oneLine = ""
#        for block in on_table:                
#            oneLine = oneLine + " ___ "
#        lines.append(oneLine)

        # Take 
        #print ('on_table')
        #print (on_table)
        newrow = []
        on_table = [x+1 for x in on_table]
        print ('on_table')
        print (on_table)
        for block in on_table:                
            #For every block, search if is in the list
            if (block in self.state):
                newrow.append(self.state.index(block))

        while (len(newrow)>0):            
            print('newrow')
            print (newrow)
            lines.extend(self.plot_row(newrow))
            newrow = [x+1 for x in newrow]
            newrow2 = newrow
            newrow = []
            for block in newrow2:                
            #For every block, search if is in the list
                if (block in self.state):
                    newrow.append(self.state.index(block))
            
        # Plot everything in reverse order as it was added

        l = len(lines)-1
        while (l>=0):
            #print (l)
            outfile.write(lines[l])
            outfile.write("\n")
            l = l-1
                        

#        outfile.write("[block_to_move, destination]; b [0,numBlocks-1], d[0,numBlocks]\n")                 
#        outfile.write("Initial state: " + str(self.initial)+ "\n")
#        outfile.write("Current state: " + str(self.state)+ "\n")
#       outfile.write (str(self.state))
#        outfile.write("Goal state:    "+ str(self.goal) + "\n")
#        outfile.write ("Reward: " + str(self.last_reward)+ "\n")
#        outfile.write ("Total Episode Reward: " + str(self.episode_total_reward)+ "\n")
        return outfile
