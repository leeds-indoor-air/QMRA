''' SOURCE: Close v. far field tx paper'''
''' litres per min '''
def pulmonary_rate( n, ranD ):
    '''
    ~ uniform(9, 11)
    '''
    return np.divide( stats.uniform.rvs( 9, 11, size = n, random_state = ranD ), 1000 )
