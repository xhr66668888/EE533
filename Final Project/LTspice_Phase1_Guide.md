# Phase 1 LTspice 操作说明

这份说明是给 `Project_Phase1.ipynb` 里 LTspice 部分配套用的。按下面步骤做完以后，把截图插到 notebook 对应小节，并把测到的数值替换进去即可。

## 0. 需要提交/保存的文件

建议在 `Final Project` 下面新建一个文件夹：

```text
ltspice_phase1/
```

最后至少保存这些文件：

```text
ltspice_phase1/phase1_inamp.asc
ltspice_phase1/phase1_op_schematic.png
ltspice_phase1/phase1_diff_ac.png
ltspice_phase1/phase1_cm_ac.png
ltspice_phase1/phase1_noise_density.png
ltspice_phase1/phase1_noise_error_log.png
```

真正要交的是 notebook。`.asc` 文件也建议一起留着，万一老师要看电路。

## 1. 电路参数

在 schematic 里先放一个 SPICE directive，写这些参数：

```spice
.param Rth=500
.param RF=4.99k
.param RG=200
.param R1=10k
.param R2=19.6k
.param eps=0
```

设计值如下：

| 名称 | 数值 | 说明 |
| --- | ---: | --- |
| `VDD` | `5 V` | 单电源 |
| `Vcm` | `2.5 V` | bridge common-mode / mid-supply |
| `Rth` | `500 ohm` | bridge 每一端的 Thevenin 电阻 |
| `RF` | `4.99k` | `Rfp`, `Rfm` |
| `RG` | `200` | 第一阶段 gain resistor |
| `R1` | `10k` | 第二阶段 input resistors |
| `R2` | `19.6k` | 第二阶段 feedback/reference resistors |
| `eps` | `0` 或 `0.001` | 只有 common-mode mismatch 仿真设成 `0.001` |

对应增益：

```text
G1 = 1 + 2*4.99k/200 = 50.9 V/V
G2 = 19.6k/10k = 1.96 V/V
Gtot = 99.764 V/V = 39.99 dB
```

## 2. 运放型号

最终噪声仿真用 `ADA4528` / `ADA4528-2` 模型。

在 LTspice 里按 `F2`，搜索：

```text
ADA4528
```

如果能找到 `ADA4528-2`，直接放 4 个运放实例。虽然 BOM 里是 2 个 dual op amp 封装，但是 schematic 里可以画成 4 个单运放实例：`U1`, `U2`, `U3`, `U4`。

如果找不到 `ADA4528-2`：

1. 去 Analog Devices 的 ADA4528-2 页面下载 LTspice/SPICE model。
2. 在 LTspice 里 `File -> Open` 打开下载的 `.cir` 或 `.lib`。
3. 对 subcircuit 名字右键，选择 `Create Symbol`。
4. 回到 schematic 里用新生成的 symbol。
5. 在 schematic 里加一行 `.include`，路径指向下载的模型文件。

不要用 `UniversalOpamp2` 做最终 noise 截图，因为它的噪声不是 ADA4528-2 的真实模型。可以用它临时检查连接是否正确。

## 3. 画输入 Thevenin bridge 模型

这里不用把四个桥臂都画出来，而是按题目建议把 strain gage bridge 等效成 Thevenin differential source。这样 `.noise` 也比较干净。

放这些源和电阻：

```text
VDD:  节点 vdd 到 0，DC = 5
VCM:  节点 vcm 到 0，DC = 2.5, AC = 0
Vdiff: 节点 srcp 到 srcm，DC = 0, AC = 1
RcmP: srcp 到 vcm，1G
RcmM: srcm 到 vcm，1G
RsP:  srcp 到 vip，{Rth}
RsM:  srcm 到 vim，{Rth}
```

`RcmP` 和 `RcmM` 只是把 floating differential source 的 DC common-mode 固定在 2.5 V。它们是 1 Gohm，所以不会明显加载输入。

节点名一定要用这些，后面画图表达式会用到：

```text
srcp, srcm, vip, vim, vcm, vdd
```

## 4. 画 instrumentation amplifier

### 第一阶段

`U1`：

```text
U1 + input  -> vip
U1 - input  -> n1
U1 output   -> u1out
U1 V+       -> vdd
U1 V-       -> 0
```

`U2`：

```text
U2 + input  -> vim
U2 - input  -> n2
U2 output   -> u2out
U2 V+       -> vdd
U2 V-       -> 0
```

电阻：

```text
Rfp: u1out 到 n1，{RF}
RG:  n1 到 n2，{RG}
Rfm: u2out 到 n2，{RF}
```

### 第二阶段 difference amplifier

`U3`：

```text
U3 - input  -> n3m
U3 + input  -> n3p
U3 output   -> out
U3 V+       -> vdd
U3 V-       -> 0
```

四个电阻用下面的表达式，这样 nominal 和 worst-case mismatch 可以只改 `eps`：

```text
R1p: u1out 到 n3m，{R1*(1-eps)}
R1m: u2out 到 n3p，{R1*(1+eps)}
R2p: out 到 n3m，{R2*(1+eps)}
R2m: n3p 到 vref，{R2*(1-eps)}
```

注意这个 mismatch 方向就是 final-project 图里的 worst-case 方向。

### Vref buffer

不要用理想 2.5 V 电压源直接接 `vref`。按题目要求，用分压 + buffer：

```text
Rvtop: vdd 到 vref_raw，10k
Rvbot: vref_raw 到 0，10k
```

`U4` 做 voltage follower：

```text
U4 + input  -> vref_raw
U4 - input  -> vref
U4 output   -> vref
U4 V+       -> vdd
U4 V-       -> 0
```

## 5. `.op` operating point

把 schematic 里只保留这个 simulation directive：

```spice
.op
```

同时确认：

```text
VCM: DC 2.5, AC 0
Vdiff: DC 0, AC 0
eps = 0
```

运行以后，在 schematic 上对这些节点放 `.op Data Label`：

```text
vdd
vcm
srcp
srcm
vip
vim
n1
n2
u1out
u2out
vref_raw
vref
n3m
n3p
out
```

期望值基本都是：

```text
vdd = 5.000 V
vcm = 2.500 V
srcp = srcm = 2.500 V
vip = vim = 2.500 V
n1 = n2 = 2.500 V
u1out = u2out = 2.500 V
vref_raw = vref = 2.500 V
n3m = n3p = 2.500 V
out = 2.500 V
```

需要截图：

```text
phase1_op_schematic.png
```

截图必须包含：

```text
完整电路
所有 resistor value
运放型号 ADA4528
5 V supply
Vref divider + buffer
所有上面列出的 DC node voltage labels
```

还要在 `View -> SPICE Error Log` 里记录 `I(VDD)`。LTspice 的电源电流符号通常是负的，电源实际输出电流用：

```text
Isupply = -I(VDD)
Ptotal = 5V * Isupply
```

我的手算估计是：

```text
Isupply ≈ 10.85 mA
Ptotal ≈ 54.25 mW
```

实际值以你的 LTspice 模型为准。

## 6. Differential AC simulation

把 `.op` 注释掉，放这个：

```spice
.ac dec 200 1 10Meg
```

设置：

```text
VCM:   DC 2.5, AC 0
Vdiff: DC 0, AC 1
eps = 0
```

运行以后，在 waveform 窗口 `Add Trace` 输入：

```text
dB(V(out)/V(srcp,srcm))
```

需要用 cursor 记录：

```text
low-frequency gain, 建议在 10 Hz 或 100 Hz 读
gain at 10 kHz
```

期望值：

```text
low-frequency gain ≈ 39.99 dB
gain at 10 kHz ≈ 39.96 dB
```

需要截图：

```text
phase1_diff_ac.png
```

截图要求：

```text
图上有 trace 名称 dB(V(out)/V(srcp,srcm))
x-axis 能看到 1 Hz 到 10 MHz
cursor 放在 10 kHz，能看到 gain 数值
```

## 7. Common-mode AC simulation with mismatch

这一步要测共模响应，所以输入要改成 common-mode AC。

仍然用：

```spice
.ac dec 200 1 10Meg
```

设置：

```text
VCM:   DC 2.5, AC 1
Vdiff: DC 0, AC 0
eps = 0.001
```

也就是把第二阶段电阻设成 worst-case 0.1% mismatch。

运行以后，在 waveform 窗口 `Add Trace` 输入：

```text
dB(V(out)/V(vcm))
```

需要记录：

```text
common-mode gain at 10 Hz 或 100 Hz
common-mode gain at 10 kHz
CMRR = differential gain - common-mode gain
```

期望 low-frequency 结果：

```text
common-mode gain ≈ -51.5 dB
CMRR ≈ 39.99 - (-51.5) = 91.5 dB
```

需要截图：

```text
phase1_cm_ac.png
```

截图要求：

```text
图上有 trace 名称 dB(V(out)/V(vcm))
cursor 放在 10 Hz 或 100 Hz，显示 common-mode gain
最好再放一个 cursor 在 10 kHz
```

## 8. Noise simulation

噪声仿真用 nominal resistor，不要用 mismatch：

```text
eps = 0
```

设置输入：

```text
VCM:   DC 2.5, AC 0
Vdiff: DC 0, AC 1
```

把 `.ac` 注释掉，放：

```spice
.noise V(out) Vdiff dec 100 0.1 10k
```

运行以后，waveform 里一般会有 `onoise_spectrum` 和 `inoise_spectrum`。

要看 input-referred noise density，plot：

```text
inoise_spectrum
```

如果没有自动显示，`Add Trace` 手动输入：

```text
inoise_spectrum
```

需要记录：

```text
input-referred noise density at 10 kHz
total integrated input-referred noise from 0.1 Hz to 10 kHz
```

10 kHz 的 density 用 waveform cursor 读：

```text
inoise_spectrum at 10 kHz
```

期望值：

```text
inoise_spectrum(10 kHz) ≈ 9 nV/sqrt(Hz)
```

integrated noise 在 `View -> SPICE Error Log` 里看。LTspice 会写类似：

```text
Total output noise: ...
Total input noise: ...
```

记录 `Total input noise`。

期望值：

```text
Total input noise ≈ 0.9 uVrms
```

需要截图两个：

```text
phase1_noise_density.png
phase1_noise_error_log.png
```

截图要求：

```text
phase1_noise_density.png:
    plot inoise_spectrum
    cursor 放在 10 kHz
    能看清 y 值，单位是 V/sqrt(Hz)

phase1_noise_error_log.png:
    Error Log 里 Total input noise 那几行
```

## 9. 可选 transient 检查

这个不是 rubric 必需项，但是可以用来检查输出 swing。

把 `Vdiff` 改成：

```text
SINE(0 10m 1k) AC 1
```

放：

```spice
.tran 5m
```

plot：

```text
V(out)
V(srcp,srcm)
```

期望：

```text
V(srcp,srcm) = 20 mVpp
V(out) ≈ 1.50 V to 3.50 V
```

这个图不一定要交，除非你想多放一个验证图。

## 10. 最后填回 notebook 的数值

跑完以后，把 notebook 里这些值用你的 LTspice 实测值替换/补充：

```text
.op:
    V(vip), V(vim), V(u1out), V(u2out), V(vref), V(out)
    I(VDD)
    Ptotal

Differential AC:
    low-frequency gain
    gain at 10 kHz

Common-mode AC:
    common-mode gain with eps=0.001
    CMRR = differential gain - common-mode gain

Noise:
    inoise_spectrum at 10 kHz
    Total input noise from 0.1 Hz to 10 kHz
```

只要这些图和数值都在 notebook 里，rubric 的 3, 5, 6, 7 项就都有对应证据。
