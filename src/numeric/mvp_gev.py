# James Merrick, May 2018
# Developed from minimum viable product of adapt/retreat model, and following discussions at Stanford University, April+May 2018

# James Merrick, September 2024
# merge numeric_b (gev.py) into this structure
# first step just allow a toggle between, should reproduce what a and b reproduce independently


# Data from Ireland for this first version
# this version leaves the dynamics aside for now. We here assume a one period decision. 
# First year SLR is coming, and associated flooding, what are you going to do?
# will include plotting for each region here too
# a few things were missing from discussion with MC - a) [what was on edge of my mind] if retreat option how deal with flood risk b) if doing some sort of aggregate period decision, how deal with multiple years of flooding

import random
import sys
import json
import io
import matplotlib.pyplot as plt
import numpy as np

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
        # note in gev.py the second term here was not there, ie.zero
        return data.pc*float(length(r))*2*h + float(length(r))*data.lv*1.7

    def cost(self,r,e):
        h = e #+self.slr[r]
        # note in gev.py the second term here was not there, ie.zero
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
        # note in gev.py version of this function there is no plannedicost
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
        with open('../../data/true.json') as data_file:
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






arg = sys.argv

if arg[1] != "GEV":
        
    #parameters:(beta, number of iterations)
    if len(arg) == 2:
        ar_1 = adaptretreat(float(arg[1]),1)
        print("currently hard coded to run for 1 iteration")
    else:
        print("please enter beta parameter as 1st argument")
        print("e.g. python3 mvp.py 1")
        print("(note currently hard coded for 1 iteration, so second argument not needed)")
        sys.exit()
    print(arg)
    ar_1.populate()
    ar_1.update()
    print('(0 = no action, 1 = action)')

else:

    rcp_gev = []
    with open('../../data/rcp_ie.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rcp_gev.append(row)
    
    def g_gev(s,lb,r):
        return genextreme.pdf(s,data.c[r],data.loc[r],data.scale[r]) * quad(integrand,0,s+lb,r)[0]
    def g_eile_gev(s,r):
        lb = float(rcp_gev[r][0])
        return g_gev(s,lb,r)
    
    def dcost_gev(r,h):
        return data.pc*float(length(r))*2*h
    def f_gev(s):
        return g_gev(s,float(rcp_gev[r_temp][2]),r_temp) - dcost_gev(r_temp,s+lb_temp)
    def retreatcost_gev(r,h):
        a_ = data.a[r]

        movefactor = float(data.scal[0][0])
        capmovefactor = float(data.scal[1][0])
        mobcapfrac = float(data.scal[2][0])
        democost = float(data.scal[3][0])

        return area(h,a_) * (movefactor*(data.sigma_k/3.0) + capmovefactor * mobcapfrac*data.sigma_k + democost*(1-mobcapfrac)*data.sigma_k)

    def inundcost_gev(r,h,depr):
        a_ = data.a[r]

        return data.lv * area(h,a_) + (1-depr) * data.sigma_k * area(h,a_)

    def cost_gev(r,h):
        return data.pc * float(length(r)) * h * h



    
    for i in range(0,29):
        flood = float(genextreme.rvs(data.c[i],data.loc[i],data.scale[i]))
        meanflood = float(genextreme.stats(data.c[i],data.loc[i],data.scale[i],moments='m'))

        for l in range(0,3):
            if l==0:
                lb = float(rcp_gev[i][0])
            elif l==1:
                lb = float(rcp_gev[i][1])
            else:
                lb = float(rcp_gev[i][2])
                
            ans_c = quad(integrand,lb,lb+flood,i)[0]

        print('damage to region, ',data.n[i],' from flood level ',flood,' is ', ans_c, 'M$')
        print('\t\t\t\t %.2fm sea level rise is %.2f million $' %(lb,ans_c))

    for i in range(0,29):
        meanflood = float(genextreme.stats(data.c[i],data.loc[i],data.scale[i],moments='m'))        
        ans_m,err_m = quad(integrand,0,meanflood,i)
        print('mean damage to region %s from mean flood level %.2fm on top of:'%(data.n[i],meanflood))
        for l in range(0,3):
            if l==0:
                lb = float(rcp_gev[i][0])
            elif l==1:
                lb = float(rcp_gev[i][1])
            else:
                lb = float(rcp_gev[i][2])

            ans_m = quad(integrand,lb,lb+meanflood,i)[0]
            print('\t\t\t\t%.2fm sea level rise is %.2f million $' %(lb,ans_m))
            #    print('cost of wall for max case is %.2f million $' %(cost(i,lb+meanflood)))


    # now we want to plot g(s) in our notation
    if len(arg) == 3:
        r_temp = int(arg[2])
    else:
        print("Select region by order, e.g. 'python3 mvp_gev.py GEV 1'")
        sys.exit()

    c_temp = data.c[r_temp]
    loc_temp = data.loc[r_temp]
    scale_temp = data.scale[r_temp]
    meanflood = float(genextreme.stats(c_temp,loc_temp,scale_temp,moments='m'))        
    lb_temp = float(rcp_gev[r_temp][2])


    xxa=np.arange(20.0)
    xxa_eile=np.arange(20.0)
    yya=np.arange(20.0)
    yya_eile=np.arange(20.0)
    cy=np.zeros(20)

    for xx in range(0,20,1):
        level=xx*.05
        yy = g_gev(level,lb_temp,r_temp)

        xxa[xx]=float(level)
        yya[xx]=float(yy)

        cy[xx] = dcost_gev(r_temp,level+lb_temp)

    s_inter = fsolve(f_gev,meanflood*3)

    # TEMP removal of below print statements 9/9/24 
    
    #note that the actual amount built should be s_inter+lslr (same as dcost calculated) [that is, graph shows
    # ok, this can be basis..
    print('retreat cost would be',retreatcost_gev(r_temp,2+lb_temp))
    print('inundation cost would be with depreciation',inundcost_gev(r_temp,2+lb_temp,1))
    print('inundation cost would be with no depreciation',inundcost_gev(r_temp,2+lb_temp,0))
    print('inundation cost slr',inundcost_gev(r_temp,lb_temp,0))
    print('wall cost slr',cost_gev(r_temp,lb_temp))
    print('wall cost would be',cost_gev(r_temp,s_inter+lb_temp))
    print('intersection s is',s_inter)

    print('expected damages', quad(g_eile_gev,0,5,r_temp)[0])



    plt.scatter(xxa,yya)
    plt.plot(xxa,yya)

    # TEMP removal of below print statements 9/9/24 
    print('s_inter',s_inter)
    print('dcost',dcost_gev(r_temp,s_inter+lb_temp), 'g',g_gev(s_inter,lb_temp,r_temp))
    #,'icost',0.04*inundcost(r_temp,lb_temp,0)
    print('lb_temp',lb_temp)

    plt.plot(xxa,cy)
    ##plt.scatter(s_inter+lb_temp,dcost(r_temp,s_inter+lb_temp),color='r',marker='x',s=200,linewidths=3)
    plt.scatter(s_inter,dcost_gev(r_temp,s_inter),color='r',marker='x',s=200,linewidths=3)
    plt.title(data.n[r_temp])
    plt.xlabel("metres")
    plt.ylabel("millions of $")
    plt.xlim(-.1,1.1)

    # uncomment to show plot
    plt.show()

# uncomment to save plot
#name = 'fig/'+str(n[r_temp])+'.png'
#plt.savefig(name)
    

    sys.exit()





# remember basically have to put in the last graph I sent melanie. each region decide what to do based on that. but imperfect decision due to \beta. put in mechanism to update that then also, maybe just a heuristic it inches up if wave is higher than the mean they are expecting. there is probably a fancier formula for doing that - surely Bayes?!











####
# notes below taken from gev.py
####

#Note c is negative of Delavane's xi parameter
# https://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.stats.genextreme.html

#Notes

#For c=0, genextreme is equal to gumbel_r. The probability density function for genextreme is:

#genextreme.pdf(x, c) =
#    exp(-exp(-x))*exp(-x),                    for c==0
#    exp(-(1-c*x)**(1/c))*(1-c*x)**(1/c-1),    for x <= 1/c, c > 0
#Note that several sources and software packages use the opposite convention for the sign of the shape parameter c.

#genextreme takes c as a shape parameter.

##The probability density above is defined in the `standardized' form. To shift and/or scale the distribution use the loc and scale parameters. Specifically, genextreme.pdf(x, c, loc, scale) is identically equivalent to genextreme.pdf(y, c) / scale with y = (x - loc) / scale.
# this latter point however does not account for a further scaling factor Delavane has in her paper. she divides by sigma. This seems to bring surge from fraction of meter to meters


#So for Ireland8502 and 8515
#   r            mu         sigma     xi        
#Ireland8502 0.06265796 0.03573306 0.2064354 
#Ireland8515 0.06157673 0.03526684 0.2098331

#xi=0.2098331
#sigma=0.03526684
#mu=0.06157673

#c = -xi
#loc = mu
#scale = sigma
