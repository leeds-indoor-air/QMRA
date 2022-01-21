import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt

C = [1000, 0, 0, 0, 0]

beta12 = 0.05
beta21 = 0.02
beta23 = 0.01

Q = [0.0, 0.12, 0.0, 0.0, 0.0]

m = [[0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.001],
     [0.0, 0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0]]

beta = [[0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, beta12, 0.0, 0.0],
        [0.0, beta21, 0.0, beta23, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]]


d = [1.0, 2.0, 4.0, 8.0, 16.0]
d_inv = np.divide(1.0, d)

Z = np.zeros((5,5))

def f(C, t):
    D_inv = np.eye(d_inv.size, d_inv.size)*d_inv
    
    dXdt = np.matmul( np.matmul(D_inv, Z), C )
    return dXdt

def update_Z(Z, m, beta, Q, N):
    beta_row_sum = np.sum(beta, axis=1)
    for i in range(N):
        for j in range(N):
            Z[i, j] = beta[j][i] + m[j][i]

    for i in range(N):
        Z[i, i] = -beta_row_sum[i] - Q[i]
    
update_Z(Z, m, beta, Q, 5)    

t1 = np.linspace(0, 5.0, 1000)
Ct1 = odeint(f, C, t1)

m[0][1] = 1e10 * 0.54 * 1e6 * 1.3863104870030406e-12
update_Z(Z, m, beta, Q, 5)

t2 = np.linspace(5.0, 15.0, 1000)
Ct2 = odeint(f, Ct1[-1], t2)

m[0][1] = 0.0
update_Z(Z, m, beta, Q, 5)

t3 = np.linspace(15.0, 115.0, 1000)
Ct3 = odeint(f, Ct2[-1], t3)

t = np.concatenate( (t1, t2, t3) )
Ct = np.concatenate( (Ct1, Ct2, Ct3), axis=0 )

plt.plot(t, Ct[::, 1:])
plt.savefig('test_out')



