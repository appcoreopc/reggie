import os
import numpy as np
import matplotlib.pyplot as pl

import reggie.gps
import reggie.learning
import reggie.plotting


if __name__ == '__main__':
    cdir = os.path.abspath(os.path.dirname(__file__))
    data = np.load(os.path.join(cdir, 'xy.npz'))

    # create a model
    gp = reggie.gps.BasicGP(0.1, 1.0, 0.1)

    # set the hyperpriors
    gp.set_prior('sn2', 'lognormal', 0, 10)
    gp.set_prior('rho', 'lognormal', 0, 100)
    gp.set_prior('ell', 'lognormal', 0, 10)
    gp.set_prior('mean', 'normal', 0, 20)

    gp.set_block('rho', 1)
    gp.set_block('mean', 2)

    # add data and optimize
    gp.add_data(data['X'], data['y'])
    gp.optimize()

    # sample hyperparameters
    mcmc = reggie.learning.MetaMCMC(gp, n=1000, rng=None)

    # optimize and plot
    pl.figure(1)
    pl.subplot(121)
    reggie.plotting.plot_posterior(gp, draw=False)
    pl.axis(ymax=3, ymin=-2)
    pl.title('MAP')

    pl.subplot(122)
    reggie.plotting.plot_posterior(mcmc, draw=False)
    pl.axis(ymax=3, ymin=-2)
    pl.title('MCMC')
    pl.draw()
