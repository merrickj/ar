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
    def __init__(self, regions, init_prob_act, n_iterations):
        self.regions = regions
        self.init_prob_act = init_prob_act
        self.n_iterations = n_iterations
        self.action = [] # 0 if no action, 1 if action
        self.alpha = min(1,10*(float(1)/self.regions)) # how much weight your own region relative to neighbours
        self.transition = [0 for x in range(self.regions)]

    def populate(self):
        self.action = [0 for x in range(self.regions)]
        self.actual_damage = [0 for x in range(self.regions)]
        self.expected_damage = [100 for x in range(self.regions)]
        self.total_damage = [0 for x in range(self.regions)]
        self.prob_act = [self.init_prob_act for x in range(self.regions)]
        #then we will see who wants to act (assuming in this version that they all should if behaving rationa
        print 'initial:'
        self.plot_eile()    
        self.decide_action()
        print 'before flooding:'
        self.plot_eile()    


    def update_prob_act(self):
        self.calculate_damage()
        for i in range(self.regions):
            self.prob_act[i] = max(self.prob_act[i],self.actual_damage[i]/(self.init_prob_act*self.expected_damage[i])) #for now just assume we only care about our own region

    def decide_action(self):
            for i in range(self.regions):
                if self.action[i] == 0:
                    if random.random() < self.prob_act[i]:
                        self.action[i] = 1      
                        self.transition[i] = 1

    def calculate_damage(self):
        for i in range(self.regions):
            if self.action[i] == 0:
                s=self.flood_rv(i)
                self.actual_damage[i] = self.damage(s,i)
                self.total_damage[i] = self.total_damage[i] + self.actual_damage[i]


    def flood_rv(self,region):
        c=-.5
        loc=10
        scale=1
        return genextreme.rvs(c,loc,scale)
#        return genextreme.rvs(c(region),loc(region),scale(region))

    def damage(self,s,region):
        #either delavane function calculated from bottom up (more work) or something simpler that I have not worked out yet
        return s
                                                                        
    def update(self):
        print 'after observation:\t P(act)'
        for iter in range(self.n_iterations):
            self.transition = [0 for x in range(self.regions)]
            self.update_prob_act()
            self.decide_action()
            self.plot_eile()  
            if sum(self.action) == self.regions:
                print 'ends at observation ',iter
                print 'alpha this run: ', self.alpha
                break
        rounded_total_damage=[round(x,0) for x in self.total_damage]
        print 'Total damage:', rounded_total_damage


    def plot_eile(self):
#        print self.actual_damage
        agent_colors = {0:'0', 1:'1'}        
        roundedlist=[round(x,2) for x in self.prob_act]
        for i in range(self.regions):
                print agent_colors[self.action[i]],
                if (self.action[i] == 1) and (self.transition[i] != 1):
                    roundedlist[i] = '-'
        print '\t',roundedlist
        print ''




#parameters:(number of regions, prob action, number of iterations)
#ar_1 = adaptretreat(10,.2,.5,500)
arg=sys.argv
ar_1 = adaptretreat(int(float(arg[1])),float(arg[2]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'




