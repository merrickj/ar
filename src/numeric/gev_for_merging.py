




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
