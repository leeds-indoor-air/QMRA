#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import numpy as np
import math as m
import sys
import datetime
#get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import pyplot as plt

import queue_model_fns as qu
from van_Doremalen_2020 import viral_half_lives
from Duguid_1946 import total_talk_small
import first_order_ODE as foode
from pulmonary_rate import pulmonary_rate

#seed random number generator
seed = int(time.time())
rD = np.random.default_rng(seed)
print('seed:',seed)


# ## Set up
# 
# - Simulates usage of m-cubicle toilet block by a population with a background prevalence of an airborne infectious disease
# - simulation period is 24hr, midnight to midnight
# - arrivals are Markovian (with rate depending on time of day)
# - general residence time distribution
# - if someone arrives and all m cubicles are occupied, they join a queue
# 
# Calculates: 
# - airborne pathogen concentration over the period
# - pathogen exposure for each susceptible visitor + probability of infection
# - expected total 2nd-ary infections over period
# 
# Where we are being naive:
# - no account taken of fomite transmission
# - we assume everyone uses toilet block for same purpose (so no washing, washing of clothes or other uses)
# - we assume a very large population uses the block, with no one making repeat visits
# - no mitigations

# ### Background disease prevalence rate - change this (value between 0 and 1)

# In[2]:


prev = 0.1


# ### Buidling parameters - change these at will!

# In[3]:


V = 1.5 * 5 * 2 #cubic metres

cubs = 4 #number of cubicles

people = 4
litrespersecondperperson = 0.25


# In[4]:


Q = people * litrespersecondperperson * 60 * 60/ 1000 #total ventilation rate in m3/hour
Q_ACH = Q / V
print('Building volume: %.2f (m^3)' %V)
print('Ventilation rate: %.2f (m^3 per hour), %.2f (air changes per hour)' %(Q, Q_ACH))


# ### Decay rate of SARS-CoV-2 in aerosols [hour$^{-1}$] (van Doremalen 2020) - does not apply generally, so keep or change

# In[5]:


gamma = {k_:m.log(2)/(v_) for k_, v_ in zip(viral_half_lives.keys(),
                                                 viral_half_lives.values())} #per hour [van Doremalen (2020)]

gamma_air = gamma['aerosol']
print('gamma_air: %.2f (per hour)' %gamma_air)


# ### Quanta emission rate - change this

# In[6]:


qer = 30.0 #per hour


# ### Residence time distribution
# 
# Naively gamma-distributed with mean approx. 6 mins.  However, we can make this more sophisticated by e.g. calibrating from Ghana data and taking into account different modes of usage, such as washing vs. toileting.

# In[7]:


def residence_time(rD):
    return rD.gamma(shape=1.1, scale=1.0/10)

residence_times_hist = [residence_time(rD) for i in range(5000)]
plt.hist(residence_times_hist, bins=40)
plt.xlabel('time (hours)')
plt.ylabel('frequency')
plt.show()


# ### Arrival pattern - change this
# 
# Just made this up, but again, can play with this and/or use Ghana data

# In[8]:


'''
very quiet: midnight to 6am
busy: 6am to 9am
quiet: 9am to 6pm
busy: 6pm to 10pm
quiet: 10pm to midnight
'''

very_quiet_rate = 0.5 #per hour
quiet_rate = 3.0 #per hour
busy_rate = 25.0 #per hour


# ## Run simulation

# ### 1. Simulate arrivals and usage

# In[9]:


arrivals = []

qu.simulate_arrivals(very_quiet_rate, 0.0, 6.0, prev, arrivals, rD)
qu.simulate_arrivals(busy_rate, 6.0, 9.0, prev, arrivals, rD)
qu.simulate_arrivals(quiet_rate, 9.0, 18.0, prev, arrivals, rD)
qu.simulate_arrivals(busy_rate, 18.0, 22.0, prev, arrivals, rD)
qu.simulate_arrivals(quiet_rate, 22.0, 24.0, prev, arrivals, rD)


# In[10]:


out_str = []
t, occ, inf, que, arrive_depart = qu.simulate_usage(cubs, arrivals, residence_time, out_str, rD)


# In[11]:


#Uncomment below if you want to see simulated usage pattern listed
#for str in out_str:
#        print(str)
        


# ### 2. Calculate airborne concentration [quanta m$^{-3}$] at each change in occupancy

# In[12]:


a =  qer / V
b = (Q/V + gamma_air)
C = qu.calculate_concentrations( t, inf, a, b, 0.0 )


# ### 3. Calculate each person's exposure [quanta]

# #### notes
# 
# Gammaitoni and Nucci's model [Beggs, et al. 2003] in terms of airborne *concentration* rather than absolute airborne pathogen load is
# 
# \begin{align}
# \frac{dS}{dt} &= - p\,C\,S\\
# \frac{dC}{dt} &= \frac{q}{V} - (\frac{Q}{V} + \gamma_{\text{air}})\,C\\
# \end{align}
# 
# where
# 
# $S = $ number of susceptibles
# 
# $C = $ airborne concentration [quanta per m${^3}$] 
# 
# $p = $ pulmonary ventilation rate [m${^3}$ per hour]
# 
# $Q = $ ventilation rate [m${^3}$ per hour]
# 
# $V = $ room volume [m${^3}$]
# 
# $\gamma_{\text{air}} = $ pathogen decay rate in aerosols [per hour]
# 
# $q = $ emission rate [quanta].
# 
# 
# Adapting to discrete infections, note that hazard of infection, per susceptible, is
# 
# \begin{equation}
# h(t) = p\,C(t)
# \end{equation}
# 
# and, therefore, probability of infection due to exposure to concentration $C(t)$ between $t_0$ and $t_1$ is
# 
# \begin{align}
#     P_{\text{inf}} &= 1 - \exp\left\{-\int_{t_0}^{t_1} h(t)\,dt\right\}\\
#     & = 1 - \exp\left\{-p\int_{t_0}^{t_1} C(t)\,dt\right\}.\\
# \end{align}
# 
# E.g. total exposure to 1 quantum leads to infection with probability $1 - e^{-1} = 0.632$.
# 
# Integral is performed by function `calculate_exposures` in `queue_model_fns`

# In[13]:


pulmonary_rates = pulmonary_rate( len(arrive_depart), rD) / 1000.0
E = np.array( qu.calculate_exposures( pulmonary_rates, arrive_depart, t, C, inf, a, b ) )


# ## View outputs

# ### 1. Occupancy & airborne concentration

# In[14]:


fig, ax = plt.subplots(1,2,sharex=True)

fig.set_size_inches( (18,5) )

ax[0].step(t, occ, 'g-', where='post', label='occupants', alpha=0.6)
ax[0].step(t, inf, 'r-', where='post', label='infected', alpha=0.6)
ax[0].step(t, que, 'b-', where='post', label='queue', alpha=0.6)
ax[0].legend( loc='upper left' )

ax[1].plot(t, C, 'k-')

ax[0].set_xlabel('time (hr)')
ax[0].set_title('occupancy (people)')
ax[1].set_title(r'airborne concentration (quanta m$^{-3}$)')

plt.show()


# ### 2. Exposure

# In[15]:


pinf = 1 - np.exp(-E)

print('time entered\ttime left\ttime spent\texposure (quanta)\tP(inf)')
print('--------------------------------------------------------------------------------------')
print('(susceptibles only)\n')
susceptibles = 0
for (a, d, _), e, pinf_ in zip(arrive_depart, E, pinf):
    if _ == 1:
        continue
    t_enter = str(datetime.timedelta(hours=a)).rsplit('.')[0]
    t_leave = str(datetime.timedelta(hours=d)).rsplit('.')[0]
    t_spent = str(datetime.timedelta(hours=d) - datetime.timedelta(hours=a)).rsplit('.')[0]
    susceptibles += 1
    #spent = (d-a)*60.0
    print(t_enter + '\t\t' + t_leave + '\t\t' + t_spent +'\t\t%.8f\t\t%.4f' %(e, pinf_))


# ### Expected number of secondary infections

# In[16]:


E_infs = np.sum(pinf)
print('Expected 2nd-ary infections: %.3f out of %d susceptibles' %(E_infs, susceptibles) )

