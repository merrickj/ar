a=[]
p=[]
s=[]
k=[]
fg=[]
n=[]
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

with open('ireland_cap_1.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        k.append(row)

with open('flood_gev.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        fg.append(row)

with open('ainmneacha.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        n.append(row)


from scipy.stats import genextreme
#c=-.5
#loc=1
#scale=.1
#Note c is negative of Delavane's xi parameter
#print genextreme.rvs(c,loc,scale)

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
    out.append(genextreme.rvs(c,loc,scale)/scale)
    out.append(genextreme.stats(c,loc,scale,moments='m')/scale)
    return out

#flood=genextreme.rvs(c,loc,scale)/sigma
#print 'Ireland8515 flood level (m):'
#print 'actual ',genextreme.rvs(c,loc,scale),'mean:', genextreme.stats(c,loc,scale,moments='m')
#print 'actual alt', flood , 'mean alt:', ((genextreme.stats(c,moments='m')*sigma) + mu)/sigma

#see note above about dividing by sigma here
import math
x=.0923
#gpdf = ((1+(x-mu)/sigma*xi)**(-1/xi))**(xi+1)*math.exp(-1*(1+(x-mu)/sigma*xi)**(-1/xi))/sigma
#gcdf = math.exp(-1*(1+(x-mu)/sigma*xi)**(-1/xi))
#print 'gpdf: ',gpdf, 'gcdf: ',gcdf



#to integrate the function x**2 between 0 and 1
from scipy.integrate import quad

#def integrand(x):
#    return x**2

#ans,err = quad(integrand,0,1)
#print 'test integral ', ans

#,seg,segid,s1,s10,s100,s1000,smax,longi,lati,slopecst,uplift,area1,area2,area3,area4,area5,area6,area7,area8,area9,area10,area11,area12,area13,area14,area15,area16,length,h0,pop,popdens,wetland,iso,countrylongname,FUNDregion,ypc_scale,cci,gtapland

#56.674,3.96,28351,110.547,0,IRL,Ireland,WEU,1,1.289,0.619785455

#a_cooley=[64,6,2,3,1,5.333333333,5.333333333,5.333333333,3,3,3,3,3.25,3.25,3.25,3.25];
#print a_cooley[15]

#what happened area15?
def area(y,a_):
    a=[]
    for i in range(0,15):
        temp=float(a_[i])
        a.append(temp)

    return a[0]*max(0,min(0.5,y))+(a[1]+a[0])/2*max(0,min(1,y-0.5))+a[1]*max(0,min(0.5,y-1.5))+a[2]*max(0,min(1,y-2))+a[3]*max(0,min(1,y-3))+a[4]*max(0,min(1,y-4))+a[5]*max(0,min(1,y-5))+a[6]*max(0,min(1,y-6))+a[7]*max(0,min(1,y-7))+a[8]*max(0,min(1,y-8))+a[9]*max(0,min(1,y-9))+a[10]*max(0,min(1,y-10))+a[11]*max(0,min(1,y-11))+a[12]*max(0,min(1,y-12))+a[13]*max(0,min(1,y-13))+a[14]*max(0,y-14)

#print 'cooley area flooded', area(flood,a_cooley)


#sigma_k_cooley = 14.43628151582;
#vsl = 9.444821238556;
#rho = 0.518144214230081;



def psi(e):
    return e/(1+e);

def damage(e,r):
    sigma_k = float(k[r][0]);
    vsl = 9.444821238556;
    mu = 0.01;
    sigma_l = float(p[r][0]);
    rho = 0.518144214230081;
    a_ = a[r];
    return (1-rho)*area(e,a_)*(sigma_k*psi(e)+sigma_l*vsl*mu)



#print 'damage_snap', damage(flood)

def integrand(e,r):
#    r=rgn
    return damage(e,r)

#global rgn
#for i in range(0,28):
for i in range(0,29):
#    rgn=i
    floodl = flood_gev(i)
    flood = float(floodl[0])
    meanflood = float(floodl[1])
    ans_c,err_c = quad(integrand,0,flood,i)

#print 'test integral, err_c', ans_c, err_c 
#    print 'damage to region, ',n[rgn],' from flood level ',flood,' is ', ans_c, 'M$'
    print 'damage to region %s from flood level %.2fm is %.2f million $' %(n[i],flood,ans_c)

#    print a[rgn]
#    print s[rgn]
#    print p[rgn]
#    print k[rgn]

for i in range(0,29):
#    rgn=i
    floodl = flood_gev(i)
    meanflood = float(floodl[1])
#    print meanflood
    ans_m,err_m = quad(integrand,0,meanflood,i)
    print 'mean damage to region %s from mean flood level %.2fm is %.2f million $' %(n[i],meanflood,ans_m)









