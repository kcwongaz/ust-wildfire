import numpy as np
from scipy.stats import linregress


def powerlaw_fit(x, y, x_range=(None, None)):
    """
    Compute the power law fit by a linear fit of log(y) against log(x)

    :param x: x values to be fitted
    :param y: y values to be fitted
    :param x_range: array-like (x_min, x_max);
                    only x-values within this range is used for fitting.
                    x_min, x_max = None means no boundary set
    :return: a, b
             a is the power law index, b is the constant, y = b*x^a
    """

    # Select data in the target x-range
    if x_range[0] is not None:
        ind = np.where(x >= x_range[0])
        x = x[ind]
        y = y[ind]

    if x_range[1] is not None:
        ind = np.where(x <= x_range[1])
        x = x[ind]
        y = y[ind]

    # Remove bins with zeros before fitting
    ind = np.nonzero(y)
    logy = np.log(y[ind])
    logx = np.log(x[ind])

    # If there are not enough data to fit
    if len(logy) < 2:
        return np.nan, np.nan

    a, c, _, _, _ = linregress(logx, logy)
    b = np.exp(c)

    return a, b
