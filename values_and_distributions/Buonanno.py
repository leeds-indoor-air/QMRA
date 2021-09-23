'''
Taken from Estimation of airborne viral emission: 
Quanta emission rate of SARS-CoV-2 for infection risk assessment
by G.Buonanno, L.Stabile & L.Morawska 2020

D = droplet diameter midpoints [micrometer]
V = droplet volumes [mL]
IR = inhalation rates (averaged over males & females) [m^3 h^-1] by activity_level
N = droplet concentrations for each d in D and expiratory activity [part cm^-3] by respiratory_activity
c_i = RNA->quanta conversion [quanta per RNA copy]
c_v = sputum viral load [RNA copies per mL]

RETURNS: quanta emission rate [quanta per hour]
'''
import math as m

D = [0.8, 1.8, 3.5, 5.5] #micrometers
V = [m.pi * m.pow(d,3) / 6 * 1e-12 for d in D] #mL

IR = {'resting':0.49
      ,'standing': 0.54
      ,'light exercise': 1.38
      ,'moderate exercise': 2.35
      ,'heavy exercise': 3.30} #m^3 h^-1
      
N = {'voiced counting': [0.236, 0.068, 0.007, 0.011]
     ,'whispered counting': [0.110, 0.014, 0.004, 0.002]
     ,'unmodulated vocalization': [0.751, 0.139, 0.139, 0.059]
     ,'breathing': [0.084, 0.009, 0.003, 0.002]} #part cm^-3 (equiv. part mL^-1)

'''
calculate \sum N_i,j V_j for each respiratory activity
'''
NV = N.copy()
for act, val in N.items():
    nv = 0
    for v, n in zip(V, val):
        nv += n*v
    NV[act] = nv

print(NV)

act_level_str = "activity level should be one of \'resting\', \'standing\', \'light exercise\', \'moderate exercise\' or \'heavy exercise\'"

resp_act_str = "respiratory activity should be one of \'voiced counting\', \'whispered counting\', \'unmodulated vocalization\' or \'breathing\'"

def quanta_emission_rate(c_v, c_i, respiratory_activity, activity_level):
    try:
        ir = IR[activity_level]
    except KeyError:
        print(act_level_str)
        return

    try:
        n = NV[respiratory_activity]
    except KeyError:
        print(resp_act_str)
        return
    
    ER = c_v * c_i * IR[activity_level] * 1e6 * NV[respiratory_activity]
    return ER


