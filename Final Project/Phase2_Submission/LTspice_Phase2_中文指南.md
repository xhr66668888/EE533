# Phase 2 LTspice 中文操作指南

这个文件是给你跑 LTspice、补截图、最后重新运行 notebook 用的。最后 Canvas 主提交物是：

```text
Phase2_Submission/EE533_Project_Phase2.ipynb
```

如果 Canvas 允许多个附件，可以同时交 `.asc` 文件和截图压缩包。如果 Canvas 只允许一个文件，就把截图放进 `screenshots/` 文件夹后重新运行 notebook，让截图嵌入 notebook 输出里。

## 0. 先看本次设计数值

Phase 2 notebook 已经把滤波器和 ADC 算完。关键值如下：

| 项目 | 数值 |
| --- | ---: |
| 仪表放大器增益 | 99.764 V/V |
| Phase 1 输入参考白噪声密度 | 9.112 nV/sqrt(Hz) |
| 进入滤波器前的输出噪声密度 | 0.909 uV/sqrt(Hz) |
| 75 dB SNR 允许的最大输出 rms 噪声 | 125.7 uVrms |
| 选用滤波器 | 四阶 Butterworth 低通 |
| 设计截止频率 | 13.5 kHz |
| 10 kHz 衰减 | 约 0.377 dB |
| 等效噪声带宽 ENBW | 约 13.85 kHz |
| ADC | ADS8326，16 bit，实际用 100 kS/s，芯片最高 250 kS/s |

滤波器用两个 unity-gain Sallen-Key 二阶级联。低 Q 级放前面，高 Q 级放后面。

| 级数 | Q | R1 | R2 | 从第一个 RC 节点接到 op amp 输出的反馈电容 | 从 op amp 输入节点接到 Vref 的电容 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.541 | 10 kOhm | 10 kOhm | 1.276 nF | 1.089 nF |
| 2 | 1.307 | 10 kOhm | 10 kOhm | 3.081 nF | 451.2 pF |

在 LTspice 里可以直接输入这些值，例如 `1.276n`、`451.2p`。

## 1. 先解释 Phase 1 的 `Vdiff AC 1`

这个是我前面提到的重点。

在 LTspice 做 `.noise` 分析时，命令通常写成：

```spice
.noise V(vout) Vdiff dec 100 0.1 100Meg
```

这里第二个参数 `Vdiff` 不是随便写的，它必须是电路里真实存在的输入电压源名字。LTspice 会把输出噪声除以这个输入源的 AC 增益，从而得到 input-referred noise，也就是 `V(inoise)`。

所以 `Vdiff` 这个电压源必须设置小信号 AC 幅度：

```text
AC 1
```

如果它是 `AC 0`，LTspice 对输入参考噪声的计算会不对，或者会出现和手算白噪声预算明显不一致的结果。你之前的 Phase 1 截图里 10 kHz 白噪声约是 9 nV/sqrt(Hz)，但 error log 积分噪声显示约 9.48 uVrms，这个数和白噪声预算不一致，所以最终提交前建议重新跑一次 `.noise`。

我已经把当前这个文件里的 `Vdiff` 改成了 `AC 1`：

```text
ltSpice/Draft3.asc
```

并且我把默认 AC 设置改成了差分/噪声仿真模式：

```text
Vdiff: AC 1
VCM:   AC 0
```

如果你要跑 common-mode AC 仿真，需要临时切换成：

```text
Vdiff: AC 0
VCM:   AC 1
```

但是我不能在本机打开 LTspice GUI，所以你还需要在 LTspice 里确认一下：

1. 打开 `ltSpice/Draft3.asc`。
2. 右键点名为 `Vdiff` 的电压源。
3. 确认 Small signal AC amplitude 是 `1`。
4. 重新运行 `.noise`。
5. 截图并保存为 `screenshots/phase1_unfiltered_noise.png`。

## 2. Phase 1 放大器需要带过来的截图

使用 Phase 1 的 instrumentation amplifier schematic。

截图前检查：

1. `Vref` 是由 10 kOhm / 10 kOhm 分压再经过 buffer 得到，不是理想电压源直接给。
2. 平衡状态下 bridge 输出、共模节点、放大器输出都应该接近 2.5 V。
3. `.noise` 里用的差分输入源 `Vdiff` 必须是 `AC 1`。

运行 `.op`，截图命名为：

```text
screenshots/phase1_amp_op.png
```

这张图要能看到：放大器 schematic、元件值、op amp 型号、DC node voltage label。

运行未加滤波器的 noise：

```spice
.noise V(amp_out) Vdiff dec 100 0.01 100Meg
```

在 waveform viewer 里画：

```text
V(onoise)
V(inoise)
```

然后打开 error log 看 integrated rms noise。截图命名为：

```text
screenshots/phase1_unfiltered_noise.png
```

## 3. 单独搭滤波器

建议先单独搭 filter，不要一开始就接完整系统，这样最容易 debug。

### 3.1 生成真实 2.5 V reference

不要用理想 2.5 V 电压源直接当 reference。按要求做：

1. 一个 5 V supply。
2. 两个 10 kOhm 电阻从 5 V 分压到地。
3. 分压中点接一个 op amp voltage follower。
4. buffer 输出节点命名为 `Vref`。

filter op amp 用 `ADA4661-2`。如果你的 LTspice 里暂时找不到，可以先用 `UniversalOpamp2` debug，但最终截图最好换成真实 op amp model。

### 3.2 每一级 Sallen-Key 接法

每一级都这样接：

1. 输入节点经过 `R1=10k` 到中间节点。
2. 中间节点经过 `R2=10k` 到 op amp 的 non-inverting 输入。
3. op amp 做 voltage follower：输出接回 inverting 输入。
4. 反馈电容从中间节点接到 op amp 输出。
5. shunt 电容从 non-inverting 输入节点接到 `Vref`。

第一级：

```text
R1 = 10k
R2 = 10k
Cfeedback = 1.276n
Cshunt = 1.089n
```

第二级：

```text
R1 = 10k
R2 = 10k
Cfeedback = 3.081n
Cshunt = 451.2p
```

把单独 filter 输入节点命名为 `fin`，最终输出命名为 `fout`。

### 3.3 Filter `.op`

输入源设置：

```spice
VTEST fin 0 DC 2.5 AC 1
.op
```

运行后，filter 内部节点和 `fout` 都应该接近 2.5 V。截图命名为：

```text
screenshots/filter_op.png
```

### 3.4 Filter AC response

指令：

```spice
.ac dec 200 0.1 100Meg
```

画：

```text
dB(V(fout)/V(fin))
```

把 cursor 放到 10 kHz，应该大约是：

```text
-0.38 dB
```

这个小于题目要求的最大 0.5 dB attenuation。

关于 noise bandwidth，LTspice waveform viewer 里如果能用 Power Bandwidth 就量一下，目标大约是：

```text
13.85 kHz
```

如果你的 LTspice 版本不好找 Power Bandwidth，就在截图里至少显示 10 kHz cursor，然后 notebook 里已经有 Python ENBW 计算。

截图命名为：

```text
screenshots/filter_ac.png
```

## 4. 完整 top-level circuit

完整 schematic 要包括：

1. Wheatstone bridge model。
2. Phase 1 instrumentation amplifier。
3. 两级 lowpass filter。
4. ADC 文字标注：`ADS8326, 16 bit, fs = 100 kS/s, Vref = 5 V`。

ADC 不需要在 LTspice 里真的搭电路，ADC quantization 在 Python 里模拟。

运行 `.op` 后，在重要节点放 DC labels：

```text
bridge 输出节点
第一级 op amp 输出
amp_out / filter input
filter 内部节点
filter output
Vref
```

同时标出正电源电流或 supply source current，用来算 power dissipation。

截图命名为：

```text
screenshots/top_level_op_power.png
```

## 5. Top-level AC response

用差分输入源作为输入，并设置：

```text
AC 1
```

指令：

```spice
.ac dec 200 0.1 100Meg
```

画：

```text
dB(V(fout)/V(srcp,srcm))
```

低频增益应该接近 40 dB。10 kHz 处应该约为：

```text
39.6 dB
```

也就是 instrumentation amplifier 的约 40 dB 减去 filter 的约 0.38 dB。

截图命名为：

```text
screenshots/top_level_ac.png
```

## 6. Top-level noise response

指令：

```spice
.noise V(fout) Vdiff dec 100 0.1 100Meg
```

再次注意，`Vdiff` 必须是 `AC 1`。

在 waveform viewer 里：

1. 画 `V(inoise)`，cursor 放在 10 kHz，报告 input-referred noise density。
2. 画 `V(onoise)` 或者看 error log，报告 total integrated output noise。
3. 理想滤波器计算预期输出 integrated noise 约为 0.11 mVrms。

截图命名为：

```text
screenshots/top_level_noise.png
```

## 7. Time-domain noise 和 ADC simulation

先运行一次 notebook，它会生成：

```text
input_noise_phase2.csv
```

把这个 CSV 放到 transient LTspice schematic 同一个文件夹里。

transient testbench 里需要两个完全一样的 filter copy：

1. noise path：PWL noise source 加 2.5 V 偏置，再进入 filter。
2. signal path：干净 sine source，再进入一样的 filter。

noise source：

```spice
VNOISE nraw 0 PWL file=input_noise_phase2.csv
```

进入 filter 前要上移 2.5 V，让 filter input 等于：

```text
2.5 V + VNOISE
```

干净信号源：

```spice
VSIG sig_in 0 SINE(2.5 1 1k)
```

导出 `.wave` 之前，要把两个 filter output 都减掉 2.5 V，因为 `.wave` 适合导出大约 +/-1 V 的波形：

```text
vn_wav = filtered_noise_output - 2.5
vsig_wav = filtered_signal_output - 2.5
```

最简单是用 behavioral source：

```spice
BNOISEWAV vn_wav 0 V=V(vn_fout)-2.5
BSIGWAV vsig_wav 0 V=V(vsig_fout)-2.5
```

运行：

```spice
.tran 0 100m 0 0.5u
.wave sampled_noise_phase2.wav 32 100e3 V(vn_wav) V(vsig_wav)
```

把生成的 `sampled_noise_phase2.wav` 放进：

```text
Phase2_Submission/
```

然后重新运行 notebook。notebook 会读取这个 LTspice WAV，再计算 ADC 后 SNR。如果 WAV 不存在，notebook 会使用 Python ideal-filter fallback。

截图命名为：

```text
screenshots/transient_wave_export.png
```

## 8. 最终截图清单

| 文件名 | 对应 rubric |
| --- | --- |
| `phase1_amp_op.png` | 1.1 amplifier schematic |
| `phase1_unfiltered_noise.png` | 1.3 unfiltered noise simulation |
| `filter_op.png` | 2.2 filter schematic and DC simulation |
| `filter_ac.png` | 2.4 filter AC simulation and ENBW |
| `top_level_op_power.png` | 3.1 complete schematic, DC operating point, power |
| `top_level_ac.png` | 3.4 full circuit AC simulation |
| `top_level_noise.png` | 3.5 input-referred/output noise |
| `transient_wave_export.png` | 3.6 time-domain LTspice export evidence |

全部截图放好以后，重新运行 `EE533_Project_Phase2.ipynb`。确认 notebook 里没有 `Missing screenshot`，并且最后 ADC SNR 大于 75 dB。
