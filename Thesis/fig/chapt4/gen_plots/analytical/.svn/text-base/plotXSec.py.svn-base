#!/usr/bin/env python

"""Plots parton-level analytical cross sections."""

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


gF = 1.1663787e-5  # GeV^(-2)
mt = 172.5  # GeV


def alpha_s(scale, alphaSMZ=0.130, mZ=91.1876, nf=5):
    """Compute alpha_s at the given scale using one-loop running."""
    
    b0 = (33 - 2 * nf) / (12 * math.pi)
    return alphaSMZ / (1 + 2 * alphaSMZ * b0 * math.log(scale / mZ))


def xsec_even(sqrtS, mass, width):
    """Compute cross section for gg -> H -> tt."""
    
    if sqrtS <= 2 * mt:
        return 0., 0.
    
    s = sqrtS**2
    alpha = alpha_s(sqrtS / 2)
    
    beta = math.sqrt(1 - 4 * mt**2 / s)
    y = math.log((1 + beta) / (1 - beta))
    denom = (s - mass**2)**2 + (mass * width)**2
    
    xSecRes = 3 * (alpha * gF * mt**3)**2 * beta**3 / (1024 * math.pi**3) \
        * (16 + 8 * beta**2 * (math.pi**2 - y**2) + beta**4 * (math.pi**2 + y**2)**2) / denom
    xSecInt = - alpha**2 * gF * mt**4 * beta**2 / (32 * math.pi * math.sqrt(2) * s) * y \
        * ((s - mass**2) * (4 + beta**2 * (math.pi**2 - y**2)) \
        + 2 * math.pi * beta**2 * mass * width * y) / denom
    
    # Convert cross sections from GeV^(-2) to pb
    xSecRes /= 2.5819e-9
    xSecInt /= 2.5819e-9
    
    return xSecRes, xSecInt


def xsec_odd(sqrtS, mass, width):
    """Compute cross section for gg -> A -> tt."""
    
    if sqrtS <= 2 * mt:
        return 0., 0.
    
    s = sqrtS**2
    alpha = alpha_s(sqrtS / 2)
    
    beta = math.sqrt(1 - 4 * mt**2 / s)
    y = math.log((1 + beta) / (1 - beta))
    denom = (s - mass**2)**2 + (mass * width)**2
    
    xSecRes = 3 * (alpha * gF * mt**3)**2 * beta / (1024 * math.pi**3) \
        * (math.pi**2 + y**2)**2 / denom
    xSecInt = - alpha**2 * gF * mt**4 / (32 * math.pi * math.sqrt(2) * s) * y \
        * ((s - mass**2) * (math.pi**2 - y**2) + 2 * math.pi * mass * width * y) / denom
    
    xSecRes /= 2.5819e-9
    xSecInt /= 2.5819e-9
    
    return xSecRes, xSecInt


def xsec_helper(sqrtSArray, mass, width, cpState, part):
    """Compute cross section for the given CP state and part of process.
    
    Return a NumPy array with cross section values for the given values
    of sqrt(s-hat).
    """
    
    cpState = cpState.lower()
    
    if cpState == 'even':
        xsec_calc = xsec_even
    elif cpState == 'odd':
        xsec_calc = xsec_odd
    else:
        raise RuntimeError('Unknown CP state requested.')
    
    part = part.lower()
    
    if part == 'r':
        return np.fromiter((xsec_calc(x, mass, width)[0] for x in sqrtSArray), sqrtSArray.dtype)
    elif part == 'i':
        return np.fromiter((xsec_calc(x, mass, width)[1] for x in sqrtSArray), sqrtSArray.dtype)
    elif part == 'sum':
        return np.fromiter((sum(xsec_calc(x, mass, width)) for x in sqrtSArray), sqrtSArray.dtype)
    else:
        raise RuntimeError('Unknown part of process requested')


def plot_all(massPoints, relWidth, outNameBase):
    """Plot cross sections for given mass points and relative width.
    
    Cross sections for R, I, and R+I are plotted in different figures,
    while mass points and CP states are aggregated together.
    """
    
    sqrtS = np.linspace(340., 1000., num=500, dtype=np.float32)
    
    for part, partLabel in [('R', 'R'), ('I', 'I'), ('Sum', 'R + I')]:
        
        fig = plt.figure()
        axes = fig.add_subplot(111)
        
        for mass in massPoints:
            axes.plot(
                sqrtS, xsec_helper(sqrtS, mass, mass * relWidth, 'even', part),
                color='steelblue'
            )
            axes.plot(
                sqrtS, xsec_helper(sqrtS, mass, mass * relWidth, 'odd', part),
                color='orange'
            )
        
        axes.set_xlim(sqrtS[0], sqrtS[-1])
        
        if part == 'R':
            axes.set_ylim(bottom=0.)
        
        axes.set_xlabel(r'$\sqrt{\hat{s}}$ [GeV]', horizontalalignment='right', x=1.)
        axes.set_ylabel(
            r'$\sigma_\mathrm{BSM} - \sigma_\mathrm{QCD}$ [pb]',
            horizontalalignment='right', y=1.
        )
        
        if part != 'R':
            zeroLine = mpl.lines.Line2D(
                [sqrtS[0], sqrtS[-1]], [0., 0.],
                color='black', linestyle='dashed', linewidth=mpl.rcParams['ytick.major.width']
            )
            axes.add_line(zeroLine)
        
        axes.text(
            0.15, 0.92,
            '$m = {}$ GeV\n$\\Gamma / m = {:g}$%, $g = 1$, ${}$'.format(
                ', '.join(['{:g}'.format(mass) for mass in massPoints]),
                relWidth * 100, partLabel
            ),
            transform=axes.transAxes, horizontalalignment='left', verticalalignment='center'
        )
        
        axes.legend(
            ['$CP$-even', '$CP$-odd'],
            loc='center left', bbox_to_anchor=(0.53, 0.92), frameon=False
        )
        
        fig.savefig('{}_{}.pdf'.format(outNameBase, part))
        plt.close(fig)
    


if __name__ == '__main__':
    
    # Adjust the style
    mpl.rc('xtick', top=True, direction='in')
    mpl.rc('ytick', right=True, direction='in')
    
    massPoints = [400., 600., 800.]
    plot_all(massPoints, 0.01, 'xSec_relW1')
    plot_all(massPoints, 0.1, 'xSec_relW10')
    plot_all(massPoints, 0.25, 'xSec_relW25')
