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

xi=0.2064354
sigma=0.03573306
mu=0.06265796

c = -xi
loc = mu
scale = sigma

print 'Ireland8502 flood level (m):'
print genextreme.rvs(c,loc,scale)/sigma
print 'mean', genextreme.stats(c,loc,scale,moments='m')
print 'mean', ((genextreme.stats(c,moments='m')*sigma) + mu)/sigma

#see note above about dividing by sigma here
import math
x=.0923
gpdf = ((1+(x-mu)/sigma*xi)**(-1/xi))**(xi+1)*math.exp(-1*(1+(x-mu)/sigma*xi)**(-1/xi))/sigma
gcdf = math.exp(-1*(1+(x-mu)/sigma*xi)**(-1/xi))
print gpdf, gcdf



#to integrate the function x**2 between 0 and 1
from scipy.integrate import quad

def integrand(x):
    return x**2

ans,err = quad(integrand,0,1)
print ans

