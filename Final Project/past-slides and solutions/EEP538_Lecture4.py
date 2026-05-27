import os
import sys
import cmath
import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy import signal


""" Opamp open-loop gain characteristic """
A_dc = 1e4
f_T = 1e6
tau = 1/(2*np.pi*f_T/A_dc)
Av_ol = signal.TransferFunction([A_dc], [tau, 1])
w = 2*np.pi*np.logspace(0,7,num=50)
w, mag, phase = Av_ol.bode(w=w)       # rad/s, dB, degrees 
f = w/2/np.pi   

# Plot the frequency response
fig, axs = plt.subplots(2)
fig.suptitle('Opamp Open-Loop Frequency Response')
axs[0].semilogx(f, mag)
axs[0].grid()
axs[0].set_ylabel('Magnitude [dB]')
axs[0].set_ylim(-10, 83)
axs[0].set_xlim(1, 1e7)
axs[1].semilogx(f,phase)
axs[1].grid()
axs[1].set_ylabel('Phase [deg]')
axs[1].set_xlabel('Frequency [Hz]')
axs[1].set_ylim(-100, 10)
axs[1].set_xlim(1, 1e7)
fig.align_ylabels(axs[:])
plt.show()

""" Opamp constant gain-bandwidth """
A_dc = 1e4
f_T = 1e6
tau = 1/(2*np.pi*f_T/A_dc)
beta = np.asarray([0.01, 0.1, 1])
fig, axs = plt.subplots(2)
for b in beta:
    Av_cl = signal.TransferFunction([A_dc], [tau, 1 + b*A_dc])
    w = 2*np.pi*np.logspace(0,7,num=50)
    w, mag, phase = Av_cl.bode(w=w)       # rad/s, dB, degrees 
    f = w/2/np.pi   

    # Plot the frequency response for multiple values of beta
    fig.suptitle('Opamp Closed-Loop Frequency Response')
    axs[0].semilogx(f, mag)
    axs[0].grid()
    axs[0].set_ylabel('Magnitude [dB]')
    #axs[0].set_ylim(-10, 83)
    axs[0].set_xlim(1, 1e7)
    axs[1].semilogx(f,phase)
    axs[1].grid()
    axs[1].set_ylabel('Phase [deg]')
    axs[1].set_xlabel('Frequency [Hz]')
    axs[1].set_ylim(-100, 10)
    axs[1].set_xlim(1, 1e7)
    fig.align_ylabels(axs[:])
plt.show()


fig, axs = plt.subplots(2)
for b in beta:
    Av_cl = signal.TransferFunction([A_dc], [tau, 1 + b*A_dc])
    tin = np.linspace(0,20e-6,100)
    u_step = np.concatenate( (0, np.ones(99)), axis=None)
    tout,vout = signal.step(Av_cl, X0=None, T=tin)
   
    # Plot the frequency response for multiple values of beta
    fig.suptitle('Opamp Closed-Loop Step Response')
    axs[0].plot(1e6*tout, b*vout)
    axs[0].grid()
    axs[0].set_ylabel(r'$\beta V_o$ [V]')
    #axs[0].set_xlim(1, 1e7)
    axs[1].plot(1e6*tin,u_step)
    axs[1].grid()
    axs[1].set_ylabel('Input Voltage [V]')
    axs[1].set_xlabel('Time [$\mu $s]')
    #axs[1].set_ylim(-100, 10)
    #axs[1].set_xlim(1, 1e7)
    fig.align_ylabels(axs[:])
plt.show()

""" Differential Signals with noise """
bits = 8
f = 1e3
w = f*2*np.pi
t = np.linspace(0,3e-3,num=300)
mu = 0
sigma = 100e-6
bins = np.linspace(-1, 1, num=2**bits)


v_sine = 1e-3*np.sin(w*t)
v_noise = np.random.normal(mu, sigma, 300)
v_adc = [0]*v_sine.size 
inds = np.digitize(100*v_sine, bins)
for ind in range(v_sine.size):
    v_adc[ind] = bins[inds[ind]]



v_sensor = v_sine + v_noise

fig, ax = plt.subplots(3)
sensor_line = ax[0].plot(1e3*t, 1e3*v_sensor, linewidth=4)
amp_line = ax[1].plot(1e3*t, 1e3*100*v_sine, linewidth=4)
adc_line = ax[2].plot(1e3*t, v_adc, linewidth=4)

ax[0].set_ylabel('$v_+$ [mV]')
ax[1].set_ylabel('$v_-$ [mV]')
ax[2].set_ylabel('$v_+ - v_-$ [mV]')
ax[2].set_xlabel('Time [ms]')
plt.show()