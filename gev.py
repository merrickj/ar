a=[]
p=[]
s=[]
k=[]
fg=[]
n=[]
rcp=[]


import csv
with open('ireland_input.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        a.append(row)

with open('ireland_popdens.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        p.append(row)


with open('ireland_seg.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        s.append(row)

#the cap csv is ok, must have been sorted at some point
with open('ireland_cap_1.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        k.append(row)

#ok too, must have been sorted
with open('flood_gev.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        fg.append(row)
#also ok
with open('ainmneacha.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        n.append(row)

with open('rcp_ie.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        rcp.append(row)


from scipy.stats import genextreme

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

def flood_gev(r):
    c = -float(fg[r][2])
    loc = float(fg[r][0])
    scale = float(fg[r][1])
    out = []
    out.append(genextreme.rvs(c,loc,scale))
    out.append(genextreme.stats(c,loc,scale,moments='m'))
    return out



import math
#to integrate the function x**2 between 0 and 1
from scipy.integrate import quad


#what happened area15?
def area(y,a_):
    a=[]
    for i in range(0,15):
        temp=float(a_[i])
        a.append(temp)

    return a[0]*max(0,min(0.5,y))+(a[1]+a[0])/2*max(0,min(1,y-0.5))+a[1]*max(0,min(0.5,y-1.5))+a[2]*max(0,min(1,y-2))+a[3]*max(0,min(1,y-3))+a[4]*max(0,min(1,y-4))+a[5]*max(0,min(1,y-5))+a[6]*max(0,min(1,y-6))+a[7]*max(0,min(1,y-7))+a[8]*max(0,min(1,y-8))+a[9]*max(0,min(1,y-9))+a[10]*max(0,min(1,y-10))+a[11]*max(0,min(1,y-11))+a[12]*max(0,min(1,y-12))+a[13]*max(0,min(1,y-13))+a[14]*max(0,y-14)


def psi(e):
    e = e/1.0
    return e/(1+e);

def integrand(e,r):
    sigma_k = float(k[r][0]);
    vsl = 9.444821238556;
    mu = 0.01;
    sigma_l = float(p[r][0]);
    rho = 0.518144214230081;
    a_ = a[r];
    return (1-rho)*area(e,a_)*(sigma_k*psi(e)+sigma_l*vsl*mu)


def damage(lb,e,r):
    out = quad(integrand,lb,e,r)
    return out[0]

def g(lb,s,r):
    c_temp = -float(fg[r][2])
    loc_temp = float(fg[r][0])
    scale_temp = float(fg[r][1])
    return genextreme.pdf(s,c_temp,loc_temp,scale_temp) * damage(lb,s+lb,r)



def f(s):
#    print 'cost:',cost
    return g(float(rcp[r_temp][2]),s,r_temp) - dcost(r_temp,s+lb_temp)

def length(r):
    al = a[r]
    return al[16]
#    print 'length', length


def cost(r,h):
    pc = 7.7598    
    return pc*float(length(r))*h*h

def dcost(r,h):
    pc = 7.7598    
    return pc*float(length(r))*2*h
    


for i in range(0,29):
    floodl = flood_gev(i)
    flood = float(floodl[0])
    meanflood = float(floodl[1])
    for l in range(0,3):
        if l==0:
            lb = float(rcp[i][0])
        elif l==1:
            lb = float(rcp[i][1])
        else:
            lb = float(rcp[i][2])

        ans_c = damage(lb,lb+flood,i)
    print 'damage to region, ',n[i],' from flood level ',flood,' is ', ans_c, 'M$'
    print '\t\t\t\t %.2fm sea level rise is %.2f million $' %(lb,ans_c)


for i in range(0,29):
    floodl = flood_gev(i)
    meanflood = float(floodl[1])
    ans_m,err_m = quad(integrand,0,meanflood,i)
    print 'mean damage to region %s from mean flood level %.2fm on top of:'%(n[i],meanflood)
    for l in range(0,3):
        if l==0:
            lb = float(rcp[i][0])
        elif l==1:
            lb = float(rcp[i][1])
        else:
            lb = float(rcp[i][2])

        ans_m = damage(lb,lb+meanflood,i)
        print '\t\t\t\t%.2fm sea level rise is %.2f million $' %(lb,ans_m)
#    print 'cost of wall for max case is %.2f million $' %(cost(i,lb+meanflood))


# now we want to plot g(s) in our notation
import sys
r_temp = int(sys.argv[1])
c_temp = -float(fg[r_temp][2])
loc_temp = float(fg[r_temp][0])
scale_temp = float(fg[r_temp][1])
floodl = flood_gev(r_temp)
meanflood = float(floodl[1])
lb_temp=float(rcp[r_temp][2])



import numpy as np
xxa=np.arange(20.0)
yya=np.arange(20.0)
cy=np.zeros(20)
for xx in range(0,20,1):
    level=xx*.05
    yy = g(lb_temp,level,r_temp)
    xxa[xx]=float(level)
    yya[xx]=float(yy)

    cy[xx] = dcost(r_temp,level+lb_temp)


from scipy.optimize import fsolve
s_inter = fsolve(f,meanflood*3)


print 'intersection s is',s_inter



import matplotlib.pyplot as plt

plt.scatter(xxa,yya)
plt.plot(xxa,yya)


plt.plot(xxa,cy)
plt.scatter(s_inter,dcost(r_temp,s_inter+lb_temp),color='r',marker='x',s=200,linewidths=3)
plt.title(n[r_temp])
plt.xlabel("metres")
plt.ylabel("millions of $")
plt.xlim(-.1,1.1)

# uncomment to show plot
#plt.show()

# uncomment to save plot
name = 'fig/'+str(n[r_temp])+'.png'
plt.savefig(name)
    




import sys
sys.exit()




