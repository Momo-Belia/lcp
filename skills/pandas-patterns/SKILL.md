---
name: pandas-patterns
description: 数据分析和可视化中常用的 pandas 与 matplotlib 模式
---

## 数据加载
使用 `pd.read_csv()` 加载 CSV 文件。始终先检查 `df.info()` 和 `df.describe()`。

## 可视化
使用 `matplotlib` 绘制柱状图，使用 `seaborn` 绘制统计图。
使用 `plt.savefig("output.png", dpi=150, bbox_inches="tight")` 保存图像。

## 报告
将 Markdown 摘要写入 `report.md`，并与生成的图表放在一起。