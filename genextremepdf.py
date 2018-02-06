
def val(s):
        return genextreme.pdf(s,-xi,mu,sigma)


Iorras region    
xi=0.206
mu=0.063
sigma=.036




quad(val,0,.1)


#check what fraction of probabilty dist is below 0.1
#quad(val,0,.1)
