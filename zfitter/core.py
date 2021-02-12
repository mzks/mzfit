import numpy as np
import matplotlib.pyplot as plt
import zfit

class zfitter(object):

    def __init__(self, data):
        self.data = data
        self.data_lower = np.min(data)
        self.data_upper = np.max(data)
        self.fit_lower = self.data_lower
        self.fit_upper = self.data_upper
        self.bins = 100
        self._calc_fit_bins()
        self.model = 'gauss'
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
        self.calc_fit_bins()
        self.obs = zfit.Space('x', limits=(self.fit_lower, self.fit_upper))

    def add_parameter(self, parameter):
        zfit.Parameter(parameter)

    def set_model(self, model):
        if model == 'gauss':
            mu = zfit.Parameter("mu", 0)
            sigma = zfit.Parameter("sigma", 1)
            self.model = zfit.pdf.Gauss(obs=self.obs, mu=mu, sigma=sigma)
        else:
            self.model = model

    def set_loss(self, loss):
        self.loss = loss

    def fit(self):
        self.model = self.model
        data = zfit.Data.from_numpy(obs=self.obs, array=self.data)
        result = self.minimizer.minimize(self.loss(model=self.model, data=data))
        self.fitted = True
        return result

    def draw(self):
        hist = plt.hist(self.data, range=(self.data_lower, self.data_upper), bins=self.bins,
                        histtype='step', label='data')
        x_fit = np.arange(self.fit_lower, self.fit_upper, self.bin_width*0.01)
        n_sample = len([d for d in self.data if self.fit_lower < d < self.fit_upper])
        scale_factor = n_sample/self.fit_bins*self.obs.area()
        y_fit = zfit.run(self.model.pdf(x_fit)*scale_factor)
        model_line_style = '-' if self.fitted else '--'
        plt.plot(x_fit, y_fit, label='model', linestyle=model_line_style)
        return hist

    def draw_option(self):

        plt_option = None
        return plt_option
