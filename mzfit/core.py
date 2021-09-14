import os
os.environ['ZFIT_DISABLE_TF_WARNINGS']='1'

import numpy as np
import matplotlib.pyplot as plt

import zfit
from zfit import z
import inspect

class zf(object):

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
        self.minimizer = zfit.minimize.Minuit()
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

    def set_value(self, name, value):
        self.model.params[name].set_value(value)

    def set_parameter(self, name, value):
        if name in zfit.Parameter._existing_params:
            param = self.model.params[name]
            if value:
                param.set_value(value)
        else:
            print('No such Parameter ' + name)

    def set_parameters(self, dict):
        for name, value in dict.items():
            self.set_parameter(name, value)

    def set_model(self, model):
        self._reset_parameters()
        if model == 'gauss':
            mu = zfit.Parameter("mu", 0)
            sigma = zfit.Parameter("sigma", 1)
            self.model = zfit.pdf.Gauss(obs=self.obs, mu=mu, sigma=sigma)
        elif model == 'uniform':
            low = zfit.Parameter("low", 0)
            high = zfit.Parameter("high", 1)
            self.model = zfit.pdf.Uniform(obs=self.obs, low=low, high=high)
        elif model == 'exp':
            Lambda = zfit.Parameter("lambda", 0)
            self.model = zfit.pdf.Uniform(obs=self.obs, Lambda=Lambda)
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
        if self.result:
            print('Fitting summary')
            print(self.result)

    def _reset_parameters(self):
        zfit.Parameter._existing_params.clear()


    def set_model_func(self, func):

        self._reset_parameters()
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

        hist = np.histogram(self.data, bins=self.bins, range=(self.data_lower, self.data_upper))
        x = (hist[1][:-1] + hist[1][1:])/2
        bin_widths = hist[1][1:] - hist[1][:-1]
        xerr=bin_widths/2
        y = hist[0]
        yerr = np.sqrt(y)
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, linestyle='None', label='data')

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
