# Assignment 4 LTspice 中文手把手教程

这个文件是给你操作 LTspice 用的，不一定要提交。真正要提交的主要还是 `Assignment4.ipynb`，然后把 LTspice 截图放进 notebook 里。

这次 LTspice 需要做两套图：

1. Part 2c：单级 non-inverting amplifier，必须做。
2. Bonus：两级 non-inverting amplifier，想拿 bonus 就做。

我已经给你准备了两个 `.cir` 文件：

- `sensor_amp_single.cir`
- `sensor_amp_bonus_two_stage.cir`

`.cir` 可以直接在 LTspice 里跑，用来检查数值。但是作业要求要有 schematic 截图，所以你最好还是按下面步骤手动画 `.asc` schematic，然后截图。

## Part 2c 单级放大器

### 目标

输入是 `Vs = 100mV DC`，输出应该接近 `4V DC`。

低频 AC 增益应该接近：

```text
40 V/V = 32.04 dB
```

1% gain drop 频率大约：

```text
35.6 kHz
```

3 dB bandwidth 大约：

```text
250 kHz
```

### 第一步：新建 schematic

1. 打开 LTspice。
2. 点 `File -> New Schematic`。
3. 保存到 `Assignment4` 文件夹，名字可以叫：

```text
sensor_amp_single.asc
```

### 第二步：放 op amp

1. 按键盘 `F2`，打开元件窗口。
2. 找 `Opamps` 文件夹。
3. 选择 `UniversalOpamp2`。
4. 放到图中间。

如果你找不到 `UniversalOpamp2`，在元件搜索框里直接搜：

```text
UniversalOpamp2
```

### 第三步：放电阻

按键盘 `R` 放电阻。

需要两个电阻：

```text
R1 = 12.5
R2 = 487.5
```

连接方式：

- `R2` 从输出 `out` 接到反馈节点 `fb`
- `R1` 从反馈节点 `fb` 接到地
- op amp 的 `-` 输入接到 `fb`
- op amp 的 `+` 输入接到输入节点 `in`

右键电阻可以改数值。

注意 LTspice 里 `12.5` 就是 `12.5 ohm`，`487.5` 就是 `487.5 ohm`。

### 第四步：放输入电压源 Vs

1. 按 `F2`。
2. 选择 `voltage`。
3. 放一个电压源，从 `in` 接到地。
4. 右键这个 voltage source，把值改成：

```text
DC 100m AC 1
```

这里的意思是：

- `.op` DC operating point 用 `100mV`
- `.ac` 小信号分析用 `AC amplitude = 1`

因为 AC amplitude 是 1，所以你画 `V(out)/V(in)` 的时候，就是直接看闭环增益。

### 第五步：放电源 +5V 和 -5V

再放两个 voltage source：

```text
Vpos = 5
Vneg = -5
```

连接方式：

- `Vpos` 上端节点标成 `vcc`，下端接地
- `Vneg` 上端节点标成 `vee`，下端接地
- op amp 正电源脚接 `vcc`
- op amp 负电源脚接 `vee`

给节点命名的方法：

1. 按 `F4`。
2. 输入节点名字，比如 `vcc`。
3. 点到对应导线上。

同理标这些节点：

```text
in
fb
out
vcc
vee
```

### 第六步：设置 UniversalOpamp2 参数

右键 `UniversalOpamp2` 符号，把参数设置成下面这一整行：

```text
level2 Avol=1Meg GBW=10Meg Slew=10Meg Ilimit=10m Rail=0 Vos=0 En=0 Enk=0 In=0 Ink=0 Rin=500Meg Rout=1
```

参数意思不用全部记住，关键是：

- `Avol=1Meg`：DC open-loop gain 是 `10^6`
- `GBW=10Meg`：unity gain frequency 是 `10MHz`
- `Ilimit=10m`：输出电流限制是 `10mA`
- `Rail=0`：可以到电源轨
- `Rout=1`：LTspice 这个模型需要非零输出电阻参数；这里用 `1 ohm` 近似作业给的 `Rout = 0 ohm`

### 第七步：放 SPICE 指令

按键盘 `S`，放 SPICE directive。

先放这两行：

```text
.op
.ac dec 100 10 100Meg
```

再放这些 `.meas` 指令，方便 LTspice 自动算结果：

```text
.meas op vout_dc FIND V(out)
.meas op vfb_dc FIND V(fb)
.meas op i_feedback PARAM abs(V(out)/500)
.meas ac gain10 FIND mag(V(out)/V(in)) AT=10
.meas ac f_1pct WHEN mag(V(out)/V(in))=39.6 FALL=1
.meas ac f_3db WHEN mag(V(out)/V(in))=gain10/sqrt(2) FALL=1
```

如果运行时报错 `Unknown subcircuit: level2`，再放这一行：

```text
.lib UniversalOpAmp2.lib
```

如果你的 LTspice 版本库文件名字不同，就去 LTspice 的 `lib/sub` 文件夹找 Universal OpAmp 的库文件，用那个真实文件名。

### 第八步：运行仿真

点工具栏上的小人跑步图标，也就是 `Run`。

运行后会弹出波形窗口。

### 第九步：看 DC operating point

作业要求 schematic 上要显示 DC node voltages。

步骤：

1. 先确认 schematic 里有 `.op`。
2. 点 `Run`。
3. 回到 schematic。
4. 在节点导线上右键。
5. 选择 `Place .op Data Label`。

至少给这些节点放 label：

```text
in
fb
out
vcc
vee
```

你应该看到大概：

```text
V(in)  = 100 mV
V(fb)  = 100 mV
V(out) = 4.0 V
V(vcc) = 5.0 V
V(vee) = -5.0 V
```

这张 schematic 截图要提交，因为 Part 2c 明确要求 resistor values 和 DC node voltages。

### 第十步：看 AC gain 和 phase

在波形窗口里：

1. 右键空白处。
2. 选 `Add Trace`。
3. 输入：

```text
dB(V(out)/V(in))
```

这就是 magnitude plot。

再加 phase：

```text
ph(V(out)/V(in))
```

如果 magnitude 和 phase 挤在一起看不清，你可以：

1. 先只画 `dB(V(out)/V(in))` 截一张。
2. 再删掉 magnitude，只画 `ph(V(out)/V(in))` 截一张。

你要在图上能看出：

```text
low-frequency gain ~= 32.04 dB
f_1pct ~= 35.6 kHz
f_3dB ~= 250 kHz
```

### 第十一步：查看 `.meas` 结果

运行后点：

```text
View -> SPICE Error Log
```

里面应该能看到类似：

```text
vout_dc: about 4
vfb_dc: about 0.1
i_feedback: about 0.008
gain10: about 40
f_1pct: about 3.56e4
f_3db: about 2.50e5
```

如果这些数值接近，就说明仿真是对的。

## 需要提交/放进 notebook 的 Part 2c 截图

Part 2c 最少需要两类图：

1. schematic 截图：能看到 `R1=12.5`、`R2=487.5`、`Vs DC 100m AC 1`、`UniversalOpamp2`，还有 `.op` data label。
2. AC simulation 截图：能看到 `dB(V(out)/V(in))` 和 `ph(V(out)/V(in))`。

## Bonus 两级设计

bonus 是把总增益 40 拆成两级：

```text
Gstage = sqrt(40) = 6.3246
```

每一级都是 non-inverting amplifier：

```text
Gain = 1 + R2/R1 = 6.3246
```

所以：

```text
R2/R1 = 5.3246
```

我选的值是每一级：

```text
R1 = 1k
R2 = 5.3246k
```

### Bonus 连接方法

一共用两个 `UniversalOpamp2`。

第一级：

- `+` 输入接 `in`
- `-` 输入接 `fb1`
- 输出叫 `mid`
- `R2A = 5.3246k`：从 `mid` 接 `fb1`
- `R1A = 1k`：从 `fb1` 接地

第二级：

- `+` 输入接 `mid`
- `-` 输入接 `fb2`
- 输出叫 `out`
- `R2B = 5.3246k`：从 `out` 接 `fb2`
- `R1B = 1k`：从 `fb2` 接地

两个 op amp 都接同样的电源：

```text
vcc = +5V
vee = -5V
```

两个 op amp 都用同样参数：

```text
level2 Avol=1Meg GBW=10Meg Slew=10Meg Ilimit=10m Rail=0 Vos=0 En=0 Enk=0 In=0 Ink=0 Rin=500Meg Rout=1
```

输入 source 还是：

```text
DC 100m AC 1
```

### Bonus 仿真指令

放：

```text
.op
.ac dec 100 10 100Meg
.meas op mid_dc FIND V(mid)
.meas op vout_dc FIND V(out)
.meas ac gain10 FIND mag(V(out)/V(in)) AT=10
.meas ac f_1pct WHEN mag(V(out)/V(in))=39.6 FALL=1
.meas ac f_3db WHEN mag(V(out)/V(in))=gain10/sqrt(2) FALL=1
```

如果需要，也放：

```text
.lib UniversalOpAmp2.lib
```

### Bonus 预期结果

DC：

```text
V(in)  ~= 0.100 V
V(mid) ~= 0.632 V
V(out) ~= 4.0 V
```

AC：

```text
low-frequency gain ~= 40 V/V = 32.04 dB
f_1pct ~= 159 kHz
f_3dB ~= 1.02 MHz
```

这个 bandwidth 大于单级的 `250 kHz` 的 2 倍，所以 bonus 条件满足。

## 最容易错的地方

1. 忘记接地：每个 voltage source 都必须有地，R1 下面也必须接地。
2. op amp 电源脚没接：`UniversalOpamp2` 需要 `+5V` 和 `-5V`。
3. AC source 没写 `AC 1`：如果没有 `AC 1`，AC plot 可能是 0。
4. `R1/R2` 接反：non-inverting amplifier 是 `R2` 从 output 到 feedback node，`R1` 从 feedback node 到 ground。
5. 没有 `.op` data label：作业要求 schematic 上显示 DC node voltages。
6. 只跑 `.cir` 不画 schematic：`.cir` 可以验证数值，但作业要 schematic 截图，所以要画 `.asc`。
