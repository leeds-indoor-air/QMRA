'''
van Doremalen, N, Bushmaker, T, Morris, DH., et al. (2020). Aerosol and Surface Stability of SARS-CoV-2 as Compared with SARS-CoV-1

for example,

Exponential_decay_rate_air = log(2)/1.1 #per hour van Doremalen
Exponential_decay_rate_surf = log(2)/5.63 #per hour for Steel van Doremalen
'''
viral_half_lives = {'aerosol':1.1,
                    'copper':0.75, 
                    'cardboard':3.5,
                    'stainless_steel':5.6,
                    'plastic':6.8
                    }#hours
