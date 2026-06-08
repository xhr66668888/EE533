# Phase 1 修改与截图中文教程

这个文件是专门给 Phase 1 查分、改 LTspice、重新截图用的。核心结论先说：

1. 你现在的 Phase 1 思路大体是对的，Python 手算噪声、AC、CMRR 都写得比较完整。
2. 最大扣分风险是 LTspice noise 那一项：当前 notebook 写了 integrated input-referred noise 是 `9.4965 uVrms`，这会让 Phase 1 SNR 只有约 `57.4 dB`，和题目要求 `77 dB` 冲突。
3. 我已经把 `ltSpice/Draft3.asc` 默认改成差分/噪声模式：

```text
Vdiff: AC 1
VCM:   AC 0
```

你需要在 LTspice 里重新跑 noise，并重新截图。仅修改 `.asc` 文本不够，必须重新 run simulation。

## 1. 按 Phase 1 rubric 给你现在版本打分

这个是按你现在的 `Project_Phase1.ipynb` 和已有截图估计的，不是老师最终分数。

| Rubric item | 分值 | 现在估计 | 原因 |
| --- | ---: | ---: | --- |
| 1. Target input-referred noise calculation | 5 | 5 | 目标推导正确：`0.999 uVrms`、`9.988 nV/sqrt(Hz)` |
| 2. Noise analysis of each noise source | 10 | 8 | 主要噪声源都有表格和公式，但低频噪声/模型噪声解释还不够闭合 |
| 3. Schematic and DC operating point voltage | 5 | 3.5 | 有 DC operating point 截图，但 notebook 自己指出 transient/Vref setup 有问题 |
| 4. Table of total cost | 5 | 4.5 | 有 BOM 和总价；如果补上 Digikey 链接会更稳 |
| 5. AC differential frequency response | 5 | 5 | 有差分 AC testbench 和 10 kHz cursor |
| 6. AC common-mode frequency response with mismatch | 10 | 9 | 有 mismatch、CMRR 计算和截图；需要确保共模仿真时 AC source 设置正确 |
| 7. Input-referred noise density and integrated noise | 10 | 4 | 10 kHz density 有，但 integrated noise 写成 `9.4965 uVrms`，明显不满足 77 dB |

当前粗略总分：

```text
39 / 50 左右
```

如果你把 Phase 1 的 LTspice noise 重新跑正确，并让 integrated input-referred noise 回到大约 `0.9 to 1.0 uVrms`，同时更新 notebook 文字，Phase 1 有机会到：

```text
47 to 49 / 50
```

## 2. Recommended Phase 1 approach vs 你自己的设计

老师给的 recommended approach 是：

```text
G1 = 100
G2 = 1
```

也就是几乎所有 gain 都放在 instrumentation amplifier 第一 stage，difference amplifier 只做 unity gain。

你现在的设计是：

```text
G1 = 50.9
G2 = 1.96
Gtotal = 99.764
```

### 2.1 你自己的设计优点

1. 总增益正确，`20 mVpp` 输入能得到约 `1.995 Vpp` 输出。
2. 第一 stage 输出摆幅较小，更不容易接近 op amp output swing 限制。
3. CMRR 计算和仿真都刚好超过 `90 dB`。
4. Python 噪声预算是完整的，计算结果 `9.112 nV/sqrt(Hz)` 低于目标。

### 2.2 recommended approach 优点

如果用：

```text
Rfp = Rfm = 4.99 kOhm
RG  = 100 Ohm
R1  = R2 = 10 kOhm
```

则：

```text
G1 = 1 + (4.99k + 4.99k)/100 = 100.8
G2 = 1
```

这个版本的好处是：

1. second-stage gain 是 1，difference amplifier 引入的噪声更小。
2. CMRR 更高。用 `0.1%` mismatch：

```text
CMRR = G1 * (G2 + 1) / (4 epsilon)
     = 100.8 * 2 / 0.004
     = 50400 V/V
     = 94.0 dB
```

比你现在的 `91.5 dB` 更有余量。

3. 和老师 recommended design approach 更一致，评分时更容易解释。

### 2.3 我建议用哪个

如果只是想最少改动：保留你自己的 `G1=50.9, G2=1.96`，只修正 LTspice noise 和 Vref，重新截图即可。

如果想冲满分：建议改成 recommended approach：

```text
RG = 100 Ohm
R1 = 10 kOhm
R2 = 10 kOhm
Rfp = Rfm = 4.99 kOhm
```

这个方案更贴合老师提示，CMRR 更稳，second-stage 噪声也更小。缺点是第一 stage 输出摆幅变大，但 full-scale 输入时大约是 2.0 V 到 3.0 V，仍然在 5 V single-supply 里合理。

## 3. 最少改动版：只修你当前 Phase 1

这个版本最快，也最不容易把已有 notebook 搞乱。

### Step 1: 打开 LTspice 文件

打开：

```text
ltSpice/Draft3.asc
```

### Step 2: 差分/noise 模式设置

用于 differential AC 和 noise simulation 时，设置：

```text
Vdiff: AC amplitude = 1
VCM:   AC amplitude = 0
```

我已经在 `.asc` 里改过默认值，但你在 LTspice GUI 里还是检查一下：

1. 右键 `Vdiff` 电压源。
2. Small signal AC analysis amplitude 填 `1`。
3. 右键 `VCM` 电压源。
4. Small signal AC analysis amplitude 填 `0`。

### Step 3: 检查 Vref

Phase 1 要求 `Vref` 不能直接用 ideal 2.5 V source。正确做法：

1. 5 V 到地接两个 10 kOhm 电阻分压。
2. 中点是 2.5 V。
3. 中点接 op amp voltage follower。
4. buffer 输出命名为 `Vref`。
5. difference amplifier 的 reference resistor 接这个 buffered `Vref`。

截图里必须能看出这个 reference buffer。

### Step 4: 跑 `.op`

激活：

```spice
.op
```

先把 `.ac`、`.noise`、`.tran` 都注释掉，只保留 `.op`。

运行后，在这些节点放 `.op data label`：

```text
srcp, srcm
Vip, Vin
U1 output
U2 output
Vref
vout
5 V supply current
```

保存截图：

```text
phase1_op_schematic_corrected.png
```

### Step 5: 跑 differential AC

设置：

```text
Vdiff: AC 1
VCM:   AC 0
```

激活：

```spice
.ac dec 200 0.1 100Meg
```

画：

```text
dB(V(vout)/V(srcp,srcm))
```

把 cursor 放到 `10 kHz`。你当前设计预期大约：

```text
39.3 to 40.0 dB
```

保存截图：

```text
phase1_diff_ac_corrected.png
```

### Step 6: 跑 common-mode AC with mismatch

设置：

```text
Vdiff: AC 0
VCM:   AC 1
```

保留 mismatch：

```spice
.param eps=0.001
R4 = R1*(1-eps)
R5 = R2*(1+eps)
R6 = R1*(1+eps)
R7 = R2*(1-eps)
```

激活：

```spice
.ac dec 200 0.1 100Meg
```

画：

```text
dB(V(vout)/V(VCM))
```

或如果你的 common-mode 输入节点叫 `vcm`：

```text
dB(V(vout)/V(vcm))
```

把 cursor 放到 `10 kHz`。你现在设计预期：

```text
Acm around -51 dB
CMRR around 90 to 91 dB
```

保存截图：

```text
phase1_cm_ac_corrected.png
```

### Step 7: 跑 noise

设置：

```text
Vdiff: AC 1
VCM:   AC 0
```

激活：

```spice
.noise V(vout) Vdiff dec 100 0.1 10k
```

在 waveform viewer 里画：

```text
V(inoise)
```

把 cursor 放到 `10 kHz`，目标值应该接近：

```text
9 nV/sqrt(Hz)
```

然后看 integrated noise。推荐两种方式：

1. 用 LTspice error log 里的 total input noise。
2. 或者在 waveform viewer 里对 `V(inoise)` 做 total noise/integrated noise 显示。

目标是：

```text
Vn,in from 0.1 Hz to 10 kHz <= 0.999 uVrms
```

保存两张截图：

```text
phase1_noise_density_corrected.png
phase1_noise_error_log_corrected.png
```

### Step 8: 更新 notebook 文字

如果 rerun 后 integrated noise 变成约 `0.9 uVrms`，把原 notebook 里这段删掉或改掉：

```text
The integrated result is 9.4965 uVrms...
SNR = 57.4 dB...
op amp has to be selected...
```

改成：

```text
The corrected LTspice noise simulation gives an input-referred noise density of about 9 nV/sqrt(Hz) at 10 kHz and an integrated input-referred noise below 1 uVrms from 0.1 Hz to 10 kHz. This meets the 77 dB Phase 1 SNR target and is consistent with the hand noise budget.
```

## 4. 冲满分版：改成 recommended gain split

如果你愿意多改一点，按下面改。

### Step 1: 改电阻参数

把 LTspice 里的参数改成：

```spice
.param R1=10k
.param R2=10k
.param eps=0.001
.param Rth=500
```

把 gain resistor 改成：

```text
Rfp = 4.99k
Rfm = 4.99k
RG  = 100
```

### Step 2: notebook 里同步改参数

在 `Project_Phase1.ipynb` 里改：

```python
Rfp = Rfm = 4.99e3
RG = 100.0
R1 = 10e3
R2 = 10e3
```

重新运行 notebook。你应该看到：

```text
G1 ≈ 100.8
G2 = 1
Gtot ≈ 100.8
Output p-p from 20 mVpp input ≈ 2.016 Vpp
CMRR ≈ 94 dB
```

`2.016 Vpp` 比 2 V 多 0.8%，通常可以接受。如果想更接近 2.000 Vpp，可以把 `RG` 微调成：

```text
RG = 101 Ohm
```

这样：

```text
G1 = 1 + 9.98k/101 ≈ 99.81
Gout ≈ 1.996 Vpp
```

### Step 3: 重新跑所有截图

冲满分版要重新跑：

```text
phase1_op_schematic_corrected.png
phase1_diff_ac_corrected.png
phase1_cm_ac_corrected.png
phase1_noise_density_corrected.png
phase1_noise_error_log_corrected.png
```

截图方法和最少改动版一样。

## 5. 最终 Phase 1 截图清单

Phase 1 按 rubric 至少需要这些：

| 截图 | 内容 |
| --- | --- |
| `phase1_op_schematic_corrected.png` | 完整 schematic、元件值、DC node voltages、supply current |
| `phase1_diff_ac_corrected.png` | differential AC response，10 kHz cursor |
| `phase1_cm_ac_corrected.png` | common-mode AC response with mismatch，10 kHz cursor |
| `phase1_noise_density_corrected.png` | input-referred noise density，10 kHz cursor |
| `phase1_noise_error_log_corrected.png` | integrated input-referred noise from 0.1 Hz to 10 kHz |

可选但有帮助：

| 截图 | 内容 |
| --- | --- |
| `phase1_transient_input_corrected.png` | `V(srcp,srcm)` 接近 20 mVpp |
| `phase1_transient_output_corrected.png` | `V(vout)` 接近 2 Vpp |

## 6. 最终建议

如果时间紧，做最少改动版：修 `Vdiff/VCM`、修 `Vref`、重跑 noise，把 notebook 里失败的 noise 文字改掉。

如果想让 Phase 1 更像老师推荐答案，做冲满分版：把 gain 几乎全部放到第一 stage，也就是 `RG≈100 Ohm`、`R1=R2=10k`。这个版本 CMRR 和 second-stage noise 余量更好。
