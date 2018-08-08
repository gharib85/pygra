# generates diffeent types of klist

import numpy as np

def default(g,nk=400):
  """ Input is geometry"""
  if g.dimensionality == 2:
    b1 = np.array([1.,0.])
    b2 = np.array([0.,1.])
#    b2 = np.array([.5,np.sqrt(3)/2])
#    b2 = np.array([0.,-1.])
    fk = open("klist.in","w")  
    fk.write(str(nk)+"\n") # number of kpoints
    k = np.array([0.,0.]) # old kpoint
    kout= []
    for i in range(nk):
      k += (b1+b2) /(nk) # move kpoint 
      fk.write(str(k[0])+"   "+str(k[1])+"\n    ")
      kout.append(k.copy()) # store in array
    fk.close()
    # write bandlines
    fbl = open("BANDLINES.OUT","w")
    fbl.write("0   \Gamma\n")
    fbl.write(str(nk/3)+"   K\n")
    fbl.write(str(nk/2)+"   M\n")
    fbl.write(str(2*nk/3)+"   K'\n")
    fbl.write(str(nk)+"   \Gamma\n")
    fbl.close()
    return kout






def gen_default(k):
  """ Return a function which generates the path"""
  b1 = np.array([1.,0.])
  b2 = np.array([0.,1.])
  return k*(b1+b2) # return kpoint 




def kx(g,nk=400):
  """ Input is geometry"""
  if g.dimensionality == 2:
    b1 = np.array([1.,0.])
    b2 = np.array([0.,1.])
    fk = open("klist.in","w")  
    fk.write(str(nk)+"\n") # number of kpoints
    k = -b1/2 # old kpoint
    kout= []
    for i in range(nk):
      k += (b1) /(nk) # move kpoint 
      fk.write(str(k[0])+"   "+str(k[1])+"\n    ")
      kout.append(k) # store in array
    fk.close()
    # write bandlines
    fbl = open("BANDLINES.OUT","w")
    fbl.write("0   X_1\n")
    fbl.write(str(nk/2)+"   \Gamma\n")
    fbl.write(str(nk)+"   X_1\n")
    fbl.close()



def tr_path(nk=100,d=20,write=True):
  """ Creates the special path to calculate the Z2 invariant"""
  # d is the number of divisions
  w = 1.0/8 # heigh of the path
  ks = [] # initialice list
  dk = 1./nk 
  # full path
  ks += [[il,.5/d] for il in np.arange(-.5-dk,.5/d,dk)] 
  ks += [[.5/d,il] for il in np.arange(.5/d,0-dk,-dk)] 
  ks += [[il,0.-dk] for il in np.arange(.5/d,(d-1)*.5/d,dk)] 
  ks += [[(d-1)*.5/d,il] for il in np.arange(0.-dk,.5/d,dk)] 
  ks += [[il,.5/d] for il in np.arange((d-1)*.5/d,.5+dk,dk)] 
  ks += [[.5+dk,il] for il in np.arange(.5/d,(d-1)*.5/d,dk)] 
  ks2 = [[-k[0],.5-k[1]] for k in ks]
  ks = ks + ks2 # sum the two lists
  if write:
    f = open("klist.in","w")
    f.write(str(len(ks))+"\n") # number of kpoints
    for k in ks:
      f.write(str(k[0]) + "  ")
      f.write(str(k[1]) + "\n")
    f.close()



def tr_klist(nk=100,d=20):
  """ Creates the special path to calculate the Z2 invariant"""
  # d is the number of divisions
  w = 1.0/8 # heigh of the path
  lks = [] # initialice list
  dk = 1./nk 
  # full path
  class ks_class: pass
  ks = ks_class() # create object
  lks += [[il,.5/d] for il in np.arange(-.5-dk,.5/d,dk)] 
  lks += [[.5/d,il] for il in np.arange(.5/d,0-dk,-dk)] 
  lks += [[il,0.-dk] for il in np.arange(.5/d,(d-1)*.5/d,dk)] 
  lks += [[(d-1)*.5/d,il] for il in np.arange(0.-dk,.5/d,dk)] 
  lks += [[il,.5/d] for il in np.arange((d-1)*.5/d,.5+dk,dk)] 
  ks.common = [[.5+dk,il] for il in np.arange(.5/d,(d-1)*.5/d,dk)] 
  lks2 = [[-k[0],.5-k[1]] for k in lks]
  ks.path1 = lks  # first path
  ks.path2 = lks2  # second path
  return ks

