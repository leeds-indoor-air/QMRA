import numpy as np

zind = {'1a' : 0
        ,'1b' : 1
        ,'c1' : 2
        ,'2a' : 3
        ,'2b' : 4
        ,'c2' : 5
        ,'3a' : 6
        ,'3b' : 7
        ,'c3' : 8}

geometry = np.zeros( (9, 9), dtype=bool )

def add_geometry(ind1, ind2):
    geometry[ind1, ind2] = geometry[ind2, ind1] = 1

add_geometry( zind['1a'], zind['1b'])
add_geometry( zind['1b'], zind['c1'])
add_geometry( zind['2a'], zind['2b'])
add_geometry( zind['2b'], zind['c2'])
add_geometry( zind['3a'], zind['3b'])
add_geometry( zind['3b'], zind['c3'])
add_geometry( zind['c1'], zind['c2'])
add_geometry( zind['c2'], zind['c3'])

print('geometry:')
print(geometry*1)

supply = np.array([0, 6, 3, 0, 6, 3, 0, 6, 3])
extract = np.array([6, 0, 3, 6, 0, 3, 6, 0, 3])

beta = np.zeros( (9,9) )

beta[ zind['1a'], zind['1b'] ] = -6
beta[ zind['1b'], zind['1a'] ] = -beta[ zind['1a'], zind['1b'] ]



print( np.sum(supply) - np.sum(extract) )





