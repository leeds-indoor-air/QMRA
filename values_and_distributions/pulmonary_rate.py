import numpy as np
from scipy import stats

''' SOURCE: Close v. far field tx paper'''
''' litres per min '''
def pulmonary_rate( n, ranD ):
    '''
    ~ uniform(9, 11)
    '''
    return stats.uniform.rvs( 9, 11, size = n, random_state = ranD )
