import numpy as np


def write_kdos(k=0.,es=[],ds=[],new=True):
  """ Write KDOS in a file"""
  if new: f = open("KDOS.OUT","w") # open new file
  else: f = open("KDOS.OUT","a") # continue writting
  for (e,d) in zip(es,ds): # loop over e and dos
    f.write(str(k)+"     ")
    f.write(str(e)+"     ")
    f.write(str(d)+"\n")
  f.close()





def kdos1d_sites(h,sites=[0],scale=10.,nk=100,npol=100,kshift=0.,
                  ewindow=None,info=False):
  """ Calculate kresolved density of states of
  a 1d system for a certain orbitals"""
  if h.dimensionality!=1: raise # only for 1d
  ks = np.linspace(0.,1.,nk) # number of kpoints
  h.turn_sparse() # turn the hamiltonian sparse
  hkgen = h.get_hk_gen() # get generator
  if ewindow is None:  xs = np.linspace(-0.9,0.9,nk) # x points
  else:  xs = np.linspace(-ewindow/scale,ewindow/scale,nk) # x points
  import kpm
  write_kdos() # initialize file
  for k in ks: # loop over kpoints
    mus = np.array([0.0j for i in range(2*npol)]) # initialize polynomials
    hk = hkgen(k+kshift) # hamiltonian
    for isite in sites:
      mus += kpm.local_dos(hk/scale,i=isite,n=npol)
    ys = kpm.generate_profile(mus,xs) # generate the profile
    write_kdos(k,xs*scale,ys,new=False) # write in file (append)
    if info: print "Done",k


def surface(h,surft,nk=50,ne=50,ewindow=[-.5,.5]):
  klist = np.linspace(0.,1.,nk) # number of kpoints
  energies = np.linspace(ewindow[0],ewindow[1],ne) # number of energies
  # get the different matrices
  tx = surft["tx"]
  intra = surft["intra"]
  ty = surft["ty"]
  txy = surft["txy"]
  txmy = surft["txmy"]
  # perform the loop
  for k in klist:
    # this is for the edge cell
    tky = ty*np.exp(1j*np.pi*2.*k)
    tkx = ty*np.exp(1j*np.pi*2.*k)
    tkxy = txy*np.exp(1j*np.pi*2.*k)
    tkxmy = txmy*np.exp(-1j*np.pi*2.*k)  # notice the minus sign !!!!
    # chain in the x direction
    onsk = intra + tky + tky.H  # intra of k dependent chain
    hopk = tx + tkxy + tkxmy  # hopping of k-dependent chain
    for energy in energies:
      dosb,doss = green.green_kchain(h,k=ki,energy=energy,delta=0.0002,only_bulk=False)
      # now calculate the selfenergy
      raise
      selfe = hopk 


  fkd = open("KDOS.OUT","w") # open file
  p = Pool(5)  # create pool
  list_dosk = p.map(kdos,kpoints)  # compute kpoints in parallel
  for (k,dosk) in zip(kpoints,list_dosk):
    for (energy,doss) in zip(energies,dosk):
      fkd.write(str(k)+"   ")
      fkd.write(str(energy)+"   ")
      fkd.write(str(doss)+"\n")
      print "Done",k,energy
  fkd.close()

