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

""" First Order Response """
tau = 1e-3
f = np.logspace(0, 4, num = 1000)
w = 2*np.pi*f
mag_first = (1/np.sqrt(1+(w*tau)**2))               
tin = np.linspace(0,10e-3,100) 
step_first = (1 - np.exp(-tin/tau))

# Plot the frequency response
fig, axs = plt.subplots(2)
fig.suptitle('$1^{st}$ Order System Magnitude and Step Responses')
axs[0].semilogx(f, 20*np.log10(mag_first))
axs[0].grid()
axs[0].set_ylabel('Magnitude Response [dB]')
axs[0].set_xlabel('Frequency [Hz]')

axs[1].plot(1e3*tin, step_first)
axs[1].grid()
axs[1].set_ylabel('Step Response')
axs[1].set_xlabel('Time [ms]')
plt.show()

""" RC filter magnitude and step responses """
RC_mag = []
RC_step = []
tau = np.logspace(-5,-2, num = 4)
f = np.logspace(0, 6, num = 1000)
w = 2*np.pi*f
tin = np.linspace(0,1e-2,1000) 

for t in tau: 
    RC_mag.append(1/np.sqrt(1+(w*t)**2))
    RC_step.append(1-np.exp(-tin/t))
    
# Plot the frequency response
fig, axs = plt.subplots(2)
for mag in RC_mag:
    axs[0].semilogx(f, 20*np.log10(mag))

axs[0].legend( [r'$\tau = 10\mu s$', r'$100\mu s$', r'$1 ms$', r'$10 ms$'],loc='upper center', ncol=5, fancybox=True, 
           shadow=True, bbox_to_anchor=(0.5,1.2))
axs[0].set_ylim(-40, 6)
axs[0].grid()
axs[0].set_ylabel('Magnitude Response [dB]')
axs[0].set_xlabel('Frequency [Hz]')
#axs[0].set_title('RC Lowpass Filter Magnitude and Step Responses')

for trans in RC_step:
    axs[1].plot(1e3*tin, trans)   
axs[1].set_xlabel('Time [ms]')    
axs[1].set_ylabel('Step Response')
axs[1].grid()

fig.align_ylabels(axs[:])


plt.show()

""" Second Order Response """
tau = 1e-3
w0 = 1/tau
s = 1j*w
Q = 1.5
mag_second = (abs(w0**2/(s**2 + s*w0/Q + w0**2)))           
tin = np.linspace(0,10e-3,100) 


sys_second = signal.TransferFunction([w0**2], [1, w0/Q, w0**2])
w, mag_second, phase = sys_second.bode()       # rad/s, dB, degrees 
f = w/2/np.pi 
tout,step_second = signal.step(sys_second, X0=None, T=tin)

# Plot the frequency response
fig, axs = plt.subplots(2)
fig.suptitle('$2^{nd}$ Order System Magnitude and Step Responses')
axs[0].semilogx(f, mag_second)
axs[0].grid()
axs[0].set_ylabel('Magnitude Response [dB]')
axs[0].set_xlabel('Frequency [Hz]')

axs[1].plot(1e3*tin, step_second)
axs[1].grid()
axs[1].set_ylabel('Step Response')
axs[1].set_xlabel('Time [ms]')
plt.show()

""" Second Order Response """
tau = 1e-3
w0 = 1/tau
s = 1j*w
Q = np.asarray([0.5, 0.707, 1, 2, 5])        
tin = np.linspace(0,10e-3,100) 

fig, axs = plt.subplots(2)
fig.suptitle('$2^{nd}$ Order System Magnitude and Step Responses')

mags = []
steps = []

for q in Q:
    sys_second = signal.TransferFunction([w0**2], [1, w0/q, w0**2])
    w, mag_second, phase = sys_second.bode()       # rad/s, dB, degrees 
    f = w/2/np.pi 
    tout,step_second = signal.step(sys_second, X0=None, T=tin)

    
    # Plot the frequency response
    axs[0].semilogx(f, mag_second, label = q)
    axs[0].grid()
    axs[0].set_ylabel('Magnitude Response [dB]')
    axs[0].set_xlabel('Frequency [Hz]')

    axs[1].plot(1e3*tin, step_second)
    axs[1].grid()
    axs[1].set_ylabel('Step Response')
    axs[1].set_xlabel('Time [ms]')
fig.align_ylabels(axs[:])
axs[0].legend( ["Q = 0.5", "0.707", "1", "2", "5"],loc='upper center', ncol=5, fancybox=True, 
           shadow=True, bbox_to_anchor=(0.5,1.2))
plt.show()

""" 6th Order Chebyshev """
b, a = signal.cheby1(6, 0.5, 2*np.pi*5000, 'low', analog=True)
cheby_6 = signal.TransferFunction(b, a)
w, h = signal.freqs(b,a)
f = w/2/np.pi


# Plot the magnitude response
fig, ax = plt.subplots()
ax.semilogx(f, 20*np.log10(abs(h)))
ax.set_ylim(-50, 10)
#ax.set_xlim(0.1, 50e3)
ax.set_title(r'$6^{th}$ Order Chebyshev Filter with 0.5dB Ripple')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.grid()
plt.show()

# Plot the step response
tin = np.linspace(0, 1e-3, 1000)
tout,step_cheby = signal.step(cheby_6, X0=None, T=tin)
fig, ax = plt.subplots()
ax.plot(1e6*tout, step_cheby)
#ax.set_ylim(-50, 10)
#ax.set_xlim(0.1, 50e3)
ax.set_title(r'$6^{th}$ Order Chebyshev Filter Step Response')
ax.set_xlabel(r'Time $[\mu s]$')
ax.set_ylabel('Step Response')
ax.grid()
plt.show()

""" 2nd Order Butterworth """
b, a = signal.butter(2, 2*np.pi*5000, 'low', analog=True)
butter_4 = signal.TransferFunction(b, a)
f = np.logspace(1, 5, 100)
w = 2*np.pi*f
w, mag_butter, phase_butter = butter_4.bode(w)
f = w/2/np.pi


# Plot the magnitude response
fig, ax = plt.subplots()
ax.semilogx(f, mag_butter)
# ax.set_ylim(-50, 10)
# ax.set_xlim(100, 100e3)
ax.set_title(r'$2^{nd}$ Order Butterworth Filter with $f_c = 5kHz$')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.grid(which='both', axis='both')
plt.show()

# Plot the step response
# tin = np.linspace(0, 1e-3, 1000)
# tout,step_butter = signal.step(butter_4, X0=None, T=tin)
# fig, ax = plt.subplots()
# ax.plot(1e6*tout, step_cheby)
# #ax.set_ylim(-50, 10)
# #ax.set_xlim(0.1, 50e3)
# ax.set_title(r'$6^{th}$ Order Chebyshev Filter Step Response')
# ax.set_xlabel(r'Time $[\mu s]$')
# ax.set_ylabel('Step Response')
# ax.grid()
# plt.show()

""" 2nd Order Chebyshev """
b, a = signal.cheby1(2, .5, 2*np.pi*5000, 'low', analog=True)
cheby_4 = signal.TransferFunction(b, a)
w, mag_cheby, phase_cheby = cheby_4.bode(w)
f = w/2/np.pi

print(a)
print(b)
print(a[1]/np.sqrt(a[2]))

# Plot the magnitude response
fig, ax = plt.subplots()
ax.semilogx(f, mag_cheby)
ax.set_ylim(-50, 10)
ax.set_xlim(100, 100e3)
ax.set_title(r'$2^{nd}$ Order Chebyshev Filter with 0.5dB Ripple')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.grid(which='both', axis='both')
plt.show()

# Plot the step response
# tin = np.linspace(0, 1e-3, 1000)
# tout,step_butter = signal.step(butter_4, X0=None, T=tin)
# fig, ax = plt.subplots()
# ax.plot(1e6*tout, step_cheby)
# #ax.set_ylim(-50, 10)
# #ax.set_xlim(0.1, 50e3)
# ax.set_title(r'$6^{th}$ Order Chebyshev Filter Step Response')
# ax.set_xlabel(r'Time $[\mu s]$')
# ax.set_ylabel('Step Response')
# ax.grid()
# plt.show()

""" 2nd Order Bessel """
b, a = signal.bessel(2, 2*np.pi*5000, 'low', analog=True)
bessel_4 = signal.TransferFunction(b, a)
w, mag_bessel, phase_bessel = bessel_4.bode(w)
f = w/2/np.pi


# Plot the magnitude response
fig, ax = plt.subplots()
ax.semilogx(f, mag_bessel)
ax.set_ylim(-50, 10)
ax.set_xlim(100, 100e3)
ax.set_title(r'$2^{nd}$ Order Bessel Filter with $f_c = 5kHz$')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.grid(which='both', axis='both')
plt.show()

# Plot the step response
# tin = np.linspace(0, 1e-3, 1000)
# tout,step_butter = signal.step(butter_4, X0=None, T=tin)
# fig, ax = plt.subplots()
# ax.plot(1e6*tout, step_cheby)
# #ax.set_ylim(-50, 10)
# #ax.set_xlim(0.1, 50e3)
# ax.set_title(r'$6^{th}$ Order Chebyshev Filter Step Response')
# ax.set_xlabel(r'Time $[\mu s]$')
# ax.set_ylabel('Step Response')
# ax.grid()
# plt.show()


""" Magnitude Response Comparison """
fig, ax = plt.subplots()

ax.semilogx(f, mag_butter)
ax.semilogx(f, mag_bessel)
ax.semilogx(f, mag_cheby)

ax.grid(which='both', axis='both')
ax.set_title(r'$2^{nd}$ Order Filter Magnitude Response Comparison')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.set_ylim(-50, 2)
ax.legend( ['Butterworth', 'Bessel', 'Chebyshev'])
plt.show()

""" Step Response Comparison """
tin = np.linspace(0, 1e-3, 1000)
tout1, step_butter = signal.step(butter_4, X0=None, T=tin)
tout2, step_bessel= signal.step(bessel_4, X0=None, T=tin)
tout3, step_cheby = signal.step(cheby_4, X0=None, T=tin)

fig, ax = plt.subplots()
ax.plot(1e6*tout1, step_butter)
ax.plot(1e6*tout2, step_bessel)
ax.plot(1e6*tout3, step_cheby)
ax.grid()

ax.set_title(r'$2^{nd}$ Order Filter Step Response Comparison')
ax.set_xlabel(r'Time $[\mu s]$')
ax.set_ylabel('Normalized Step Response')
ax.legend( ['Butterworth', 'Bessel', 'Chebyshev'])



plt.show()