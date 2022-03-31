# PROTECT-NCS WP2.1.1
Code repository for the National Core Study PROTECT project, work package 2.1.1.

Contains code and Jupyter notebooks for
- the simple three-route QMRA model
- QMRA / queue model of a public toilet
- useful data from publications (in `values_and_distributions/`)

## To use the repo
- `git clone git@github.com:uol-research-private/QMRA.git`

- append "/path/to/QMRA/helper_functions" and "/path/to/QMRA/values_and_distributions" to your PYTHONPATH environment variable.

## `helper_functions/`

**`first_order_ODE.py`** provides `xs(t, a, b, x0)` and `xs_(t, a, b, x0)` for solutions to the ODE

<img src="https://render.githubusercontent.com/render/math?math=\frac{dx}{dt} = a - bx"> with <img src="https://render.githubusercontent.com/render/math?math=x(0) = x_0">

<img src="https://render.githubusercontent.com/render/math?math=t_1"> with <img src="https://render.githubusercontent.com/render/math?math=x(0) = x_0">
of these solutions can be obtained using `x_int(a, b, x0, t0, t1)` and `x_int_(a, b, x0, t0, t1)`.

**`fit_normal_to_quantiles.py`** contains the routine `fit_norm( alpha, q_0, q_1 )`, which fits a univariate normal r.v. X, with mean <img src="https://render.githubusercontent.com/render/math?math=\mu"> and standard deviation <img src="https://render.githubusercontent.com/render/math?math=\sigma">,
such that

<img src="https://render.githubusercontent.com/render/math?math=\mathbf{P}(q_0 \leq X \leq q_1) = \alpha">.

**`queue_model_fns.py`** contains simulation routines to model an m-server queue with Markovian arrivals and general service times, as well as functions to
calculate airborne pathogen concentration and exposure risk in small multi-occupancy spaces.  These functions are used in the toilet block QMRA airborne 
expousre risk model.


