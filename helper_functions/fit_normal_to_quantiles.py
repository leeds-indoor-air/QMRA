from scipy.stats  import norm

'''
Given 0 < alpha < 1 and quantiles q_0 < q1 returns mean and std. deviation of normal distribution
X ~ Normal(mu, sigma) such that P(q_0 < X < q_1) = alpha

mu: since normal distribution is symmetric, mu is midway between q_0 and q_1

sigma: X = mu + sigma*Z ~ N(mu, sigma) (Z ~ N(0,1))

P( -(q_1 - q_0)/(2*sigma) < Z < (q_1 - q_0)/(2*sigma) ) = alpha


https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.html#scipy.stats.rv_continuous
    sf(x) = 1 - F(x)
    isf = sf^-1

    y in [0,1], y = sf( isf( y ) ) = 1 - F( isf(y) )
    F( isf(y) ) = 1 - y
    F( isf(1-y) ) = y
'''
def fit_norm( alpha, q_0, q_1 ):
    mu = (q_0 + q_1)*0.5
    u = norm.isf( 0.5*(1-alpha) )
    sigma = (q_1 - q_0)/(2*u)
    return mu, sigma



