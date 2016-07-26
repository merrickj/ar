# James Merrick, July 8th 2016
# Minimum viable product of adapt/retreat moel

# James Merrick, July 13th 2016
# Updated structure following discussion with Melanie Craxton

# REMEMBER - GIT STRUCTURE IN PLACE!

import random
import sys

class adaptretreat:
    def __init__(self, regions, prob_flood, init_prob_act, n_iterations):
        self.regions = regions
        self.prob_flood = prob_flood 
        self.init_prob_act = init_prob_act
        self.n_iterations = n_iterations
        self.action = [] # 0 if no action, 1 if action
        self.hits = []   # Number of times flooded
        self.potential = 0 # Number of potential flooding events
        self.alpha = min(1,10*(float(1)/self.regions)) # how much weight your own region relative to neighbours
        self.prob_alpha = []
        self.transition = [0 for x in range(self.regions)]

    def populate(self):
        self.action = [0 for x in range(self.regions)]
        self.prob_alpha = [self.prob_flood for x in range(self.regions)]
        self.prob_act = [self.init_prob_act for x in range(self.regions)]
        self.hits =  [0 for x in range(self.regions)]
        #then we will see who wants to act (assuming in this version that they all should if behaving rationa
        print 'initial:'
        self.plot_eile()    
        self.decide_action()
        print 'before flooding:'
        self.plot_eile()    


    def update_flood_perception(self,iter):
        if (self.potential-(iter+1)) == 0:
            denominator = 1
        else:
            denominator = self.potential - (iter+1);
        for i in range(self.regions):
            if self.action[i] == 0:
                self.prob_alpha[i] = self.alpha * (float(self.hits[i])/(iter+1)) + (1-self.alpha)*(float(sum(self.hits)-self.hits[i]) / denominator)
            else:
                self.prob_alpha[i] = self.prob_flood # would be computationally better not to do it this way, but want to get it working for now


    def update_prob_act(self):
        for i in range(self.regions):
            #Bayes rule  P(A|B)=P(B|A)P(A)/P(B)
            #self.prob_act[i] = self.init_prob_act * (float(self.prob_alpha[i])/self.prob_flood)
            # this would be an alternate
            self.prob_act[i] = max(self.init_prob_act, self.prob_act[i]*(float(self.prob_alpha[i])/self.prob_flood))

    def is_damaged(self):
        self.potential = self.potential + (self.regions-sum(self.action))
        for i in range(self.regions):
            if self.action[i] == 0:
                if random.random() < self.prob_flood:
                    self.hits[i] = self.hits[i] + 1

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act[i]:
                        self.action[i] = 1      
                        self.transition[i] = 1
                                                                        
    def update(self):
        print 'after observation:\t P(act)'
        for iter in range(self.n_iterations):
            self.transition = [0 for x in range(self.regions)]
            self.is_damaged()
            self.update_flood_perception(iter)
            self.update_prob_act()
            self.decide_action()
            self.plot_eile()  
            if sum(self.action) == self.regions:
                print 'ends at observation ',iter
                break


    def plot_eile(self):
        agent_colors = {0:'0', 1:'1'}        
        roundedlist=[round(x,2) for x in self.prob_act]
        for i in range(self.regions):
                print agent_colors[self.action[i]],
                if (self.action[i] == 1) and (self.transition[i] != 1):
                    roundedlist[i] = '-'
        print '\t',roundedlist,self.hits,self.prob_alpha
        print ''
        print 'self.alpha',self.alpha



#parameters:(number of regions, prob flood, prob action, number of iterations)
#ar_1 = adaptretreat(10,.2,.5,500)
arg=sys.argv
ar_1 = adaptretreat(int(float(arg[1])),float(arg[2]),float(arg[3]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'




