import numpy as np
import matplotlib.pyplot as plt
import zfit
from zfit import z
import inspect

class zfitter(object):

    def __init__(self, data, bins=None, lower=None, upper=None):
        self.data = data
        self.bins = 100 if bins is None else bins
        self.data_lower = np.min(data) if lower is None else lower
        self.data_upper = np.max(data) if lower is None else upper
        self.fit_lower = self.data_lower
        self.fit_upper = self.data_upper
        self._calc_fit_bins()
        self.model = None
        self.loss = zfit.loss.UnbinnedNLL
        self.minimizer = zfit.minimize.Adam()
        self.fitted = False
        self.obs = zfit.Space('x', limits=(self.fit_lower, self.fit_upper))

    def _calc_fit_bins(self):
        self.bin_width = (self.data_upper - self.data_lower)/self.bins
        self.fit_bins = int((self.fit_upper - self.fit_lower)/self.bin_width)
        # If bin edges are not match between fit and data, it may be mistake.

    def set_data_bins(self, bins):
        self.bins = bins
        self._calc_fit_bins()

    def set_data_range(self, lower, upper):
        self.data_lower = lower
        self.data_upper = upper

    def set_range(self, lower, upper):
        self.fit_lower = lower
        self.fit_upper = upper
        self._calc_fit_bins()
        self.obs = zfit.Space('x', limits=(self.fit_lower, self.fit_upper))

    def set_bins(self, bins):
        self.bins = bins
        self._calc_fit_bins()
        self.obs = zfit.Space('x', limits=(self.fit_lower, self.fit_upper))

    def set_parameter(self, parname, value):
        self.model.params[parname].set_value(value)

    def set_model(self, model):
        if model == 'gauss':
            mu = zfit.Parameter("mu", 0)
            sigma = zfit.Parameter("sigma", 1)
            self.model = zfit.pdf.Gauss(obs=self.obs, mu=mu, sigma=sigma)
        elif model == 'uniform':
            low = zfit.Parameter("low", 0)
            high = zfit.Parameter("high", 1)
            self.model = zfit.pdf.Uniform(obs=self.obs, low=low, high=high)
        else:
            self.model = model

        print('Parameters')
        self.params()

    def set_loss(self, loss):
        self.loss = loss

    def params(self):
        params = self.model.get_params()
        [print(v.name + ' : ' + str(v.value().numpy())) for v in self.model.get_params()]
        return params

    def summary(self):
        print('Fitting summary')


    def set_model_func(self, func):

        parameters = {k: v.default for k, v
                      in inspect.signature(func).parameters.items()
                      if k != 'x'}

        class UserPDF(zfit.pdf.ZPDF):
            _PARAMS = list(parameters.keys())

            def _unnormalized_pdf(self, x):
                params =[self.params[param] for param in self._PARAMS]
                x = z.unstack_x(x)
                args = {name:para for name, para in zip(self._PARAMS, params)}
                return func(x, **args)

        zfit_parameters = []

        for k,v in parameters.items():
            if v == inspect._empty:
                v = 1
            zfit_parameters.append(zfit.Parameter(k, v))
        arguments = {name:para for name, para in zip(parameters.keys(), zfit_parameters)}

        self.model = UserPDF(obs=self.obs, **arguments)

        print('Parameters')
        self.params()




    def fit(self):
        self.model = self.model
        data = zfit.Data.from_numpy(obs=self.obs, array=self.data)
        self.result = self.minimizer.minimize(self.loss(model=self.model, data=data))
        self.fitted = True
        return self.result

    def draw(self):
        hist = plt.hist(self.data, range=(self.data_lower, self.data_upper), bins=self.bins,
                        histtype='step', label='data')
        if self.model:
            x_fit = np.arange(self.fit_lower, self.fit_upper, self.bin_width*0.01)
            n_sample = len([d for d in self.data if self.fit_lower < d < self.fit_upper])
            scale_factor = n_sample/self.fit_bins*self.obs.area()
            y_fit = zfit.run(self.model.pdf(x_fit)*scale_factor)
            model_line_style = '-' if self.fitted else '--'
            plt.plot(x_fit, y_fit, label='model', linestyle=model_line_style)
        return

    def draw_option(self):

        plt_option = None
        return plt_option
