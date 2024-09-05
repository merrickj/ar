for i in range(0,29):
    floodl = flood_gev(i) # this can be replaced with other functions in mvp
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
    print('damage to region, ',n[i],' from flood level ',flood,' is ', ans_c, 'M$')
    print('\t\t\t\t %.2fm sea level rise is %.2f million $' %(lb,ans_c))


for i in range(0,29):
    floodl = flood_gev(i)
    meanflood = float(floodl[1])
    ans_m,err_m = quad(integrand,0,meanflood,i)
    print('mean damage to region %s from mean flood level %.2fm on top of:'%(n[i],meanflood))
    for l in range(0,3):
        if l==0:
            lb = float(rcp[i][0])
        elif l==1:
            lb = float(rcp[i][1])
        else:
            lb = float(rcp[i][2])

        ans_m = damage(lb,lb+meanflood,i)
        print('\t\t\t\t%.2fm sea level rise is %.2f million $' %(lb,ans_m))
#    print('cost of wall for max case is %.2f million $' %(cost(i,lb+meanflood)))


# now we want to plot g(s) in our notation
import sys

if len(sys.argv) == 2:
    r_temp = int(sys.argv[1])
else:
    print("Select region by order, e.g. 'python3 gev.py 1'")
    sys.exit()

c_temp = -float(fg[r_temp][2])
loc_temp = float(fg[r_temp][0])
scale_temp = float(fg[r_temp][1])
floodl = flood_gev(r_temp)
meanflood = float(floodl[1])
lb_temp=float(rcp[r_temp][2])


import numpy as np
xxa=np.arange(20.0)
xxa_eile=np.arange(20.0)
yya=np.arange(20.0)
yya_eile=np.arange(20.0)
cy=np.zeros(20)
for xx in range(0,20,1):
    level=xx*.05
    yy = g(level,lb_temp,r_temp)
    yy_eile = g(level,lb_temp,r_temp) + 0.04*inundcost(r_temp,lb_temp,0)
    xxa[xx]=float(level)
    xxa_eile[xx]=float(level)+lb_temp
    yya[xx]=float(yy)
    yya_eile[xx]=float(yy_eile)    

#    cy[xx] = dcost(r_temp,level+lb_temp)
    cy[xx] = dcost(r_temp,level+lb_temp)

from scipy.optimize import fsolve
s_inter = fsolve(f,meanflood*3)
#note that the actual amount built should be s_inter+lslr (same as dcost calculated) [that is, graph shows
# ok, this can be basis..
print('retreat cost would be',retreatcost(r_temp,2+lb_temp))
print('inundation cost would be with depreciation',inundcost(r_temp,2+lb_temp,1))
print('inundation cost would be with no depreciation',inundcost(r_temp,2+lb_temp,0))
print('inundation cost slr',inundcost(r_temp,lb_temp,0))
print('wall cost slr',cost(r_temp,lb_temp))
print('wall cost would be',cost(r_temp,s_inter+lb_temp))
print('intersection s is',s_inter)

print('expected damages', expected_damage(lb_temp,r_temp))

import matplotlib.pyplot as plt

plt.scatter(xxa,yya)
plt.plot(xxa,yya)
#plt.scatter(xxa,yya_eile)
#plt.plot(xxa,yya_eile)
#plt.scatter(xxa,yya_eile)
#plt.plot(xxa,yya_eile)

print('s_inter',s_inter)
print('dcost',dcost(r_temp,s_inter+lb_temp), 'g',g(s_inter,lb_temp,r_temp))
#,'icost',0.04*inundcost(r_temp,lb_temp,0)
print('lb_temp',lb_temp)

plt.plot(xxa,cy)
#plt.scatter(s_inter+lb_temp,dcost(r_temp,s_inter+lb_temp),color='r',marker='x',s=200,linewidths=3)
plt.scatter(s_inter,dcost(r_temp,s_inter),color='r',marker='x',s=200,linewidths=3)
plt.title(n[r_temp])
plt.xlabel("metres")
plt.ylabel("millions of $")
plt.xlim(-.1,1.1)

# uncomment to show plot
plt.show()

# uncomment to save plot
#name = 'fig/'+str(n[r_temp])+'.png'
#plt.savefig(name)
    




import sys
sys.exit()




#from solvefixed.gms:
#Costs(retreatGrid,seg,t,'relocation')$xtat(t,at) = [tstept/tstep(at)]*sum(xtat(t,at), pos([coastareaA(R,at,seg,retreatGrid)] - [coastareaA(R,at-1,seg,retreatGrid)]) * [movefactor*ypc(at,seg)*1e-6*popdens(at,seg) + capmovefactor*mobcapfrac*capital(at,seg) + democost*(1-mobcapfrac)*capital(at,seg)]);

#note ypc*1e-6*popdens = capital / 3


# when calling damage in integrated file, have to make sure self.action = 0 in gev mode


# to be deleted once removed below
def flood_gev(r):
    c = -float(fg[r][2])
    loc = float(fg[r][0])
    scale = float(fg[r][1])
    out = []
    out.append(genextreme.rvs(c,loc,scale))
    out.append(genextreme.stats(c,loc,scale,moments='m'))
    return out
