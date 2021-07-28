import numpy as np

'''
SOURCE: Chen & Brobovitz (2020)

import time
seed = int(time.time())
print('seed:',seed)
ranD = np.default_rng( seed )
'''

def viral_load( n, ranD ): #copies per ml
    v = ranD.weibull( 3.47, size = n )*7.01
    return np.power( 10, v )
