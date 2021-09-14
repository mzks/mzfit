__version__ = '0.1'

from .core import *

__all__ = ['mzfit']


def help():
    print("""
    Welcome to mzfit!

    Fitting 4 steps on mzfit,

    Step 1 : Load data and make fitter
    `zf = mzfit.zf(data)`

    Step 2 : Make model and initial parameters
    ```
    zf.set_model('gauss') 
    zf.set_parameter('mu', 11)
    zf.set_parameter('sigma', 3)
    ```
    or,
    ```
    from zfit import z
    def user_func(x, mu=10, sigma=1, C=1):
        return z.exp(-z.square((x - mu) / sigma)) + C
    zf.set_model_func(user_func)
    ```

    Step 3 : Visualize
    `zf.draw()`
    If it is not nice, repeat step 2.

    Step 4 : Fit
    ```
    zf.fit()
    zf.draw()
    zf.result
    ```
    """)
    
