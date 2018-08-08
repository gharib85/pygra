import numpy.linalg as lg
from scipy.optimize import minimize_scalar
import scipy.optimize as opt
import numpy as np
import scipy.sparse.linalg as lgs
from scipy.sparse import csc_matrix

def minimize_gap(f,tol=0.001):
  """Miimizes the gap of the system, the argument is between 0 and 1"""
  return f(minimize_scalar(f,method="Bounded",bounds=(0.,1.),tol=tol).x)





def gap_line(h,kpgen,assume_eh = False,sparse=True,nocc=None):
  """Return a function with argument between 0,1, which returns the gap"""
  hk_gen = h.get_hk_gen() # get hamiltonian generator
  def f(k):
    kp = kpgen(k) # get kpoint
    hk = hk_gen(kp) # generate hamiltonian
    if sparse: 
      es,ew = lgs.eigsh(csc_matrix(hk),k=4,which="LM",sigma=0.0)
    else:
      es = lg.eigvalsh(hk) # get eigenvalues
    if assume_eh: g = np.min(es[es>0.])
    else:  
      if nocc is None: # Assume conduction are staets above E = 0.0
        try: g = np.min(es[es>0.]) - np.max(es[es<0.])
        except: g = 0.0 
      else:
        g = es[nocc] - es[nocc-1]
    return g  # return gap
  return f  # return gap


def raw_gap(h,kpgen,sparse=True,nk=100):
  hk_gen = h.get_hk_gen() # get hamiltonian generator
  ks = np.linspace(0.,1.,nk)
  etot = [] # total eigenvalues
  for k in ks:
    kp = kpgen(k)
    hk = hk_gen(kp) # generate hamiltonian
    if sparse: 
      es,ew = lgs.eigsh(csc_matrix(hk),k=4,which="LM",sigma=0.0)
    else:
      es = lg.eigvalsh(hk) # get eigenvalues
    etot.append(es)
  etot = np.array(etot)
  return min(etot[etot>0.])


def gap2d(h,nk=40,k0=np.array([0.,0.]),rmap=1.0,recursive=False,
           iterations=5):
  """Calculates the gap for a 2d Hamiltonian by doing
  a kmesh sampling"""
  if h.dimensionality != 2: raise
  hk_gen = h.get_hk_gen() # get hamiltonian generator
  emin = 1000. # initial values
  for ix in np.linspace(-.5,.5,nk):  
    for iy in np.linspace(-.5,.5,nk):  
      k = np.array([ix,iy]) # generate kvector
      if recursive: k = k0 + k*rmap # scale vector
      hk = hk_gen(k) # generate hamiltonian
      es = lg.eigvalsh(hk) # get eigenvalues
      es = es[es>0.] # retain positive
      if min(es)<emin:
        emin = min(es) # store new minimum 
        kbest = k.copy() # store the best k
  if recursive: # if it has been chosen recursive
    if iterations>0: # if still iterations left
      emin = gap2d(h,nk=nk,k0=kbest,rmap=rmap/4,recursive=recursive,
                      iterations=iterations-1)
  return emin # gap



def optimize_gap_single(h,direct=True):
  """Return the gap, just one time"""
  hkgen = h.get_hk_gen() # get generator
  dim = h.dimensionality # dimensionality
  if direct: # returnt the direct gap
    def fg(k): # minimize the gap
      es = lg.eigvalsh(hkgen(k)) # eigenvalues
      return np.min(es[es>0.])-np.max(es[es<0.]) # return gap
    x0 = np.random.random(dim) # random point
    bounds = [(0,1.) for i in range(dim)] # bounds
    result = opt.minimize(fg,x0,bounds=bounds,method="SLSQP")
    x = result.x # position of the minimum gap
    return (fg(x),x)
  else: # indirect gap
    def fg(k): # minimize the gap
      es1 = lg.eigvalsh(hkgen(k)) # eigenvalues
      es2 = lg.eigvalsh(hkgen(k)) # eigenvalues
      return np.min(es1[es1>0.])-np.max(es2[es2<0.]) # return gap
    x0 = np.random.random(dim*2) # random point
    bounds = [(0,1.) for i in range(2*dim)] # bounds
    result = opt.minimize(fg,x0,bounds=bounds,method="SLSQP")
    x = result.x # position of the minimum gap
    return (fg(x),x)
     
def optimize_gap(h,direct=True,ntries=10):
  """Return the gap, several times"""
  rs = [optimize_gap_single(h,direct=direct) for i in range(ntries)]
  gaps = [r[0] for r in rs] # gaps
  mg = np.min(gaps) # minimum gap
  for r in rs: # loop over gaps
    if r[0]==mg: return r # return minimum




  
#  else: # indirect gap

