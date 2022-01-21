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

#mi = np.genfromtxt('outputs/moving_infector.out')
e1 = np.genfromtxt('outputs/exposure_1.out')
e2 = np.genfromtxt('outputs/exposure_2.out')
e3 = np.genfromtxt('outputs/exposure_3.out')
e4 = np.genfromtxt('outputs/exposure_4.out')
e5 = np.genfromtxt('outputs/exposure_5.out')
e6 = np.genfromtxt('outputs/exposure_6.out')
e7 = np.genfromtxt('outputs/exposure_7.out')
e8 = np.genfromtxt('outputs/exposure_8.out')
e9 = np.genfromtxt('outputs/exposure_9.out')


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

#ax[1].plot(t, mi, label = 'mi')
ax[1].plot(t, e1, label = 'e1')
ax[1].plot(t, e2, label = 'e2')
ax[1].plot(t, e3, label = 'e3')
ax[1].plot(t, e4, label = 'e4')
ax[1].plot(t, e5, label = 'e5')
ax[1].plot(t, e6, label = 'e6')
ax[1].plot(t, e7, label = 'e7')
ax[1].plot(t, e8, label = 'e8')
ax[1].plot(t, e9, label = 'e9')

ax[1].legend()
ax[1].set_ylabel('Exp. (RNA copies)')

plt.savefig('Res_moving_infector')
#plt.show()
