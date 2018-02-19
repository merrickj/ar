# James Merrick, February 2018
# Developed from minimum viable product of adapt/retreat moel


import random
import sys
import json
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
from scipy.stats import genextreme
from scipy.integrate import quad
from scipy.optimize import fsolve
from import_ireland import *

def flood_rv(region):
    c = -float(fg[region][2])
    loc = float(fg[region][0])
    scale = float(fg[region][1])
    return genextreme.rvs(c,loc,scale)


class adaptretreat:
    def __init__(self, init_beta, n_iterations):
        self.regions = 29
        self.init_beta = init_beta
        self.n_iterations = n_iterations
        self.action = [] # height of wall built?
        self.meanflood=[]
        self.lb=[]
        self.expected_damage=[]
        self.true_expect=[]
        self.actual_damage=[]
        self.alpha = min(1,10*(float(1)/self.regions)) # how much weight your own region relative to neighbours

    def populate(self):
        self.action = [0 for x in range(self.regions)]
        self.actual_damage = [0 for x in range(self.regions)]
        self.meanflood = [0 for x in range(self.regions)]
        self.lb = [0 for x in range(self.regions)]        
        for i in range(self.regions):
            self.lb[i] = slr(i)
        self.flood_mean()
        self.expected_damage = [0 for x in range(self.regions)]
        self.true_expect = [0 for x in range(self.regions)]                
        self.truee()
        self.total_damage = [0 for x in range(self.regions)]
        self.beta = [self.init_beta for x in range(self.regions)]        


    def update_beta(self):
        for i in range(self.regions):
            if self.expected_damage[i] > 0:
                self.beta[i] = self.beta[i] * (self.actual_damage[i] / self.expected_damage[i])
            # a hack of an update rule for now

    def update_lb(self):
        for i in range(self.regions):
            self.lb[i] = slr(i) + self.action[i] 

    def fn(self,s,r):
        return (self.beta[r]*self.g(s,r)) - self.dcost(r,s)
            
    def decide_action(self):
        for i in range(self.regions):
            initial = self.meanflood[i] * 3
            s_inter = fsolve(self.fn,initial,i)
            if s_inter > 0:
                self.action[i] = self.action[i] + s_inter[0]


    def dcost(self,r,s):
        h = s+self.lb[r]
        pc = 7.7598    
        return pc*float(length(r))*2*h
    
    def g(self,s,r):
        c_temp = -float(fg[r][2])
        loc_temp = float(fg[r][0])
        scale_temp = float(fg[r][1])
        return genextreme.pdf(s,c_temp,loc_temp,scale_temp) * self.damage(s,r)

                    
    def damage(self,e,r):
        if (e - self.action[r]) > 0:
            out = quad(integrand,self.lb[r],e+self.lb[r]-self.action[r],r)
            return out[0]
        else:
            return 0


    def calculate_actual_damage(self):
        for i in range(self.regions):
            s=flood_rv(i)
            self.actual_damage[i] = self.damage(s,i)
            self.total_damage[i] = self.total_damage[i] + self.actual_damage[i]

     
    def calculate_expected_damage(self):
        for i in range(self.regions):
            if self.action[i] > 0:
                out = quad(self.g,0,2,i)
                self.expected_damage[i] = out[0] * self.beta[i]
            else:
                self.expected_damage[i] = self.true_expect[i] * self.beta[i]

    def truee(self):
        # Read JSON file
        with open('true.json') as data_file:
            self.true_expect = json.load(data_file)
# This was to output the json file the first time round. It is slow to calculate the expectations, so sent it out, and now it uploads it every time. Once a wall is built the expectation for future flooding changes, thus we re-calculate the expectation in those cases above
#        for i in range(self.regions):
#            out = quad(self.g,0,2,i)
#            self.true_expect[i] = out[0]
#        with io.open('true.json', 'w', encoding='utf8') as outfile:
#            str_ = json.dumps(self.true_expect,
#                      indent=4, sort_keys=True,
#                      separators=(',', ': '), ensure_ascii=False)
#            outfile.write(to_unicode(str_))


# populate such that this is only generated once
    def flood_mean(self):
        for region in range(self.regions):
            c = -float(fg[region][2])
            loc = float(fg[region][0])
            scale = float(fg[region][1])
            self.meanflood[region] = genextreme.stats(c,loc,scale,moments='m')

    def update(self):
        for iter in range(self.n_iterations):
            self.decide_action()
            self.calculate_actual_damage()
            self.calculate_expected_damage()
            self.update_beta()
            self.update_lb()
#            print map(lambda x: "{:.2f}".format(self.beta), dataList)
#                        print 'self.beta: %.2f' % self.beta
#            temp = [ '%.2f' % elem for elem in self.beta ]
            temp = [ round(elem,2) for elem in self.beta ]
            print 'self.beta:',temp
            print 'self.action', self.action



#parameters:(beta, number of iterations)
arg=sys.argv
ar_1 = adaptretreat(float(arg[1]),5)
print arg
ar_1.populate()
ar_1.update()
#print '[0 = no action, 1 = action]'



# remember basically have to put in the last graph I sent melanie. each region decide what to do based on that. but imperfect decision due to \beta. put in mechanism to update that then also, maybe just a heuristic it inches up if wave is higher than the mean they are expecting. there is probably a fancier formula for doing that - surely Bayes?!







