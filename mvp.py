# James Merrick, July 8th 2016
# Minimum viable product of adapt/retreat moel


#import matplotlib.pyplot as plt
import itertools
import random
import copy


class adaptretreat:
    def __init__(self, regions, prob_flood, prob_act, influence_threshold, n_iterations):
        self.regions = regions
        self.prob_flood = prob_flood 
        self.prob_act = prob_act
        self.influence_threshold = influence_threshold
        self.n_iterations = n_iterations
        self.action = []
        # 0 if no action, 1 if action
        self.flooded = []
        # 0 if not flooded, 1 if flooded

    def populate(self):
        #want action and flooded to be a vector of length number of regions
        #then want each element of flooded to equal zero, for now
        self.flooded = [0 for x in range(self.regions)]
        self.action = [0 for x in range(self.regions)]
        #then we will see who wants to act (assuming in this version that they all should if behaving rationa
        print 'initial:'
        self.plot_eile()    
        self.decide_action()
        print 'before flooding:'
        self.plot_eile()    

    def is_worried(self):
        # returns TRUE when fraction flooded greater than influence threshold
        #this could be extended when agents are affected by different agents differently
        #print float(sum(self.flooded)) / self.regions 
        return float(sum(self.flooded)) / self.regions > self.influence_threshold


    def is_flooded(self):
        for i in range(self.regions):
            if random.random() < self.prob_flood:
                self.flooded[i] = 1

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act:
                        self.action[i] = 1         

    def update(self):
        print 'after observation:'
        for iter in range(self.n_iterations):
            self.is_flooded()
            #self.decide_action()
            if self.is_worried():
                self.decide_action()
            self.plot_eile()  
            if sum(self.action) == self.regions:
                break


    def plot_eile(self):
        agent_colors = {0:'+', 1:'-'}        
        for i in range(self.regions):
                print agent_colors[self.action[i]],
        print ''



ar_1 = adaptretreat(10,.2,.5,.1,500)
ar_1.populate()
ar_1.update()


