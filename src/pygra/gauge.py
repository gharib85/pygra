import numpy as np
from . import operators

def to_canonical_gauge(self,m,k):
    """Return a matrix in the canonical gauge form"""
    frac_r = self.geometry.frac_r # fractional coordinates
    # start in zero
    U = np.diag([self.geometry.bloch_phase(k,r) for r in frac_r])
    U = np.array(U) # this is without .H
    U = self.spinless2full(U) # increase the space if necessary
    Ud = np.conjugate(U.T) # dagger
    out = Ud@m@U # redefine matrix
    return out


def canonical_gauge_transformation(self,k):
    """Return a matrix in the canonical gauge form"""
    frac_r = self.geometry.frac_r # fractional coordinates
    # start in zero
    U = np.diag([self.geometry.bloch_phase(k,r) for r in frac_r])
    U = np.array(U) # this is without .H
    U = self.spinless2full(U) # increase the space if necessary
    return U

def Operator2canonical_gauge(h,op):
    """transform an operator into canonical gauge, assuming that
    it is linear"""
    U = operators.Operator(lambda v,k=None: canonical_gauge_transformation(h,k)@v)
    Ud = operators.Operator(lambda v,k=None: canonical_gauge_transformation(h,k).T.conjugate()@v)
    return Ud*op*U
