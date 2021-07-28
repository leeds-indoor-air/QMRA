import numpy as np
import math as m

'''
solution to dx/dt = a - b*x(t)
x(0) = x0
assume all inputs are numpy ndarrays

t.shape = (m,1) OR (1,)
a.shape = b.shape = x0.shape = (1,n) OR (1,)
'''
def xs(t, a, b, x0):
    
    factor1 = np.exp( np.multiply(-b, t) )
    factor2 = np.subtract(  x0, np.divide(a, b) )
    ret = np.multiply( factor1, factor2 )
    np.add( ret, np.divide(a,b), out=ret )
    return ret

'''
single-valued version of xs(t, a, b, x0)
'''
def xs_(t, a, b, x0):

    ret = m.exp( -b * t )
    ret *= x0 - a / b
    ret +=  a/b
    return ret

'''
integral of x(s, a, b, x0) from s = t0 to t1
assume all inputs are numpy ndarrays
version 2
'''
def x_int(a, b, x0, t0, t1):

    ret = np.multiply( a, np.subtract(t1, t0) ) - xs(np.subtract(t1, t0), a, b, x0) + x0
    return np.divide(ret, b)


'''
single input version
'''
def x_int_(a, b, x0, t0, t1):

    ret = a*(t1 - t0) - xs_(t1 - t0, a, b, x0) + x0
    return ret/b
