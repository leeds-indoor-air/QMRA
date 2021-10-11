# leeds-indoor-air
Private repo for the Indoor Air group, department of Civil Engineering, University of Leeds

## To use the repo

`git clone address`

Explain here how to add path to local repo to `PYTHONPATH` for Windows, Linux and Mac.

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

## `values_and_distributions/`

**`Buonanno.py`**

**`Chen_Bobrovitz_2020.py`**

**`Jones_et_al_2021.py`**

**`Chen_2020.py`**

**`Duguid_1946.py`**

**`pulmonary_rate.py`**

**`van_Doremalen_2020.py`**

