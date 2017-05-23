#updated mvp_Ireland. MC attempt. Keyword- attempt. 
#based on mvp_ireland.py J Merrick

import random
import sys
from scipy.stats import genextreme #for flood distribution
from scipy.integrate import quad #for damage function
from import_ireland2 import * #imports everything from the import_ireland2 script
#vsl, mu, rho, a[] area, p[] population density, s[] ireland segments, k[] capital parameters, fg[] flood distribution parameters, n[] ??
#additionally should import: alpha, mc for the wall in each region could change to cst[]. s_bar will be sb[] pulled from some csv (?) where it's different for each region. Or start with it all the same s_bar gets imported then. Could also define them here for now(?)

class adaptretreat: 
    def _init_(self, n_iterations): 
        self.regions=29
        self.n_iterations=n_iterations #input as an argument when we run adaptretreat. 
        #I think we don't initialise s_bar and instead read it in for each region
        self.action=[] #0 if retreat, 1 if adapt
        self.add_wall=[]
        self.wall_height=[]
        self.incurred_damage=[]
        self.adapt_cost=[]
        self.expected_cost=[]
        self.retreat_cost=[] #do I need to create this here?
        self.cost_wall=[]
        
    def populate(self):
        self.action=[1 for x in range(self.regions)] #Everyone starts of possibly adapting
        self.incurred_damage=[0 for x in range(self.regions)] #start off with zero damage incurred
        #there's more to go in here, but I'm unsure what at this point
        self.add_wall=[0 for x in range(self.regions)]
        self.wall_height=[0 for x in range(self.regions)]

    def retreat_cost(self, region):
        self.retreat_cost=float(rtcst[region][0])
    
    def choose(self): #If it's less costly to adapt, adapt. If more, retreat. If equal, resolve indifference to stay. 
        for i in range(self.regions):
            if self.adapt_cost[i]<=self.retreat_cost[i]: #unsure of syntax as haven't defined the costs yet
                self.action[i]=1
                else:
                    self.action[i]=0

    def flood_rv(self, region):
        c= -float(fg[region][2])
        loc= float(fg[region][0])
        scale= float(fg[region][1])
        return genextreme.rvs(c,loc,scale)/scale 
    #Keep same code as I think we want the same flood rvs?

    def damage(self,e,region):
        #either delavane function calculated from bottom up (more work) or something simpler that I have not worked out yet
        sigma_k = float(k[region][0]);
        sigma_l = float(p[region][0]);
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
    
    def solve_min_cost(self):
        #

        
    def cost_wall(self):
        for i in range(self.regions):
            self.cost_wall[i]=alpha*self.add_wall[i] #assuming no fixed cost and that it's just MC*amount built. 
        
    def adapt_cost(self):

    def s_bar(self, region):
        s_bar=float(sb[region][0]) #if we go the make csv and pull the same way we did with fg, for example, route? is this the right syntax for this?

    #def update_s_bar(self):
       # for i in range(self.regions):
        #    self.s_bar[i]=
        
    def wall_height(self):
        for i in range(self.regions):
            self.wall_height[i]=self.wall_height[i]+self.add_wall[i]
    
    def incurred_cost(self): 
    
    def update(self):
        for iter in range(self.n_iterations):
            self.update_s_bar() #need an s_bar update function
            self.solve_min_cost() #first solve for min cost 
            self.wall_height() #figure out what the wall height will be
            self.adapt_cost() #calculate an adaptation cost
            self.choose() #compare costs to choose 
            self.incurred_cost() #incur costs according to choice
            if sum(self.action)==0: #leave algorithm if everyone has retreated, otherwise iterate through to n_iterations
                break 



                    
