# James Merrick, July 8th 2016
# Minimum viable product of adapt/retreat moel

# James Merrick, July 13th 2016
# Updated structure following discussion with Melanie Craxton

import random
import sys

class adaptretreat:
    def __init__(self, regions, prob_flood, init_prob_act, n_iterations):
        self.regions = regions
        self.prob_flood = prob_flood 
        self.init_prob_act = init_prob_act
        self.n_iterations = n_iterations
        self.action = []
        # 0 if no action, 1 if action
        self.damaged = []#can maybe GO
        # 0 if not damaged, 1 if damaged
        self.initial_noact = []
        self.hits = []
        self.potential = 0
        self.alpha = 2*(float(1)/self.regions)
        self.prob_alpha = []

    def populate(self):
        #want action and damaged to be a vector of length number of regions
        #then want each element of damaged to equal zero, for now
        self.damaged = [0 for x in range(self.regions)]
        self.action = [0 for x in range(self.regions)]
        self.prob_alpha = [self.prob_flood for x in range(self.regions)]
        self.prob_act = [self.init_prob_act for x in range(self.regions)]
        self.hits =  [0 for x in range(self.regions)]
        #then we will see who wants to act (assuming in this version that they all should if behaving rationa
        print 'initial:'
        self.plot_eile()    
        self.decide_action()
        self.initial_noact = self.regions-sum(self.action)
        print 'before flooding:'
        self.plot_eile()    


    def update_flood_perception(self,iter):
        for i in range(self.regions):
            if self.action[i] == 0:
                #print self.alpha, self.hits[i], iter, self.hits, self.potential
                #print 'self.alpha',self.alpha
                #print 'self.hits[i]',self.hits[i]
                #basically seems that prob_act goes to zero too quickly. prob_act probably should not go to zero once a single zero prob_alpha comes along. what would make more sense would be for prob_act to decline...? or alternatively a mechanism where it could grow more quickly once the waves hit
                self.prob_alpha[i] = self.alpha * (float(self.hits[i])/(iter+1)) + ((1-self.alpha)*(float(sum(self.hits)-self.hits[i])/(self.potential - 1)))
            else:
                self.prob_alpha[i] = self.prob_flood # would be computationally better not to do it this way, but want to get it working for now
        print 'prob_alpha ', self.prob_alpha

    def update_prob_act(self):
        print 'self.pact before ',self.prob_act
        for i in range(self.regions):
            #print 'self.pa',self.prob_alpha
            self.prob_act[i] = self.prob_act[i] * (float(self.prob_alpha[i])/self.prob_flood)
            self.prob_act[i] = max(0.01,self.prob_act[i])
            self.prob_act[i] = min(1,self.prob_act[i])
        print 'self.pact',self.prob_act

    def is_damaged(self):
        self.potential = self.potential + (self.regions-sum(self.action))
        for i in range(self.regions):
            if self.action[i] == 0:
                if random.random() < self.prob_flood:
                    self.damaged[i] = 1
                    self.hits[i] = self.hits[i] + 1

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act[i]:
                        self.action[i] = 1         
                                                                        
    def update(self):
        print 'after observation:'
        for iter in range(self.n_iterations):
            self.is_damaged()
            self.update_flood_perception(iter)
            self.update_prob_act()
            self.decide_action()
            #if self.is_worried():
            self.plot_eile()  
            #print self.prob_act
            #print self.prob_alpha
            #print self.hits
            if sum(self.action) == self.regions:
                print 'ends at observation ',iter
                print self.prob_act
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
ar_1 = adaptretreat(int(float(arg[1])),float(arg[2]),float(arg[3]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'
#ar_1.print_count()



