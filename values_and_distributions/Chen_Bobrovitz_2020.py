import numpy as np

'''
SOURCE: Chen, P.Z., Bobrovitz, N., Premji, Z. Heterogeneity in transmissibility and shedding SARS-CoV-2 via droplets and aerosols (2020)

import time
seed = int(time.time())
print('seed:',seed)
ranD = np.default_rng( seed )
'''

def viral_load( n, ranD ): #copies per ml
    v = ranD.weibull( 3.47, size = n )*7.01
    return np.power( 10, v )
