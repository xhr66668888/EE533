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
from scipy.interpolate import interp1d
from scipy.fftpack import rfft
import cmath
from numpy.random import normal
from itertools import accumulate as acc

def fft_mag(vin, N, T, t):
    fft_sig  = rfft(vin)  
    fft_freqs = np.linspace(0.0, t/(2.0*T), N//2)
    fft_mag = 2.0/N * np.abs(fft_sig[:N//2])
    
    return fft_freqs, fft_mag
    
def generate_noise(mu, sigma, N, T):
    x = []
    y = []
    x = np.linspace(0, N*T, N)
    y = np.random.normal(mu, sigma, N)
       
    return x, y

# textbox properties
props = dict(boxstyle='square', facecolor='wheat', alpha=0.5)

""" FFT of a sampled signal """
f_in = 1e3
N = 1024 
t_sim = 10e-3
T = t_sim / N

# Original signal
t = np.arange(0, t_sim, T) 
v_analog = np.sin(2*np.pi*f_in*t)
v_a_f, v_a_mag = fft_mag(v_analog, N, T, t_sim)

fig, ax = plt.subplots()
ax.plot(v_a_f, v_a_mag)
#ax.stem(1e-3*v_a_f[0:21]/t_sim/2, v_a_mag[0:21], linefmt='tab:blue', markerfmt='bo', basefmt='b',
#    use_line_collection=True)
ax.grid()
ax.set_xlabel(r'Frequency [$1/f_s$]')
ax.set_ylabel('Magnitude [V]')

# Undersampled signal
n_undrsmpl = 64
t_undrsmpl = np.arange(0, t_sim, T*n_undrsmpl)
v_undrsmpl = np.sin(2*np.pi*f_in*t_undrsmpl)
v_resmpl = signal.resample(v_undrsmpl, N)
v_s_f, v_s_mag = fft_mag(v_resmpl, N, T, t_sim)

fig, ax = plt.subplots(2)
ax[0].stem(1e-3*v_a_f[0:21]/t_sim, v_a_mag[0:21], linefmt='tab:blue', markerfmt='bo', basefmt='b',
        use_line_collection=True)
ax[0].set_ylabel('Spectrum of Original Signal')
ax[0].grid()
ax[1].stem(1e-3*v_s_f[0:21]/t_sim, v_s_mag[0:21], linefmt='tab:blue', markerfmt='bo', basefmt='b',
        use_line_collection=True)
ax[1].set_ylabel('Spectrum of Aliased Signal')
ax[1].set_xlabel('Frequency [kHz]')
ax[1].grid()

# Plot time domain signals
fig,ax = plt.subplots(2)
ax[0].plot(1e3*t, v_analog)
ax[0].set_ylabel('Original Signal')
ax[0].grid(which='both',axis='both')
ax[1].plot(1e3*t, v_resmpl)
ax[1].set_ylabel('After Aliasing')
ax[1].set_xlabel('Time [ms]')
ax[1].grid(which='both',axis='both')


""" Quantization Error """
nbits = 4
lsb = 2/2**nbits
v_continuous = np.linspace(-1, 1, 2**20)
v_quantized = np.round(v_continuous / lsb) * lsb

fig, ax = plt.subplots(2)
ax[0].plot(v_continuous, v_continuous, color='tab:blue')
ax[0].plot(v_continuous, v_quantized, color='tab:red')
ax[0].set_ylabel('Quantizer Output')
ax[0].grid(which='both',axis='both')
ax[0].set_yticklabels(['', r'$-V_{FS}$', r'$-V_{FS}/2$', '0', r'$V_{FS}$/2', r'$V_{FS}$'])
ax[0].set_xticklabels(['', r'$-V_{FS}$', r'$-3V_{FS}/4$', r'$-V_{FS}/2$', r'-$V_{FS}$/4', 
    r'0', r'$V_{FS}/4$', r'$V_{FS}/2$', r'$3V_{FS}/4$', r'$V_{FS}$'])

ax[1].plot(v_continuous, v_continuous - v_quantized, color='tab:blue')
ax[1].set_xlabel('Input Voltage')
ax[1].set_ylabel('Quantization Error')
ax[1].grid(which='both',axis='both')
ax[1].set_yticklabels([r'$-V_{LSB}$/2', r'$-V_{LSB}$/4', '0', r'$V_{LSB}$/4', r'$V_{LSB}$/2'])
ax[1].set_yticks([-lsb/2, -lsb/4, 0, lsb/4, lsb/2])
ax[1].set_xticklabels(['', r'$-V_{FS}$', r'$-3V_{FS}/4$', r'$-V_{FS}/2$', r'-$V_{FS}$/4', 
    r'0', r'$V_{FS}/4$', r'$V_{FS}/2$', r'$3V_{FS}/4$', r'$V_{FS}$'])

ax[0].legend( ['Input', 'Output'])
fig.align_ylabels(ax[:])

plt.show()

""" Quantization Noise """
V_fs = 3.3
bits = 16
lsb = V_fs/2**bits
t_sim = 2

# Number of sample points
N = 20000

# Sample spacing
T = t_sim / N
f = 1e3
w = f*2*np.pi
t = np.arange(0, t_sim, T)
tq = np.arange(0,t_sim, T*16)
vn_a_rms = 0

# Input signal
t, vn_a = generate_noise(0, vn_a_rms, N, T)
v_analog = 1*np.sin(w*t) + V_fs/2 + vn_a
v_sampled = 1*np.sin(w*tq) + V_fs/2 + vn_a[0::16]
v_quantized = np.round(v_analog/ lsb) * lsb
vn_q = v_analog - v_quantized

fig, ax = plt.subplots(2)
ax[0].set_title('16-bit Quantization')
ax[0].plot(1e3*t, v_analog, color = 'tab:blue')
ax[0].plot(1e3*t, v_quantized, color = 'tab:red', linestyle='',
    marker='o', markersize=2)
ax[0].set_ylabel('Original and Quantized Signals [V]')
ax[0].grid()

ax[1].plot(1e3*t, 1e6*vn_q)
ax[1].set_ylabel(r'Quantization Error [$\mu V$]')
ax[1].set_xlabel('Time (ms)')
fig.align_ylabels(ax[:])
ax[1].grid()

plt.show()

""" Spectra of Sampled Signal and Quantization Noise """    

# FFT of quantized signal
v_q_f, v_q_mag = fft_mag(v_analog, N, T, t_sim)
print(np.shape(v_q_f))

# Quantization Noise Power Spectral Density
fs, vn_q_den = signal.welch(vn_q, fs=N/t_sim, nperseg=N/4)
vn_q_2 = np.mean(vn_q_den)


#Plot FFT magnitude of quantized signal
fig, ax = plt.subplots(2)
ax[0].stem(v_q_f*T/2, v_q_mag, linefmt='tab:blue', markerfmt='bo', basefmt='b',
    use_line_collection=True)
ax[0].set_ylabel(r'$v_{q}$ Magnitude [$V^2/Hz$]')
#ax[0].set_ylim(1e-17, 1e-13)
ax[0].grid(which='both',axis='both')
# textstr = '\n'.join((
    # r'$R=%.0f$k' % (1, ),
    # r'$f_s=2\cdot f_{ENB}$'))
# ax[0].text(0.95, 0.95, textstr, transform=ax[0].transAxes, fontsize =14,
            # verticalalignment='top', horizontalalignment='right', bbox=props)
            
#Plot PSD of quantization error
ax[1].semilogy(fs[1:-2]/(N/t_sim), vn_q_den[1:-2])
ax[1].semilogy(fs[1:-2]/(N/t_sim), vn_q_2*np.ones(np.size(vn_q_den)-3))
ax[1].set_ylabel(r'$v_{nq}$ PSD [$V^2/Hz$]')
ax[1].set_xlabel(r'Normalized Frequency [$f/f_s$]')
#ax[1].set_ylim(1e-19, 1e-15)
ax[1].grid(which='both',axis='both')
# textstr = '\n'.join((
    # r'$R=%.0f$k' % (1, ),
    # r'$f_s=2\cdot f_{ENB}$'))
# ax[0].text(0.95, 0.95, textstr, transform=ax[0].transAxes, fontsize =14,
            # verticalalignment='top', horizontalalignment='right', bbox=props)

fig.align_ylabels(ax[:])

plt.show()

""" Spectrum of Sampled White Noise """
N = 2**17
Ns = N//2**7  
t_sim = 10e-3
T = t_sim / N  
t = np.linspace(1, N*T, N)
ts = np.linspace(0, N*T, Ns)
nbits = 24
lsb = 2/2**nbits
k = 1.38e-23
Tnom = 300
R = 1e3

# RMS resistor noise in a bandwidth f_enb
vn_R_2 = 4*k*Tnom*R 
f_enb = N/t_sim/2
vn_R_rms = np.sqrt(vn_R_2*f_enb)

# Time-domain and sampled/quantized noise
t, vn_R_t = generate_noise(0, vn_R_rms, N, T)
vn_R_q = np.round(vn_R_t[::N//Ns] / lsb) * lsb

fig, ax = plt.subplots(2)
ax[0].plot(1e3*t, 1e6*vn_R_t)
ax[0].set_ylabel('Original Noise [uV]')
textstr = r'$v_{n(rms)}=%.1f\mu V$' % (np.std(vn_R_t)*1e6, )
ax[0].text(0.95, 0.95, textstr, transform=ax[0].transAxes, fontsize =14,
            verticalalignment='top',horizontalalignment='right', bbox=props)

ax[1].plot(1e3*ts, 1e6*vn_R_q)
ax[1].set_ylabel('Sampled Noise [uV]')
ax[1].set_xlabel('Time [ms]')
textstr = r'$v_{n,smpl(rms)}=%.1f\mu V$' % (np.std(vn_R_q)*1e6, )
ax[1].text(0.95, 0.95, textstr, transform=ax[1].transAxes, fontsize =14,
            verticalalignment='top',horizontalalignment='right', bbox=props)

# Noise power spectral density
f, vn_R_den = signal.welch(vn_R_t, N/t_sim, nperseg=2**10)
fs, vn_R_smpl_den = signal.welch(vn_R_q, Ns/t_sim, nperseg=Ns/4)

#Plot PSD of original and sampled noise
fig, ax = plt.subplots(2)
ax[0].semilogy(1e-6*f[1:-2], vn_R_den[1:-2])
ax[0].set_ylabel(r'4KTR [$V^2/Hz$]')
ax[0].set_xlabel('Frequency [MHz]')
ax[0].set_ylim(1e-18, 1e-16)
ax[0].grid(which='both',axis='both')
textstr = '\n'.join((
    r'$R=%.0f$k' % (1, ),
    r'$f_s=2\cdot f_{ENB}$'))
ax[0].text(0.95, 0.95, textstr, transform=ax[0].transAxes, fontsize =14,
            verticalalignment='top', horizontalalignment='right', bbox=props)

ax[1].semilogy(fs[1:-2]/(Ns/t_sim), vn_R_smpl_den[1:-2])
ax[1].set_ylabel('4KTR Sampled [$V^2/Hz$]')
ax[1].set_xlabel(r'Normalized Frequency [$f/f_s$]')
ax[1].grid(which='both',axis='both')
ax[1].set_ylim(1e-18, 1e-12)
textstr = '\n'.join((
    r'$R=%.0f$k' % (1, ),
    r'$f_s=2\cdot f_{ENB}/128$'))
ax[1].text(0.95, 0.95, textstr, transform=ax[1].transAxes, fontsize =14,
            verticalalignment='top',horizontalalignment='right', bbox=props)

fig.align_ylabels(ax[:])

plt.show()

""" Oversampling """

# PSD of oversampled noise
f_os, vn_R_os_den = signal.welch(vn_R_t, 4*N/t_sim, nperseg=2**12)

fig, ax = plt.subplots()
ax.semilogy(f_os[1:-1]/(4*N/t_sim), vn_R_os_den[1:-1], color='tab:blue', label='4x Oversampled')
ax.semilogy(f[1:-1]/(N/t_sim), vn_R_den[1:-1], color='tab:red', label='Sampled at Nyquist Rate')
ax.grid(which='both',axis='both')
ax.set_ylabel(r'PSD $V^2/Hz$')
ax.set_ylim(1e-18, 1e-16)
ax.set_xlabel(r'Normalized Frequency [$f/f_s$]') 
ax.legend()
ax.legend(loc='upper center', ncol=2, fancybox=True, 
           shadow=True, bbox_to_anchor=(0.5,1.1) )

plt.show()