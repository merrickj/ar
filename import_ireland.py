import csv

class IrelandClass(object):

    a=[]
    p=[]
    s=[]
    k=[]
    fg=[]
    n=[]
    rcp=[]
    scal=[]



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

# will go with 45 for now
    with open('rcp45.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            rcp.append(row)

    with open('ireland_scalars.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            scal.append(row)

    vsl = 9.444821238556;
    mu = 0.01;
    rho = 0.518144214230081;


    ln = len(n)
    c = [0 for x in range(ln)]
    loc = [0 for x in range(ln)]
    scale = [0 for x in range(ln)]
#    for i in range(len(n)):
    for i in range(ln):
        c[i] = -float(fg[i][2])
        loc[i] = float(fg[i][0])
        scale[i] = float(fg[i][1])

    pc = 7.7598
    lv = 5.376
    sigma_k = float(k[i][0]);    
    
        
data = IrelandClass()

def integrand(e,region):
    sigma_k = float(data.k[region][0]);
    sigma_l = float(data.p[region][0]);
    a_ = data.a[region];
    return (1-data.rho)*area(e,a_)*(sigma_k*psi(e)+sigma_l*data.vsl*data.mu)

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
    al = data.a[r]
    return al[16]
        

def slr(region,time):
    return float(data.rcp[region][time])

