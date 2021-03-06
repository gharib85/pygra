# Add the root path of the pygra library
import os ; import sys ; sys.path.append(os.environ['PYGRAROOT'])

from pygra import geometry
from pygra import specialhamiltonian

g = geometry.honeycomb_lattice()
h = specialhamiltonian.flux2d(g,n=80)
h.geometry.write()
h.get_bands()
