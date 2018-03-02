a=[]
p=[]
s=[]
k=[]
fg=[]
n=[]
rcp=[]
scal=[]


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

with open('ireland_scalars.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        scal.append(row)
        

def integrand(e,region):
    sigma_k = float(k[region][0]);
    sigma_l = float(p[region][0]);
    vsl = 9.444821238556;
    mu = 0.01;
    rho = 0.518144214230081;        
    a_ = a[region];
    return (1-rho)*area(e,a_)*(sigma_k*psi(e)+sigma_l*vsl*mu)

def area(y,a_):
    a=[]
    for i in range(0,15):
        temp=float(a_[i])
        a.append(temp)
    return a[0]*max(0,min(0.5,y))+(a[1]+a[0])/2*max(0,min(1,y-0.5))+a[1]*max(0,min(0.5,y-1.5))+a[2]*max(0,min(1,y-2))+a[3]*max(0,min(1,y-3))+a[4]*max(0,min(1,y-4))+a[5]*max(0,min(1,y-5))+a[6]*max(0,min(1,y-6))+a[7]*max(0,min(1,y-7))+a[8]*max(0,min(1,y-8))+a[9]*max(0,min(1,y-9))+a[10]*max(0,min(1,y-10))+a[11]*max(0,min(1,y-11))+a[12]*max(0,min(1,y-12))+a[13]*max(0,min(1,y-13))+a[14]*max(0,y-14)

def psi(e):
    e = e/1.0
    return e/(1+e)

def length(r):
    al = a[r]
    return al[16]
        
def flood_rv(region):
    c = -float(fg[region][2])
    loc = float(fg[region][0])
    scale = float(fg[region][1])
    return genextreme.rvs(c,loc,scale)
#        return genextreme.rvs(c(region),loc(region),scale(region))


def slr(region):
    return float(rcp[region][2])
