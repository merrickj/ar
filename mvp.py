# James Merrick, July 8th 2016
# Minimum viable product of adapt/retreat moel


#import matplotlib.pyplot as plt
#import itertools
import random
#import copy
import sys

class adaptretreat:
    def __init__(self, regions, prob_flood, prob_act, influence_threshold, n_iterations):
        self.regions = regions
        self.prob_flood = prob_flood 
        self.prob_act = prob_act
        self.influence_threshold = influence_threshold
        self.n_iterations = n_iterations
        self.action = []
        # 0 if no action, 1 if action
        self.damaged = []
        # 0 if not damaged, 1 if damaged
        self.initial_noact = []
        self.count = 0

    def populate(self):
        #want action and damaged to be a vector of length number of regions
        #then want each element of damaged to equal zero, for now
        self.damaged = [0 for x in range(self.regions)]
        self.action = [0 for x in range(self.regions)]
        #then we will see who wants to act (assuming in this version that they all should if behaving rationa
        print 'initial:'
        self.plot_eile()    
        self.decide_action()
        self.initial_noact = self.regions-sum(self.action)
        print 'before flooding:'
        self.plot_eile()    

    def is_worried(self):
        # returns TRUE when fraction of those who did not originally act damaged greater than influence threshold
        #this could be extended when agents are affected by different agents differently
        #print float(sum(self.damaged)) / self.regions 
        return float(sum(self.damaged)) / self.initial_noact > self.influence_threshold


    def is_damaged(self):
        for i in range(self.regions):
            if self.action[i] == 0:
                if random.random() < self.prob_flood:
                    self.damaged[i] = 1
                    self.count = self.count + 1

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act:
                        self.action[i] = 1         

    def update(self):
        print 'after observation:'
        for iter in range(self.n_iterations):
            self.is_damaged()
            #self.decide_action()
            if self.is_worried():
                self.decide_action()
            self.plot_eile()  
            if sum(self.action) == self.regions:
                break


    def plot_eile(self):
        agent_colors = {0:'0', 1:'1'}        
        for i in range(self.regions):
                print agent_colors[self.action[i]],
        print ''

    def print_count(self):
        print ''
        print 'Total number of extra floodings: ',self.count        


#parameters:(number of regions, prob flood, prob action, influence threshold, number of iterations)
#ar_1 = adaptretreat(10,.2,.5,.5,500)
arg=sys.argv
ar_1 = adaptretreat(int(float(arg[1])),float(arg[2]),float(arg[3]),float(arg[4]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'
ar_1.print_count()



