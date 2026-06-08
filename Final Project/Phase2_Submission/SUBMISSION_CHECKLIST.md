# Phase 2 submission checklist

最后主提交物：

```text
Phase2_Submission/EE533_Project_Phase2.ipynb
```

提交前必须做：

1. 按 `LTspice_Phase2_Guide.md` 跑 LTspice。
2. 把截图按下面文件名放进 `Phase2_Submission/screenshots/`：

```text
phase1_amp_op.png
phase1_unfiltered_noise.png
filter_op.png
filter_ac.png
top_level_op_power.png
top_level_ac.png
top_level_noise.png
transient_wave_export.png
```

3. 把 LTspice 导出的 `sampled_noise_phase2.wav` 放进 `Phase2_Submission/`。
4. 在 `Phase2_Submission/` 里重新运行整本 notebook。
5. 确认 notebook 里没有 `Missing screenshot`。
6. 确认最后 ADC SNR 仍然大于 75 dB。

如果 Canvas 允许多个附件，建议一起上传：

```text
EE533_Project_Phase2.ipynb
你的 LTspice .asc 文件
screenshots/ 文件夹压缩包
```

如果 Canvas 只允许一个文件，只交已经重新运行、截图已嵌入输出的 notebook。
