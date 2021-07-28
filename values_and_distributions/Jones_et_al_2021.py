import fit_normal_to_quantiles as fit
import numpy as np
'''
Source: Estimating infectiousness throughout SARS-CoV-2 infection course. Jones et al. 2021
'''

'''
Table S3

Female, Male, Female-Male
mean (90% credible interval)
'''
group = {'female':0, 'male':1, 'female-male':2,
         'hosp_yes':3, 'hosp_no':4, 'hosp_no-yes':5,
         'pams_yes':6, 'pams_no':7, 'pams_no-yes':8}
         
N = [2051, 2287, 2051 + 2287,
     3494, 850, 3494 + 850,
     262, 4082, 262 + 4082]

increasing_slope = [ [1.97,(1.83, 2.13)],
                     [1.97,(1.82, 2.13)],
                     [0.00,(-0.17, 0.17)],
                     [1.92,(1.80, 2.05)],
                     [2.14,(1.90, 2.42)],
                     [0.22,(-0.02, 0.47)],
                     [2.24,(1.88, 2.65)],
                     [1.95,(1.83, 2.08)],
                     [-0.29,(-0.68, 0.06)] ]

days_to_peak_viral_load = [ [4.30,(3.99, 4.62)],
                            [4.32,(3.98, 4.67)],
	                    [-0.02,(-0.39, 0.34)],
                            [4.46,(4.17, 4.76)],
                            [3.70,(3.27, 4.16)],
                            [-0.75,(-1.20, -0.30)],
                            [3.41,(2.84, 4.04)],
                            [4.37,(4.10, 4.66)],
                            [0.96,(0.33, 1.53)] ]

peak_viral_load = [ [8.12,(7.93, 8.30)],
	            [8.16,(7.97, 8.34)],
	            [-0.03,(-0.12, 0.06)],
                    [8.27,(8.08, 8.45)],
                    [7.60,(7.39, 7.79)],
                    [-0.68,(-0.83, -0.52)],
                    [7.28,(6.95, 7.59)],
                    [8.20,(8.01, 8.37)],
                    [0.92,(0.62, 1.21)] ]



decreasing_slope = [ [-0.171,(-0.176, -0.167)],
	             [-0.165,(-0.170, -0.161)],
	             [-0.006,(-0.011, 0.000)],
                     [-0.169,(-0.172, -0.165)],
                     [-0.166,(-0.173, -0.159)],
                     [0.003,(-0.005, 0.010)],
                     [-0.173,(-0.186, -0.159)],
                     [-0.168,(-0.171, -0.164)],
                     [0.005,(-0.009, 0.018)] ]


'''
ind = group['pams_no-yes']
print(increasing_slope[ind])
print(days_to_peak_viral_load[ind])
print(peak_viral_load[ind])
print(decreasing_slope[ind])
'''
    
'''
fit normal distributions to 5 & 95%-tiles
'''


alpha = 0.05

increasing_slope_norm = []
days_to_peak_viral_load_norm = []
peak_viral_load_norm = []
decreasing_slope_norm = []

for d in increasing_slope:
    mean, q_alpha, q_beta = d[0], d[1][0], d[1][1]

    mu, sigma = fit.fit_norm( alpha, q_alpha, q_beta )
    bias = mu - mean
    scale_bias = bias / sigma

    increasing_slope_norm.append( (mu, sigma, bias, scale_bias) )

for d in days_to_peak_viral_load:
    mean, q_alpha, q_beta = d[0], d[1][0], d[1][1]

    mu, sigma = fit.fit_norm( alpha, q_alpha, q_beta )
    bias = mu - mean
    scale_bias = bias / sigma

    days_to_peak_viral_load_norm.append( [mu, sigma, bias, scale_bias] )

for d in peak_viral_load:
    mean, q_alpha, q_beta = d[0], d[1][0], d[1][1]

    mu, sigma = fit.fit_norm( alpha, q_alpha, q_beta )
    bias = mu - mean
    scale_bias = bias / sigma

    peak_viral_load_norm.append( [mu, sigma, bias, scale_bias] )
    
for d in decreasing_slope:
    mean, q_alpha, q_beta = d[0], d[1][0], d[1][1]

    mu, sigma = fit.fit_norm( alpha, q_alpha, q_beta )
    bias = mu - mean
    scale_bias = bias / sigma

    decreasing_slope_norm.append( [mu, sigma, bias, scale_bias] )

def viral_load(m_inc, p_eak, m_dec, t):
    traj = np.multiply( (m_inc * t + p_eak)
                        ,np.less_equal(t, 0.0) * np.greater(t, -p_eak/m_inc))

    traj += np.multiply( (m_dec * t + p_eak)
                         ,np.greater(t, 0.0) * np.less(t, -p_eak/m_dec))

    return traj

