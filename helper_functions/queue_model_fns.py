import numpy as np
import heapq
import sys
import first_order_ODE as foode

'''
m cubicle queue model
'''

def simulate_arrivals(rate, start_time, end_time, prevalence, output, rD):
    n = rD.poisson(lam = rate * (end_time - start_time))
    a = np.sort( rD.uniform(start_time, end_time, size=n) )
    i = rD.binomial(1, prevalence, n)

    for a_, i_ in zip(a, i):
        output.append( (a_, i_) )
    np.sort(output)


def simulate_usage(m, arrivals, residence_time, output_str, rD):
    event_queue = []
    
    occupants = [0]
    queue = [0]
    queue_detail = []
    infecteds = [0]
    arrive_depart = []

    t = [0.0]
    
    for arr, infected in arrivals:
        heapq.heappush( event_queue, (arr, infected, 'arrive') )

    while( event_queue != [] ):
        next_event_time, infected, next_event_type = heapq.heappop(event_queue)

        t.append(next_event_time)

        if next_event_type == 'arrive' and occupants[-1] < m:
            ''' arrives & not full '''
            occupants.append( occupants[-1] + 1 )
            queue.append( queue[-1] )
            if infected:
                infecteds.append( infecteds[-1] + 1 )
            else:
                infecteds.append( infecteds[-1] )
            duration = residence_time(rD)
            heapq.heappush( event_queue, (t[-1] + duration, infected, 'leave_') )
            arrive_depart.append( (t[-1], t[-1] + duration, infected) )
            

        elif next_event_type == 'arrive' and occupants[-1] == m:
            ''' arrives & full '''
            occupants.append( occupants[-1] )
            queue.append( queue[-1] + 1 )
            heapq.heappush( queue_detail, (next_event_time, infected) )
            infecteds.append( infecteds[-1] )

        elif next_event_type == 'leave_' and queue[-1] == 0:
            ''' leaves & queue is empty '''
            occupants.append( occupants[-1] - 1 )
            queue.append( 0 )
            if infected:
                infecteds.append( infecteds[-1] - 1 )
            else:
                infecteds.append( infecteds[-1] )
 
        elif next_event_type == 'leave_' and queue[-1] > 0:
            if infected:
                infecteds.append( infecteds[-1] - 1 )
            else:
                infecteds.append( infecteds[-1] )
                
            _, q_infected = heapq.heappop( queue_detail )

            if q_infected:
                infecteds[-1] += 1 

            queue.append( queue[-1] - 1 )
            duration = residence_time(rD)
            occupants.append( occupants[-1] )
            heapq.heappush( event_queue, (t[-1] + duration, q_infected, 'leave_') )
            arrive_depart.append( (t[-1], t[-1] + duration, infected) )

        else:
            print('something has gone wrong')
            sys.exit()

        output_str.append('%.3f\t%s\t%s\t%s\t%s'
                          %(next_event_time, next_event_type
                            ,occupants[-1], infecteds[-1], queue[-1]) )

    return t, occupants, infecteds, queue, arrive_depart


def calculate_concentrations( t, infects, a, b, c0 ):
    C = [c0]

    for t0, t1, I in zip(t[:-1:], t[1::], infects):
        c = foode.xs_( t1-t0, a*I, b, C[-1])
        C.append(c)

    return C


'''
Integrate C(t) between t0 and t1
'''
def integrate_concentration( t0, t1, t, C, I, a, b ):
    ind = np.nonzero(np.greater_equal(t, t0)*np.less_equal(t ,t1))[0]
    int_C = 0.0
    for i0, i1 in zip(ind[:-1:], ind[1::]):
        int_C += foode.x_int_(a*I[i0], b, C[i0], t[i0], t[i1])
    return int_C

def calculate_exposures( multiplier, arrive_depart, t, C, I, a, b ):
    E = []
    for mult, (a, d, _) in zip(multiplier, arrive_depart):
        E.append(mult * integrate_concentration( a, d, t, C, I, a, b ))
    return E


    
    
