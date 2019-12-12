#!/usr/bin/env python

"""Plots partial H->tt width."""

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


gF = 1.1663787e-5  # GeV^(-2)
mt = 172.5  # GeV


def width(mass, cpState):
    """Compute partial H->tt width."""
    
    if mass <= 2 * mt:
        return 0.
    
    w = 3 * gF * mt**2 * mass / (4 * math.pi * math.sqrt(2))
    beta = math.sqrt(1 - (2 * mt / mass)**2)
    
    if cpState == 'even':
        return w * beta**3
    elif cpState == 'odd':
        return w * beta
    else:
        raise RuntimeError('Unknown CP state requested.')


if __name__ == '__main__':
    
    # Adjust the style
    mpl.rc('xtick', top=True, direction='in')
    mpl.rc('ytick', right=True, direction='in')
    
    
    masses = np.linspace(340., 1000., num=500, dtype=np.float32)
    width_even = np.vectorize(lambda mass: width(mass, 'even'))
    width_odd = np.vectorize(lambda mass: width(mass, 'odd'))
    
    fig = plt.figure()
    axes = fig.add_subplot(111)
    
    axes.plot(masses, width_even(masses), color='steelblue', label='$CP$-even')
    axes.plot(masses, width_odd(masses), color='orange', label='$CP$-odd')
    
    axes.set_xlim(masses[0], masses[-1])
    axes.set_ylim(bottom=0.)
    
    axes.set_xlabel(r'$m_\Phi$ [GeV]', ha='right', x=1.)
    axes.set_ylabel(r'$\Gamma_{\Phi\to t\bar t}$ [GeV]', ha='right', y=1.)
    
    axes.plot([], linestyle='None', label='$g = 1$')
    axes.legend(loc='upper left', bbox_to_anchor=(0.05, 0.95), frameon=False)
    
    fig.savefig('width.pdf')
    plt.close(fig)
