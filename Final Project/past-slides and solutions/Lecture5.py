import os
import sys
import cmath
import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy import signal
import cmath
from numpy.random import normal


""" Resistor accuracy """
T = np.linspace(-40, 125, num=166)
R_0 = 1e3
tol = 0.001
tempco = 100/1e6
R_nom = R_0*( 1 + tempco*(T - 25) )
R_min = R_0*(1-tol)*( 1 + tempco*(T - 25) )
R_max = R_0*(1+tol)*( 1 + tempco*(T - 25) )
print(R_nom[60:70])
stats_txt = '\n'.join((
    r'$R_{nom}=%.0fk\Omega$' % (1e-3*R_nom[65], ), 
    r'$R_{min}=%.2f \cdot R_{nom}$' % (R_min[0]/R_nom[65], ),
    r'$R_{max}=%.2f \cdot R_{nom}$' % (R_max[-1]/R_nom[65], )))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig, ax = plt.subplots()
ax.plot(T, 1e-3*R_nom, label='Nominal')
ax.plot(T, 1e-3*R_min, color='tab:red', label='Min')
ax.plot(T, 1e-3*R_max, color='tab:green', label='Max')
ax.set_xlabel('Temperature [C]')
ax.set_ylabel(r'Resistance [k$\Omega$]')
ax.grid()
ax.text(0.05, 0.95, stats_txt, transform=ax.transAxes, fontsize =14,
            verticalalignment='top', bbox=props)
plt.show()

""" Monte Carlo simulation of an inverting amplifier """
tolerance = 0.001
R_i_mu = 1e3;
R_i_sigma = R_i_mu*tolerance/3
R_i = normal(R_i_mu, R_i_sigma, 10000)
R_f_mu = 10e3;
R_f_sigma = R_f_mu*tolerance/3
np.random.seed()
R_f = normal(R_f_mu, R_f_sigma, 10000)

G = R_f/R_i
G_sigma = np.std(G)
G_mu = np.mean(G)
bins = np.linspace(G_mu-6*G_sigma, G_mu+6*G_sigma, num=50)


# plot histogram
stats_txt = '\n'.join((
    r'$\mu=%.2f$' % (G_mu, ),
    r'$+6\sigma=%.2f$' % (G_mu + 6*G_sigma, ),
    r'$-6\sigma=%.2f$' % (G_mu - 6*G_sigma, )))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig, ax = plt.subplots()
ax.hist(G, bins=bins)
ax.set_xlabel('Amplifier Gain [V/V]')
ax.set_ylabel('Number of Occurrences')
ax.grid()
ax.set_title('Amplifier Monte Carlo (10,000 runs)')
ax.text(0.05, 0.95, stats_txt, transform=ax.transAxes, fontsize =14,
            verticalalignment='top', bbox=props)
plt.show()
 
""" Gain error """
A_dc = 1e7
f_T = 1e6
tau = 1/(2*np.pi*f_T/A_dc)
Av_ol = signal.TransferFunction([A_dc/tau], [1, 1/tau])
w = 2*np.pi*np.logspace(-2,7,num=50)
w, mag, phase = Av_ol.bode(w=w)       # rad/s, dB, degrees 
mag_volts = 10**(mag/20)
f = w/2/np.pi   

# Closed-loop response and associated error
b_100 = 0.01
G_100 = mag_volts/(1 + b_100*mag_volts)
#Av_100 = signal.TransferFunction([A_dc/(1+A_dc*b_100)],[tau/(1+A_dc*b_100), 1])
#w, mag_100, phase = Av_100.bode(w=w)       # rad/s, dB, degrees 
#s = 1j*w
#Av_100 = A_dc/(1+s*tau+b_100*A_dc)
#G_100 = np.absolute(Av_100)
#G_100 = np.power(10, mag_100/20)
delta_G_100 = b_100*(1/b_100 - G_100)

b_1000 = 0.001
G_1000 = mag_volts/(1 + b_1000*mag_volts)
delta_G_1000 = b_1000*(1/b_1000 - G_1000)

# Plot the frequency response
fig, ax1 = plt.subplots()
color = 'tab:blue'
fig.suptitle('Opamp Open-Loop Frequency Response')
ax1.loglog(f, mag_volts, color=color)
ax1.loglog(f, G_100)
#ax1.loglog(f,G_100_2)
ax1.grid()
ax1.set_ylabel('Open-Loop Gain [V/V]')
ax1.set_ylim(1e4, 2e7)
ax1.set_xlim(.01, 100)

ax2 = ax1.twinx()
ax2.set_ylabel('Gain Error [%]')
ax2.set_xlim(.01, 100)

color = 'tab:red'
ax2.loglog(f, 100*delta_G_100, color=color)
ax2.loglog(f, 100*delta_G_1000, color=color)
ax2.set_ylim(.001, 2)


""" Differential Signals with noise """
f = 1e3
w = f*2*np.pi
t = np.linspace(0,3e-3,num=300)
mu = 0
sigma = 100e-6
V_dd = 3.3

V_cm = V_dd/2
v_plus = V_cm + 1e-3*np.sin(w*t)
v_minus = V_cm - 1e-3*np.sin(w*t)
v_noise = np.random.normal(mu, sigma, 300)

vd_plus = v_plus + v_noise
vd_minus = v_minus + v_noise
v_diff = vd_plus - vd_minus

fig, ax = plt.subplots(3)
vplus_line = ax[0].plot(1e3*t, vd_plus)
vminus_line = ax[1].plot(1e3*t, vd_minus)
vdiff_line = ax[2].plot(1e3*t, 1e3*v_diff)

ax[0].set_ylabel('$v_+$ [V]')
ax[1].set_ylabel('$v_-$ [V]')
ax[2].set_ylabel('$v_+ - v_-$ [mV]')
ax[2].set_xlabel('Time [ms]')
ax[0].grid()
ax[1].grid()
ax[2].grid()

""" Asymmetric differential signals """
f = 1e3
w = f*2*np.pi
t = np.linspace(0,3e-3,num=300)
mu = 0
sigma = 100e-6
V_dd = 3.3

V_cm = V_dd/2
v_plus = V_cm + 1e-3*np.sin(w*t)
v_minus = V_cm - 1e-3*np.sin(w*t)
v_noise = np.random.normal(mu, sigma, 300)

vd_plus = v_plus + v_noise
vd_minus = V_cm + v_noise
v_diff = vd_plus - vd_minus

fig, ax = plt.subplots(3)
vplus_line = ax[0].plot(1e3*t, vd_plus)
vminus_line = ax[1].plot(1e3*t, vd_minus)
vdiff_line = ax[2].plot(1e3*t, 1e3*v_diff)

ax[0].set_ylabel('$v_+$ [V]')
ax[1].set_ylabel('$v_-$ [V]')
ax[1].set_ylim(1.65-.0013, 1.65 + 0.0013)
ax[2].set_ylabel('$v_+ - v_-$ [mV]')
ax[2].set_xlabel('Time [ms]')
ax[0].grid()
ax[1].grid()
ax[2].grid()

""" Common-mode signals """
f = 1e3
w = f*2*np.pi
t = np.linspace(0,3e-3,num=300)
mu = 0
sigma = 100e-6
V_dd = 3.3

V_cm = V_dd/2
v_plus = V_cm + 1e-3*np.sin(w*t)
v_minus = V_cm - 1e-3*np.sin(w*t)
v_noise = np.random.normal(mu, sigma, 300)

vd_plus = v_plus + v_noise
vd_minus = v_minus + v_noise
v_cm = (vd_plus + vd_minus)/2

fig, ax = plt.subplots(3)
vplus_line = ax[0].plot(1e3*t, vd_plus)
vminus_line = ax[1].plot(1e3*t, vd_minus)
vcm_line = ax[2].plot(1e3*t, v_cm)

ax[0].set_ylabel('$v_+$ [V]')
ax[1].set_ylabel('$v_-$ [V]')
ax[1].set_ylim(1.65-.0013, 1.65 + 0.0013)
ax[2].set_ylabel('$(v_+ + v_-)/2$ [V]')
ax[2].set_ylim(1.65-.0013, 1.65 + 0.0013)
ax[2].set_xlabel('Time [ms]')
ax[0].grid()
ax[1].grid()
ax[2].grid()
#plt.show()
