import time
import numpy as np
import math as m
import sys
import queue_model_fns as qu

from van_Doremalen_2020 import viral_half_lives
from Duguid_1946 import total_talk_small
import first_order_ODE as foode
'''
m server queue model
'''
seed = int(time.time())
rD = np.random.default_rng(seed)
print('seed:',seed)

prev = 0.1

very_quiet_rate = 0.5 #per hour
quiet_rate = 3.0 #per hour
busy_rate = 25.0 #per hour

'''
for now:
very quiet: midnight to 6am
busy: 6am to 9am
quiet: 9am to 6pm
busy: 6pm to 10pm
quiet: 10pm to midnight
'''

arrivals = []

qu.simulate_arrivals(very_quiet_rate, 0.0, 6.0, prev, arrivals, rD)
qu.simulate_arrivals(busy_rate, 6.0, 9.0, prev, arrivals, rD)
qu.simulate_arrivals(quiet_rate, 9.0, 18.0, prev, arrivals, rD)
qu.simulate_arrivals(busy_rate, 18.0, 22.0, prev, arrivals, rD)
qu.simulate_arrivals(quiet_rate, 22.0, 24.0, prev, arrivals, rD)

'''
for arr in arrivals:
    print(arr)

print(Q, Q_ACH)
'''

def residence_time(rD):
    return rD.gamma(shape=1.1, scale=1.0/10)
    #return 0.10

out_str = []
t, occ, inf, que, arrive_depart = qu.simulate_usage(4, arrivals, residence_time, out_str, rD)


for s in out_str:
    print(s)


V = 1.5 * 5 * 2 #cubic metres

people = 4 #number of people
litrespersecondperperson = 0 #stats.uniform.rvs(1, 5, size=(N,2)) #ventilation in l/s/person

Q = people * litrespersecondperperson * 60 / 1000 #total ventilation rate in m3/min
Q_ACH = 60 * Q / V

gamma = {k_:m.log(2)/(v_ * 60) for k_, v_ in zip(viral_half_lives.keys(),
                                                 viral_half_lives.values())} #per min [van Doremalen (2020)]

gamma_air = gamma['aerosol']
vol_resp_fl_small_talking = np.sum(total_talk_small) #Chen2020 + Duguid1946


'''
q = vol_resp_fl_small_talking * 1e8 / 1000.0 / V

C = [0.0]
for t0, t1, I in zip(t[:-1:], t[1::], inf):
    c = qmra.xs_( (t1-t0)*60.0, q*I, Q/V + gamma_air, C[-1])
    C.append(c)
'''

a =  vol_resp_fl_small_talking * 1e8 / (60.0 * 1000.0 * V)
b = (Q/V + gamma_air)*60.0

C = qu.calculate_concentrations( t, inf, a, b, 0.0 )

for n, (t0, t1, I, c) in enumerate(zip(t[:-1:], t[1::], inf, C)):
    print(n, t0, t1, I, c)

E = qu.calculate_exposures( 1.0, arrive_depart, t, C, inf, a, b )

for (a, d, _), e in zip(arrive_depart, E):
    print(a, d, e)

from matplotlib import pyplot as plt

fig, ax = plt.subplots(1,2,sharex=True)

fig.set_size_inches( (18,5) )

ax[0].step(t, occ, 'g-', where='post', label='occupants', alpha=0.6)
ax[0].step(t, inf, 'r-', where='post', label='infected', alpha=0.6)
ax[0].step(t, que, 'b-', where='post', label='queue', alpha=0.6)
ax[0].legend( loc='upper left' )

ax[1].plot(t, C, 'k-')

ax[0].set_xlabel('time (hr)')
ax[0].set_title('occupancy (people)')
ax[1].set_title(r'airborne concentration (RNA m$^{-3}$)')


fig.savefig('fig_out')
plt.show()





