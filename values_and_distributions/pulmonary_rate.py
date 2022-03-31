import numpy as np
from scipy import stats

def pulmonary_rate( n, ranD ):
    '''
    ~ uniform(9, 11)
    '''
    return stats.uniform.rvs( 9, 11, size = n, random_state = ranD )
