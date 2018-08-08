import numpy as np
from scipy.sparse import csr_matrix

def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])



def write(x,y,output_file="DATA.OUT",comment=None):
  fo = open(output_file,"w")
  if comment is not None: fo.write("# "+comment+"\n")
  for (ix,iy) in zip(x,y):
    fo.write(str(ix)+"    "+str(iy)+"\n")
  fo.close()
