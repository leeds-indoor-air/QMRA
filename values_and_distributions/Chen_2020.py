import math as m
'''
From:
Chen, W., Zhang, N., Wei, J., et al.
Short-range airborne route dominates exposure of respiratory infection during close contact (2020)

Figures taken from Fig. A1(b)
'''
distance = [0.1, 0.5, 1.0, 1.5, 2.0] #metres
log_10_eSR = [-1.62, -3.86, -5.22, -6.05, -6.60]
log_10_eLD = [-0.60, -5.10, -7.33, -8.44, -9.38]

eSR = [ m.pow( 10, x ) for x in log_10_eSR ] #microlitres
eLD = [ m.pow( 10, x ) for x in log_10_eLD ]
