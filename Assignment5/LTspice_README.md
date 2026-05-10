# Assignment 5 LTspice steps

这个 README 是给截图用的。`Assignment5.ipynb` 里我只放计算和结论，这里才写 LTspice 怎么搭。

## 先看文件

- `ltspice/diff_amp_ac.cir`: part b 的 quick check，用行为 op amp 估一下 20 dB 和带宽。
- `ltspice/diff_amp_bridge_tran.cir`: part c 的 bridge + difference amp transient quick check。
- `ltspice/inamp_bridge_tran.cir`: part d 的 bridge + instrumentation amp transient quick check。

这些 `.cir` 可以先跑来确认节点名和大概数值，但是正式交的 schematic screenshot 还是建议你在 LTspice 里用 `ADA4661-2` 元件画出来，因为题目指定了这个 op amp。

## 全局元件值

用这些值就行：

```text
VDD = 5 V
VREF divider = 100k / 100k, then op amp buffer
R = 500 ohm for each nominal bridge arm

Difference amp:
R1 = 25k
R2 = 250k
gain = R2/R1 = 10 = 20 dB

Instrumentation amp:
Rfp = 45k
Rfm = 45k
RG = 10k
output diff stage R1 = 25k
output diff stage R2 = 25k
overall gain = (1 + (Rfp+Rfm)/RG)*(R2/R1) = 10
```

## 怎么放 ADA4661-2

1. 打开 LTspice，`File -> New Schematic`。
2. 按 `F2` 放元件，搜索 `ADA4661-2`。
3. 如果搜不到，先 `Tools -> Sync Release` 或更新 LTspice，然后再搜。
4. 每个 op amp 的正电源脚接 `vdd`，负电源脚接 ground。
5. 按 `F4` 放 net label。强烈建议用这些名字：`vdd`, `vref`, `bplus`, `bminus`, `out`, `delta_R`。

## Part b: difference amp AC

目标：证明 low-frequency gain 是 20 dB，并量 3 dB bandwidth。

搭法：

1. 放一个 5 V DC source：正端叫 `vdd`，负端 ground。
2. 做 `VREF`：
   - `100k` 从 `vdd` 到 `vdiv`
   - `100k` 从 `vdiv` 到 ground
   - 一个 ADA4661-2 接成 buffer：`+` 输入接 `vdiv`，输出短回 `-` 输入，输出 label 叫 `vref`
3. 做 difference amp：
   - `vip -> 25k -> op amp + node`
   - `op amp + node -> 250k -> vref`
   - `vim -> 25k -> op amp - node`
   - `op amp - node -> 250k -> out`
4. 输入用两个 source：
   - `Vinp`: `DC 2.5`, small signal AC amplitude `0.5`, phase `0`
   - `Vinm`: `DC 2.5`, small signal AC amplitude `0.5`, phase `180`
   这样差分 AC 输入就是 1 V。
5. 加 spice directive：

```text
.ac dec 200 1 10Meg
```

看图：

1. Run 后，在 plot window 里点 `Plot Settings -> Add Trace`。
2. 输入：

```text
dB(V(out)/V(vip,vim))
```

3. 低频应该大约是 `20 dB`。
4. 3 dB 点就是掉到大约 `17 dB` 的频率。用 cursor 标出来。
5. 截图：AC plot，最好 cursor 1 放低频，cursor 2 放 3 dB 点。

## Part c: bridge + difference amp transient

目标：找最大 `Delta R`，并证明 output 在 `0.5 V` 到 `4.5 V` 之间。

计算结果是 `Delta R_max ~= 38.8 ohm`。如果 LTspice 因为模型误差刚好显示 `0.499 V` 这种边界值，截图时可以用 `38 ohm`，但文字里保留最大值 `38.8 ohm`。

bridge 搭法：

1. 上端接 `vdd`，下端 ground。
2. 左上固定电阻：`vdd -> 500 -> bplus`
3. 右下固定电阻：`bminus -> 500 -> ground`
4. 另外两个是 `R + Delta R`。最简单是直接用 Canvas 给的 bridge model。
5. 如果 Canvas model 没有，打开 `ltspice/diff_amp_bridge_tran.cir` 直接跑；里面用 behavioral current source 做了这两个 variable resistor。
6. `delta_R` source 设成：

```text
SINE(0 38.8 1k)
```

transient directive:

```text
.tran 0 5m 0 1u
```

看图：

1. plot `V(bplus,bminus)`，这是 bridge differential output。
2. plot `V(out)`，这是 amplified output。
3. `V(out)` 应该大约最低 `0.5 V`，最高大约 `4.35 V`。正负不完全对称是正常的，因为 `R + Delta R` 在分母里。
4. 截图：transient plot。最好分两个 pane，上面 `V(bplus,bminus)`，下面 `V(out)`。

DC operating point screenshot:

1. 把 transient directive 先保留也可以，再加：

```text
.op
```

2. Run。
3. 在 schematic 上 right click node，选 `Place .op Data Label`。
4. 至少标这些：`vdd`, `bplus`, `bminus`, `vref`, `out`。
5. `Delta R = 0` 时这些大概是：
   - `bplus ~= 2.5 V`
   - `bminus ~= 2.5 V`
   - `vref ~= 2.5 V`
   - `out ~= 2.5 V`

Supply current 和 power:

1. 在 `.op` 结果里按 `Ctrl+L` 打开 SPICE Error Log。
2. 找 `I(VDD)`。LTspice 的 source current 常常是负号，所以 supply current 用：

```text
I_supply = -I(VDD)
P_total = 5 V * I_supply
```

3. 只算 bridge 就已经大概是 `10 mA`，所以 power 大概 `50 mW`，再加 VREF divider 和 op amp quiescent current。最后以 LTspice 的 `I(VDD)` 为准。
4. 截图 schematic 时，可以用 text tool 在旁边写 `I_supply = ...` 和 `P_total = ...`。

## Part d: instrumentation amp transient

目标：同样是 20 dB gain，但 bridge 基本没有被 loading，所以 signal amplitude 会比 part c 大一点。

搭法：

1. bridge 用同一个模型。
2. 建议这里用：

```text
SINE(0 38 1k)
```

这样 no-loading 的 output 也还在 rails 里面，比较容易截图。
3. 第一阶段两个 ADA4661-2：
   - 上面 op amp 的 `+` 输入接一个 bridge node
   - 下面 op amp 的 `+` 输入接另一个 bridge node
   - 上面输出到上面 `-` 输入之间放 `Rfp = 45k`
   - 下面 `-` 输入到下面输出之间放 `Rfm = 45k`
   - 两个 `-` 输入之间放 `RG = 10k`
4. 第二阶段 difference amp：
   - 用 `R1 = 25k`, `R2 = 25k`
   - `+` 端那边的 bottom resistor 接 `vref`
   - `-` 端那边 feedback resistor 接 `out`
5. 如果 output sine 反相了，不要慌，只是两个 bridge input 接反了。part d 主要看 amplitude 变大。

看图和截图：

1. transient 还是：

```text
.tran 0 5m 0 1u
```

2. plot `V(bplus,bminus)` 和 `V(out)`。
3. 跟 part c 用同一个 `Delta R = 38 ohm` 对比，instrumentation amp 的 `V(out)` peak-to-peak 应该稍微更大。
4. 再跑 `.op`，在 schematic 上放 DC node voltage labels。零输入时主要节点还是大约 `2.5 V`。

## 最后交什么图

建议最后至少有 5 张图：

1. part b AC magnitude plot：标出 20 dB 和 3 dB bandwidth。
2. part c transient plot：`V(bplus,bminus)` 和 `V(out)`。
3. part c schematic：所有 DC node voltage labels，加 supply current 和 total power。
4. part d transient plot：`V(bplus,bminus)` 和 `V(out)`，显示 amplitude 比 difference amp 大。
5. part d schematic：所有 DC node voltage labels。

最容易扣分的地方：

- 忘记 buffer `VREF`，只用 divider 直接接很多东西。
- 两个 AC input 同相，导致差分输入变成 0。
- `R1/R2` 比例不完全 matching。
- `ADA4661-2` 电源脚没接 5 V 和 ground。
- 只 plot 单端 `V(bplus)`，没有 plot bridge differential output `V(bplus,bminus)`。
- 看到 `I(VDD)` 是负的就直接拿去算 power。要用 `-I(VDD)`。
