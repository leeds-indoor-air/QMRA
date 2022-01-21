import numpy as np
from matplotlib import pyplot as plt

fig, ax = plt.subplots(1, 2, sharex=True)
fig.set_size_inches(12, 4)
t = np.genfromtxt('outputs/time.out')

a1 = np.genfromtxt('outputs/1a.out')
b1 = np.genfromtxt('outputs/1b.out')
c1 = np.genfromtxt('outputs/c1.out')
a2 = np.genfromtxt('outputs/2a.out')
b2 = np.genfromtxt('outputs/2b.out')
c2 = np.genfromtxt('outputs/c2.out')
a3 = np.genfromtxt('outputs/3a.out')
b3 = np.genfromtxt('outputs/3b.out')
c3 = np.genfromtxt('outputs/c3.out')

e1 = np.genfromtxt('outputs/exposure_1a.out')
e2 = np.genfromtxt('outputs/exposure_1b.out')
e3 = np.genfromtxt('outputs/exposure_2a.out')

ax[0].plot(t, a1, label = '1a')
ax[0].plot(t, b1, label = '1b')
ax[0].plot(t, c1, label = 'c1')
ax[0].plot(t, a2, label = '2a')
ax[0].plot(t, b2, label = '2b')
ax[0].plot(t, c2, label = 'c2')
ax[0].plot(t, a3, label = '3a')
ax[0].plot(t, b3, label = '3b')
ax[0].plot(t, c3, label = 'c3')

ax[0].set_xlabel('time (mins)')
ax[0].set_ylabel('Conc. (RNA copies per unit area / vol)')

ax[0].legend()


ax[1].plot(t, e1, label = 'exp. 1a')
ax[1].plot(t, e2, label = 'exp. 1b')
ax[1].plot(t, e3, label = 'exp. 2a')

ax[1].legend()
ax[1].set_ylabel('Exp. (RNA copies)')

plt.savefig('Res_static_infector')
#plt.show()
