# James Merrick, July 8th 2016
# Minimum viable product of adapt/retreat moel

# James Merrick, July 13th 2016
# Updated structure following discussion with Melanie Craxton
# James Merrick, October 21 2016
# Reform probability structure to take account of Delavane's info
# main change is that flooding is now no longer a simple probability but a probabilistic damage function


# REMEMBER - GIT STRUCTURE IN PLACE!

import random
import sys
from scipy.stats import genextreme

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


    def update_prob_act(self):
        self.calculate_damage()
        for i in range(self.regions):
            self.prob_act[i] = max(self.init_prob_act,min(1,(self.actual_damage[i]/self.expected_damage[i]))) #for now just assume we only care about our own region

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act[i]:
                        self.action[i] = 1      
                        self.transition[i] = 1

    def calculate_damage(self):
        for i in range(self.regions):
            s=flood_rv(i)
            actual_damage[i]=damage(s,i)

    def flood_rv(region):
        return genextreme.rvs(c(region),loc(region),scale(region))

    def damage(s,region):
        #either delavane function calculated from bottom up (more work) or something simpler that I have not worked out yet
                                                                        
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
                print 'alpha this run: ', self.alpha
                print 'total number of floods due to no action', sum(self.hits)
                print 'number of floods due to no action by region', (self.hits)
                break


    def plot_eile(self):
        agent_colors = {0:'0', 1:'1'}        
        roundedlist=[round(x,2) for x in self.prob_act]
        for i in range(self.regions):
                print agent_colors[self.action[i]],
                if (self.action[i] == 1) and (self.transition[i] != 1):
                    roundedlist[i] = '-'
        print '\t',roundedlist
        print ''




#parameters:(number of regions, prob flood, prob action, number of iterations)
#ar_1 = adaptretreat(10,.2,.5,500)
arg=sys.argv
ar_1 = adaptretreat(int(float(arg[1])),float(arg[2]),float(arg[3]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'




