# James Merrick, May 2018
# Developed from minimum viable product of adapt/retreat model, and following discussions at Stanford University, April+May 2018

# Data from Ireland for this first version
# this version leaves the dynamics aside for now. We here assume a one period decision. 
# First year SLR is coming, and associated flooding, what are you going to do?
# will include plotting for each region here too
# a few things were missing from discussion with MC - a) [what was on edge of my mind] if retreat option how deal with flood risk b) if doing some sort of aggregate period decision, how deal with multiple years of flooding

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

def flood_rv(r):
    return genextreme.rvs(data.c[r],data.loc[r],data.scale[r])

def retreat_h(r):
    # we will say the retreat area is to the 100 year flood + end period sea level rise
    # this should be slr in final period (because height is a little arbitrary for us here anyway)
#    return slr(r,0) + genextreme.ppf(0.5, data.c[r],data.loc[r],data.scale[r])
    return slr(r,13) + genextreme.ppf(0.99, data.c[r],data.loc[r],data.scale[r])


class adaptretreat:
    def __init__(self, init_beta, n_iterations):
        self.regions= 29
        self.init_beta = init_beta
        self.n_iterations = n_iterations
        self.action = [0 for x in range(self.regions)]
        self.counteraction = [0 for x in range(self.regions)]        
        self.actual_damage = [0 for x in range(self.regions)]
        self.meanflood = [0 for x in range(self.regions)]
        self.slr = [0 for x in range(self.regions)]        
        self.retreat = [0 for x in range(self.regions)]
        self.wrongretreat = [0 for x in range(self.regions)]                
        self.retreatcost = [0 for x in range(self.regions)]
        self.expected_damage = [0 for x in range(self.regions)]
        self.true_expect = [0 for x in range(self.regions)]
        self.total_damage = [0 for x in range(self.regions)]
        self.counterdamage = [0 for x in range(self.regions)]
        self.protectcost = [0 for x in range(self.regions)]
        self.truecost = [0 for x in range(self.regions)]        
        self.noadaptcost = [0 for x in range(self.regions)]                
        

    def populate(self):
        for i in range(self.regions):
            self.slr[i] = slr(i,0)
        self.calculate_retreatcost()
        self.flood_mean()
        self.truee()
        self.beta = [self.init_beta for x in range(self.regions)]


    def update_beta(self):
        for i in range(self.regions):
            if (self.retreat[i] != 1) and (self.expected_damage[i] > 0):
                self.beta[i] = max(0.1,self.beta[i] * (self.actual_damage[i] / self.expected_damage[i]))
            # a hack of an update rule for now

    def update_slr(self,time):
        for i in range(self.regions):
            self.slr[i] = slr(i,time)

    def fn(self,s,r):
        return (self.beta[r]*self.g(s,r))  - self.dcost(r,s)
        #+self.calculate_inundation_cost(r,self.slr[r],0)
        
    def fn_true(self,s,r):
        return self.g(s,r) +self.calculate_inundation_cost(r,self.slr[r],0) - self.dcost(r,s)
    
    def decide_action(self,j):
        for i in range(self.regions):
            if self.retreat[i] != 1:  # if already retreated, out of the game
                initial = self.meanflood[i] * 3   # initial value to give solver

                #find optimum wall level (as per paper)
                s_inter = fsolve(self.fn,initial,i)

                #find optimum wall level as if beta was 1
                s_true = fsolve(self.fn_true,initial,i)


                # if self.inter < 0                
                # if self.calculate_inundation_cost(i,self.slr[i],0) > self.cost(i,self.slr[i]): # just starting implementation of diagram
                      # then go ahead and build wall to sea level height. otherwise we accept the flooding and inundation. question, what about the multiperiod aspect ? need to work that out in paper so
                    
                if s_inter > 0:
                    print('build some flood wall')
                    localfloodprotect = self.cost(i,s_inter[0]+self.slr[i]) 
                    if self.calculate_inundation_cost(i,self.slr[i],0) < self.cost(i,self.slr[i]):
                        print('Total benefit-cost ALERT (left side of diagram)')
                        # just an alert for now, won't do anything about it
                    self.action[i] = max(self.action[i], s_inter[0] + self.slr[i])
                else:
                    localfloodprotect = self.cost(i,self.slr[i])
                    if self.calculate_inundation_cost(i,self.slr[i],0) > localfloodprotect:
                        print('compare', self.calculate_inundation_cost(i,self.slr[i],0), localfloodprotect)
                        self.action[i] = max(self.action[i], self.slr[i])
                    else:
                        self.action[i] = self.action[i]
                        
                self.protectcost[i] = self.cost(i,self.action[i])
                print('protectcost',self.protectcost[i],data.n[i],self.action[i])
#                print('check here',self.action[i],self.slr[i],data.n[i])
                localcost = self.protectcost[i]

                if j==0 and self.protectcost[i]==0:
                    self.noadaptcost[i] = self.calculate_inundation_cost(i,retreat_h(i),0)                        
                    if self.retreatcost[i] < self.noadaptcost[i]:
                        self.retreat[i]=1


                print('compare retreat,wall',self.retreatcost[i],self.cost(i,retreat_h(i)))
                
                # if s_inter less than zero, cost of wall too great
                # in first period, decide between wall/noadapt or retreat. After that only considerincreases to wall height 
#                if s_inter > 0:
                    # we subsequently here need to calculate cost and benefits of
                    # optimum wall height in this period
#                    self.action[i] = max(self.action[i], s_inter[0] + self.slr[i])
                    # cumulative protection cost
#                    self.protectcost[i] = self.cost(i,self.action[i])
 #                   localcost = self.protectcost[i]
#                elif j==0:
#                    self.noadaptcost[i] = self.calculate_inundation_cost(i,retreat_h(i),0)
##                    self.noadaptcost[i] = self.calculate_inundation_cost(i,self.slr[i],0)
#                    localcost = self.noadaptcost[i]
#                if j == 0 and self.retreatcost[i] < localcost:
#                    print('retreat here')
#                    self.retreat[i] = 1

                # here track what would be optimum if no beta, and check if any region `incorrectly retreated'
                if s_true > 0:
                    self.counteraction[i] = max(self.counteraction[i],s_true + self.slr[i])
                    self.truecost[i] = self.cost(i,self.counteraction[i])
                    if (j == 0) and (self.retreat[i]==1) and (self.retreatcost[i] > self.truecost[i]):
                        self.wrongretreat[i] = 1



    def dcost(self,r,e):
        h = e+self.slr[r]
        return data.pc*float(length(r))*2*h + float(length(r))*data.lv*1.7

    def cost(self,r,e):
        h = e #+self.slr[r]
        return data.pc*float(length(r))*h*h + float(length(r))*data.lv*1.7*h
    
    def g(self,s,r):
        return genextreme.pdf(s,data.c[r],data.loc[r],data.scale[r]) * self.damage(s,r)
                    
    def damage(self,e,r):
        # if surge overtops wall, calculate the damage it causes
        if (e + self.slr[r] - self.action[r]) > 0:
            out = quad(integrand,0,e+self.slr[r],r)
            return out[0]
        else:
            return 0

    # track damage in case optimal wall built
    def alt_damage(self,e,r):
        if (e + self.slr[r] - self.counteraction[r]) > 0:
            out = quad(integrand,0,e+self.slr[r],r)
            return out[0]
        else:
            return 0


        
    def calculate_retreatcost(self):
        for i in range(self.regions):
            a_ = data.a[i]


            movefactor = float(data.scal[0][0])
            capmovefactor = float(data.scal[1][0])
            mobcapfrac = float(data.scal[2][0])
            democost = float(data.scal[3][0])

            depr = 1
            h = retreat_h(i)
#            h = self.slr[i]

            plannedicost = self.calculate_inundation_cost(i,h,depr)
            # retreat cost comprises the actual cost of moving and the cost of inundation of land (assume it is planned and orderly so it is only the land value lost while the capital on the land itself is depreciated
            self.retreatcost[i] = area(h,a_) * (movefactor*(data.sigma_k/3.0) + capmovefactor * mobcapfrac*data.sigma_k + democost*(1-mobcapfrac)*data.sigma_k)
            self.retreatcost[i] = self.retreatcost[i] + plannedicost


    def calculate_inundation_cost(self,i,h,depr):
        a_ = data.a[i]
        return data.lv * area(h,a_) + (1-depr) * data.sigma_k * area(h,a_)

            
    def calculate_actual_damage(self):
        for i in range(self.regions):
            if self.retreat[i] != 1:
                s=flood_rv(i)
                # calculate damage occurred by random surge of s
                self.actual_damage[i] = self.damage(s,i)
                # calculate damage that would have occurred if wall built to `optimal' height
                self.counterdamage[i] = self.counterdamage[i] + self.alt_damage(s,i)
                #print(data.n[i],s,self.actual_damage[i])
                self.total_damage[i] = self.total_damage[i] + self.actual_damage[i]

     
    def calculate_expected_damage(self):
        for i in range(self.regions):
            if self.retreat[i] != 1:
                self.expected_damage[i] = self.true_expect[i] * self.beta[i]
                #print('expected',data.n[i],self.expected_damage[i])


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
            self.meanflood[region] = genextreme.stats(data.c[region],data.loc[region],data.scale[region],moments='m')

    def update(self):
        for iter in range(self.n_iterations):
            print('**********************************')
            print('iteration',iter)
            print('**********************************')
            self.decide_action(iter)
            self.calculate_actual_damage()
            self.calculate_expected_damage()
            self.update_slr(iter+1)
            for i in range(self.regions):
                if iter==0:
                    #print(self.calculate_inundation_cost(i,self.slr[i],0) - self.dcost(i,0),self.dcost(i,0), '**alert**')
                    print(data.n[i],':(beta = %.2f)' %(self.beta[i]))
                    if self.protectcost[i]>0:
                        print('\t\t\t\t wall cost: %.2f' %(self.protectcost[i]))
                    else:
                        print('\t\t\t\t wall cost: too expensive',self.cost(i,retreat_h(i)))
#                        print('\t\t\t\t wall cost: too expensive',self.cost(i,self.slr[i]))                   
                        print('\t\t\t\t no-adapt cost: %.2f' %(self.noadaptcost[i]))
                    print('\t\t\t\t retreat cost: %.2f' %(self.retreatcost[i]))
                    if self.retreat[i]>0:
                        print('\t\t\t\t Decision: Retreat')
                    else:
                        if self.protectcost[i]>0:
                            print('\t\t\t\t Decision: Build wall of height: %.2f' %(self.action[i]))
                            print(iter)
                        else:
                            print('\t\t\t\t Decision: chance on')
                elif self.retreat[i] != 1:
                    print(data.n[i],':(beta = %.2f)' %(self.beta[i]))
                    print('\t\t\t\t Decision: cumulative wall height: %.2f' %(self.action[i]))
                    print('\t\t\t\t Decision: cumulative wall cost: %.2f' %(self.protectcost[i]))
            self.update_beta()
# to here
            
        for i in range(self.regions):
            if self.retreat[i]>0:
                if self.wrongretreat[i]==0:
                    print(data.n[i],' no costs incurred due to beta (retreated when should have retreated)')
                else:
                    print(data.n[i],' retreated when should not have retreated at cost %.2f' %(self.retreatcost[i]-self.truecost[i]))
            elif self.truecost[i] < self.protectcost[i]:
                print(data.n[i],' overbuilt protection at cost %.2f' %(self.protectcost[i] - self.truecost[i]))
            else:
                print(data.n[i],' underbuilt protection at cost from realised flooding relative to counter %.2f' %(self.total_damage[i] - self.counterdamage[i]))
        print(self.wrongretreat)
                
        print(self.truecost)




#parameters:(beta, number of iterations)
arg=sys.argv
ar_1 = adaptretreat(float(arg[1]),1)
print(arg)
ar_1.populate()
ar_1.update()
#print('[0 = no action, 1 = action]'



# remember basically have to put in the last graph I sent melanie. each region decide what to do based on that. but imperfect decision due to \beta. put in mechanism to update that then also, maybe just a heuristic it inches up if wave is higher than the mean they are expecting. there is probably a fancier formula for doing that - surely Bayes?!







