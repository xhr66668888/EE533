import os
import sys
import cmath
import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy import signal
from scipy.integrate import quad
from scipy import integrate
from scipy import signal
import cmath
from numpy.random import normal
from itertools import accumulate as acc


""" Johnson noise spectrum """
k = 1.38e-23
f = np.logspace(0,7,num=300)
T = 300
R = 10e3

en_10k = np.sqrt(4*k*T*R)

vn_rms = []
for fbw in f:
    vn_rms.append(np.sqrt(en_10k**2*(fbw)))
vn_rms = np.asarray(vn_rms)


fig, ax = plt.subplots(3)

# Plot noise voltage spectrum
ax[0].semilogx(f, 1e9*en_10k*np.ones(np.shape(f)))
ax[0].set_xticklabels([])
ax[0].set_ylabel(r'$e_n [nV/\sqrt{Hz}]$')
ax[0].set_title('$10k\Omega$ Resistor Noise')
ax[0].grid()
str0 = r'$e_n = \sqrt{4kTR}$' 
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax[0].text(0.05, 0.85, str0, transform=ax[0].transAxes, fontsize =14,
            verticalalignment='top', bbox=props)

# Plot noise power spectrum
ax[1].semilogx(f, 1e9**2*en_10k**2*np.ones(np.shape(f)))
ax[1].set_ylabel(r'${e_n}^2$ [${nV}^2/Hz$]')
ax[1].set_xticklabels([])
ax[1].grid()
str1 = r'${e_n}^2 = 4kTR$' 
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax[1].text(0.05, 0.85, str1, transform=ax[1].transAxes, fontsize =14,
            verticalalignment='top', bbox=props)
            
# Plot RMS voltage noise as a function of bandwidth
ax[2].semilogx(f, 1e6*vn_rms)
ax[2].grid()
ax[2].set_ylabel(r'$v_{n(rms)}$ [$\mu V$]')
ax[2].set_xlabel(r'Frequency (Bandwidth $\Delta f)$ [Hz]')
str2 = r'$v_{n(rms)} = \sqrt{4kTR\Delta f}$' 
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax[2].text(0.05, 0.85, str2, transform=ax[2].transAxes, fontsize =14,
            verticalalignment='top', bbox=props)
fig.align_ylabels(ax[:])


""" Johnson noise amplitude """
vn_range = np.linspace(-6*en_10k, 6*en_10k, 10000)
vn_ampl = (1/np.sqrt(2*np.pi))*np.exp(-np.power(vn_range,2)/2/en_10k**2)
p_3sigma = np.sum(vn_ampl)

# stats_txt = '\n'.join((
    # r'$R_{nom}=%.0fk\Omega$' % (1e-3*R_nom[65], ), 
    # r'$R_{min}=%.2f \cdot R_{nom}$' % (R_min[0]/R_nom[65], ),
    # r'$R_{max}=%.2f \cdot R_{nom}$' % (R_max[-1]/R_nom[65], )))
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# ax.text(0.05, 0.95, stats_txt, transform=ax.transAxes, fontsize =14,
            # verticalalignment='top', bbox=props)

fig, ax = plt.subplots()
ax.plot(1e9*vn_range, vn_ampl)
ax.set_xlabel('Instantaneous Voltage Value [nV]')
ax.set_ylabel('Probability Density')
ax.set_title('Noise Amplitude Probability Distribution')
ax.set_ylim(-1e9*3*en_10k, 1e9*3*en_10k)
labels = (r'$-3v_n$', r'$-2v_n$', r'$-v_n$', '0', r'$v_n$',
          r'$2v_n$', r'$3v_n$')
ax.set_xlim(-1e9*3*en_10k, 1e9*3*en_10k)
labels = (r'$-3v_n$', r'$-2v_n$', r'$-v_n$', '0', r'$v_n$',
          r'$2v_n$', r'$3v_n$')
ax.set_xticks(1e9*en_10k*np.linspace(-3,3,num=7))
ax.set_xticklabels(labels)
ax.grid()


""" Equivalent Noise Bandwidth """
f = np.logspace(0.1, 4 , 1000)
w = 2*np.pi*f
R = 10e3
C = 1e-6
tau = R*C
RC_mag = 1/np.sqrt(1+(w*tau)**2)

fig, ax = plt.subplots(2)
ax[0].semilogx(f, RC_mag)
ax[0].set_xlim(f[0], f[-1])
ax[0].set_xticks(np.logspace(0.1,4,5))
ax[1].set_xscale("log")
ax[0].set_xticklabels([])
ax[0].set_ylabel('Magnitude [V/V]')
ax[0].set_title('Equivalent Noise Bandwidth')
ax[0].grid()

ax[1].hlines(1, 0, 1/4/tau, color='tab:blue')
ax[1].hlines(0, 1/4/tau, f[-1], color='tab:blue')
ax[1].vlines(1/4/tau, 0, 1, color='tab:blue')
ax[1].set_xlim(f[0], f[-1])
ax[1].set_xticks(np.logspace(0.1,4,5))
ax[1].set_xscale("log")
ax[1].set_ylabel('Magnitude [V/V]')
ax[1].set_xlabel('Frequency [Hz]')
ax[1].grid()

""" Flicker Noise """
k = 1.38e-23
f = np.logspace(-1,5,num=300)
T = 300
R = 10e3

#flicker noise corner
f_c = 100
e_n_w = np.sqrt(4*k*T*R)
e_n_tot = e_n_w*np.sqrt(1+f_c/f)
#e_n_tot_2 = np.power((e_n_w*np.ones(np.shape(f))),2) + np.power(e_n_f
#e_n_tot = np.sqrt(e_n_tot_2)

# Plot noise voltage spectrum
fig, ax = plt.subplots()
ax.loglog(f, 1e9*(e_n_tot))
ax.set_ylabel(r'Noise Voltage Density, $e_n$ $[nV/\sqrt{Hz}]$')
ax.set_xlabel(r'$Frequency [Hz]$')
ax.set_ylim(8, 1e3)
ax.set_title('1/f Noise')
ax.grid()
       
 
""" RMS Noise vs Bandwidth """
k = 1.38e-23
f = np.logspace(-1,5,num=1000)
T = 300
R = 10e3

#flicker noise corner
f_c = 100

e_n_w_2 = 4*k*T*R
e_n_w = np.sqrt(e_n_w_2)
e_n_tot = e_n_w*np.sqrt(1+f_c/f)
e_n_tot_2 = e_n_tot**2

vn2 = integrate.cumtrapz(e_n_tot_2, f, initial=0)
vn_rms = np.sqrt(vn2)
vn_w_2 = integrate.cumtrapz(e_n_w_2*np.ones(np.shape(f)), f, initial=0)
vn_w_rms = np.sqrt(vn_w_2)


# Plot noise voltage spectrum
fig, ax = plt.subplots(2)
ax[0].loglog(f, 1e9*(e_n_tot), label=r'1/f + white noise')
ax[0].loglog(f, 1e9*(e_n_w*np.ones(np.shape(f))), color='tab:red', label = 'white noise only')
ax[0].set_ylabel(r'Noise Voltage Density, $e_n$ $[nV/\sqrt{Hz}]$')
ax[0].grid()

# Plot the RMS noise as a function of bandwidth
ax[1].semilogx(f, 1e6*vn_rms)
ax[1].semilogx(f, 1e6*vn_w_rms, color='tab:red')
ax[1].set_ylabel(r'RMS Voltage Noise, $[\mu V]$')
ax[1].set_xlabel(r'Frequency [Hz]')
ax[1].grid()
fig.align_ylabels(ax[:])

ax[0].legend()
ax[0].legend(loc='upper center', ncol=2, fancybox=True, 
           shadow=True, bbox_to_anchor=(0.5,1.2) )
       
plt.show()