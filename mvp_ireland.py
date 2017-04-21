# James Merrick, April 2017
# Developed from minimum viable product of adapt/retreat moel


import random
import sys
from scipy.stats import genextreme
from scipy.integrate import quad
from import_ireland import *

class adaptretreat:
    def __init__(self, init_prob_act, n_iterations):
        self.regions = 29
        self.init_prob_act = init_prob_act
        self.n_iterations = n_iterations
        self.action = [] # 0 if no action, 1 if action
        self.alpha = min(1,10*(float(1)/self.regions)) # how much weight your own region relative to neighbours
        self.transition = [0 for x in range(self.regions)]

    def populate(self):
        self.action = [0 for x in range(self.regions)]
        self.actual_damage = [0 for x in range(self.regions)]
        self.expected_damage = [1 for x in range(self.regions)]
        self.calculate_expected_damage()
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
            if self.expected_damage[i]>0:
                self.prob_act[i] = max(self.prob_act[i],self.init_prob_act*(self.actual_damage[i]/self.expected_damage[i])) #for now just assume we only care about our own region
            else:
                self.prob_act[i] = 1

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
                self.actual_damage[i],err_temp = quad(self.damage,0,s,i)
                self.total_damage[i] = self.total_damage[i] + self.actual_damage[i]

    def calculate_expected_damage(self):
        for i in range(self.regions):
            s=self.flood_mean(i)
            self.expected_damage[i],err_temp = quad(self.damage,0,s,i)
            print self.expected_damage[i],'expected damage'

    def flood_mean(self,region):
        c = -float(fg[region][2])
        loc = float(fg[region][0])
        scale = float(fg[region][1])
        return genextreme.stats(c,loc,scale,moments='m')/scale

    def flood_rv(self,region):
        c = -float(fg[region][2])
        loc = float(fg[region][0])
        scale = float(fg[region][1])
        return genextreme.rvs(c,loc,scale)/scale
#        return genextreme.rvs(c(region),loc(region),scale(region))

    def damage(self,e,region):
        #either delavane function calculated from bottom up (more work) or something simpler that I have not worked out yet
        sigma_k = float(k[region][0]);
        sigma_l = float(p[region][0]);
#        print a[region],'yo'
        a_ = a[region];
        return (1-rho)*self.area(e,a_)*(sigma_k*self.psi(e)+sigma_l*vsl*mu)

    def area(self,y,a_):
        a=[]
        for i in range(0,15):
            temp=float(a_[i])
            a.append(temp)
        return a[0]*max(0,min(0.5,y))+(a[1]+a[0])/2*max(0,min(1,y-0.5))+a[1]*max(0,min(0.5,y-1.5))+a[2]*max(0,min(1,y-2))+a[3]*max(0,min(1,y-3))+a[4]*max(0,min(1,y-4))+a[5]*max(0,min(1,y-5))+a[6]*max(0,min(1,y-6))+a[7]*max(0,min(1,y-7))+a[8]*max(0,min(1,y-8))+a[9]*max(0,min(1,y-9))+a[10]*max(0,min(1,y-10))+a[11]*max(0,min(1,y-11))+a[12]*max(0,min(1,y-12))+a[13]*max(0,min(1,y-13))+a[14]*max(0,y-14)

    def psi(self,e):
        return e/(1+e);
                                                                        
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
ar_1 = adaptretreat(float(arg[1]),500)
print arg
ar_1.populate()
ar_1.update()
print '[0 = no action, 1 = action]'
#jam = quad(integrand,0,2.58)# note does not quite work yet!
#print a
#print 'psi' gev.psi(10)



