# Phase 2 LTspice guide

这个文件是给你跑 LTspice 和补截图用的。最后 Canvas 主提交物是
`EE533_Project_Phase2.ipynb`。如果 Canvas 允许附件，可以把 `.asc` 和截图一起打包；如果只允许一个文件，就把截图放进 `screenshots/` 后重新运行 notebook，让图片嵌入 notebook 输出里。

## 0. 先看设计数值

Phase 2 notebook 里已经把滤波器和 ADC 算完。关键值如下：

| item | value |
| --- | ---: |
| instrumentation amplifier gain | 99.764 V/V |
| input-referred white noise density from Phase 1 budget | 9.112 nV/sqrt(Hz) |
| output noise density at filter input | 0.909 uV/sqrt(Hz) |
| maximum allowed output rms noise for 75 dB | 125.7 uVrms |
| chosen filter | 4th-order Butterworth lowpass |
| filter cutoff used in design | 13.5 kHz |
| attenuation at 10 kHz | about 0.377 dB |
| equivalent noise bandwidth | about 13.85 kHz |
| ADC | ADS8326, 16 bit, 100 kS/s used, 250 kS/s max |

Filter is implemented as two unity-gain Sallen-Key stages. Put the low-Q stage first and the high-Q stage second.

| stage | Q | R1 | R2 | C feedback from first RC node to op amp output | C from op amp input node to Vref |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.541 | 10 kOhm | 10 kOhm | 1.276 nF | 1.089 nF |
| 2 | 1.307 | 10 kOhm | 10 kOhm | 3.081 nF | 451.2 pF |

In LTspice you can type these exact values directly, for example `1.276n` and `451.2p`.

Important Phase 1 correction: for `.noise`, the differential input source must have `AC 1`. If `Vdiff` is left as `AC 0`, LTspice can report a wrong input-referred noise curve. The old screenshot that gives about 9.48 uVrms from 0.1 Hz to 10 kHz is not consistent with the 9 nV/sqrt(Hz) white-noise budget, so rerun this part before final submission.

## 1. Phase 1 amplifier screenshots to carry over

Use your Phase 1 instrumentation amplifier schematic.

Check these before taking screenshots:

1. `Vref` is made with a 10 kOhm / 10 kOhm divider and a voltage buffer, not an ideal voltage source.
2. The balanced bridge/common-mode nodes are near 2.5 V.
3. The differential test source used for `.noise` has `AC 1`.

Run `.op` and take:

`screenshots/phase1_amp_op.png`

This screenshot should show the amplifier schematic, component values, op amp part names, and DC node voltage labels.

Run unfiltered noise:

```spice
.noise V(amp_out) Vdiff dec 100 0.01 100Meg
```

Plot `V(onoise)` for output noise and `V(inoise)` for input-referred noise. Use the error log for the integrated rms value. Take:

`screenshots/phase1_unfiltered_noise.png`

The notebook uses the Phase 1 white-noise budget for filter sizing, but this LTspice screenshot is still needed for the rubric.

## 2. Standalone filter schematic

Create a new LTspice schematic first, just for the filter. This makes debugging much easier.

### 2.1 Reference node

Make a real 2.5 V reference:

1. `VDD = 5 V`.
2. Two 10 kOhm resistors as a divider from 5 V to ground.
3. Use one op amp as a unity-gain buffer.
4. Name the buffered node `Vref`.

For the filter op amp, use `ADA4661-2` if it is available in your LTspice library. If not, use `UniversalOpamp2` only for first debugging, then replace it with an available rail-to-rail op amp model for the final screenshot.

### 2.2 One Sallen-Key stage wiring

For each stage:

1. Input node goes through `R1=10k` to a middle node.
2. Middle node goes through `R2=10k` to the op amp non-inverting input node.
3. Op amp is a voltage follower: output tied to the inverting input.
4. The feedback capacitor goes from the middle node to the op amp output.
5. The shunt capacitor goes from the non-inverting input node to `Vref`.

Stage 1 values:

```text
R1 = 10k
R2 = 10k
Cfeedback = 1.276n
Cshunt = 1.089n
```

Stage 2 values:

```text
R1 = 10k
R2 = 10k
Cfeedback = 3.081n
Cshunt = 451.2p
```

Name the standalone filter input `fin` and final output `fout`.

### 2.3 Filter `.op`

Use an input source:

```spice
VTEST fin 0 DC 2.5 AC 1
.op
```

Run it. The filter internal nodes and `fout` should be close to 2.5 V. Take:

`screenshots/filter_op.png`

### 2.4 Filter AC response

Use:

```spice
.ac dec 200 0.1 100Meg
```

Plot:

```text
dB(V(fout)/V(fin))
```

Put the cursor at 10 kHz. It should read around `-0.38 dB`, which is below the 0.5 dB maximum attenuation.

For noise bandwidth, use LTspice's waveform measurement on the filter transfer function. The target is about `13.85 kHz`. If your LTspice version does not show "Power Bandwidth" cleanly, include the notebook ENBW calculation and show the AC cursor at 10 kHz.

Take:

`screenshots/filter_ac.png`

## 3. Top-level circuit

Make a full schematic:

1. Wheatstone bridge model.
2. Instrumentation amplifier from Phase 1.
3. The two-stage lowpass filter.
4. A text label for the ADC: `ADS8326, 16 bit, fs = 100 kS/s, Vref = 5 V`.

The ADC itself does not need to be electrically simulated in LTspice. The quantization is done in Python.

Run `.op`. Add DC labels on all important nodes:

```text
bridge outputs, first-stage op amp outputs, amp_out/filter input, filter internal nodes, filter output, Vref
```

Also show current through the positive supply pins or through the supply sources. Take:

`screenshots/top_level_op_power.png`

## 4. Top-level AC response

Use the differential source as the input and set it to `AC 1`.

```spice
.ac dec 200 0.1 100Meg
```

Plot:

```text
dB(V(fout)/V(srcp,srcm))
```

The low-frequency gain should be close to 40 dB. At 10 kHz it should be the instrumentation amplifier gain minus the filter attenuation, about `39.6 dB`.

Take:

`screenshots/top_level_ac.png`

## 5. Top-level noise response

Use:

```spice
.noise V(fout) Vdiff dec 100 0.1 100Meg
```

Again, `Vdiff` must be `AC 1`.

In the waveform viewer:

1. Plot `V(inoise)` and put the cursor at 10 kHz.
2. Plot `V(onoise)` or read the error log to get the total integrated output noise.
3. The expected output integrated noise is about 0.11 mVrms for the ideal filter calculation.

Take:

`screenshots/top_level_noise.png`

## 6. Time-domain noise and ADC simulation

Run the notebook once first. It creates:

`input_noise_phase2.csv`

Copy this CSV to the same folder as your transient LTspice schematic.

You need two identical filter copies in the transient testbench:

1. Noise path: PWL noise source plus a 2.5 V shift, then the filter.
2. Signal path: clean sine source, then the same filter.

Noise source:

```spice
VNOISE nraw 0 PWL file=input_noise_phase2.csv
```

Shift it up by 2.5 V before the filter. The simple way is to put a 2.5 V voltage source in series so the filter input equals:

```text
2.5 V + VNOISE
```

Clean signal source:

```spice
VSIG sig_in 0 SINE(2.5 1 1k)
```

After each filter output, shift the waveform down by 2.5 V before exporting, because `.wave` expects roughly +/-1 V:

```text
vn_wav = filtered_noise_output - 2.5
vsig_wav = filtered_signal_output - 2.5
```

A behavioral source is the easiest way:

```spice
BNOISEWAV vn_wav 0 V=V(vn_fout)-2.5
BSIGWAV vsig_wav 0 V=V(vsig_fout)-2.5
```

Run:

```spice
.tran 0 100m 0 0.5u
.wave sampled_noise_phase2.wav 32 100e3 V(vn_wav) V(vsig_wav)
```

Move `sampled_noise_phase2.wav` into `Phase2_Submission/` and rerun the notebook. The notebook will import the LTspice WAV and calculate the ADC SNR. If the WAV is missing, it uses the Python ideal-filter fallback.

Take:

`screenshots/transient_wave_export.png`

## 7. Final screenshot checklist

Before final submission, the notebook should contain these screenshots:

| filename | rubric item |
| --- | --- |
| `phase1_amp_op.png` | 1.1 amplifier schematic |
| `phase1_unfiltered_noise.png` | 1.3 unfiltered noise simulation |
| `filter_op.png` | 2.2 filter schematic and DC simulation |
| `filter_ac.png` | 2.4 filter AC simulation and ENBW |
| `top_level_op_power.png` | 3.1 complete schematic, DC operating point, power |
| `top_level_ac.png` | 3.4 full circuit AC simulation |
| `top_level_noise.png` | 3.5 input-referred/output noise |
| `transient_wave_export.png` | 3.6 time-domain LTspice export evidence |

Then rerun `EE533_Project_Phase2.ipynb` from top to bottom and submit the executed notebook.
