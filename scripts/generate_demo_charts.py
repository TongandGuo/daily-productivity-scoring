# -*- coding: utf-8 -*-
"""
用脱敏示例数据跑一遍 Analysis.ipynb 里的核心逻辑，生成几张演示图放进 README。
Runs the core logic from Analysis.ipynb against the anonymized sample data
to produce a few demo charts for the README.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("results_demo", exist_ok=True)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

df_raw = pd.read_excel("周计划_template.xlsx")
df_raw.fillna(0, inplace=True)
df_raw["星期几"] = df_raw["Time"].dt.weekday
df_raw["week_name"] = df_raw["Time"].dt.strftime("%V")

open_day, close_day = "2025-01-01", "2025-06-30"
con1 = df_raw["Time"] >= open_day
con2 = df_raw["Time"] < close_day
df_period = df_raw[con1 & con2].copy()

# growth value
conditions = [
    df_period["Score"] < 80,
    (df_period["Score"] >= 80) & (df_period["Score"] < 110),
    (df_period["Score"] >= 110) & (df_period["Score"] < 140),
    df_period["Score"] >= 140,
]
growth_rates = [-0.001, 0.001, 0.005, 0.01]
df_period["Daily_Growth"] = np.select(conditions, growth_rates, default=np.nan)
df_period["Growth_Value"] = 100 * (1 + df_period["Daily_Growth"].fillna(0)).cumprod()
df_period["Cumulative_Growth_Pct"] = (df_period["Growth_Value"] / 100 - 1) * 100

mean_period = df_period["Score"].mean().round(2)
color_plate1 = ["burlywood", "firebrick", "k"]

# ---- chart 1: score trend + growth value ----
fig, (ax1, ax2) = plt.subplots(
    nrows=2, ncols=1, figsize=(16, 12), dpi=150, facecolor="w",
    gridspec_kw={"height_ratios": [2, 1], "hspace": 0.12}, sharex=True
)
ax1.plot("Time", "Score", data=df_period, color=color_plate1[0], marker="o", markersize=4,
         label=f"平均分 {mean_period}")
ax1.axhline(y=80, color=color_plate1[1], alpha=0.7, linewidth=1, linestyle="--", label="标准线 80")
ax1.axhline(y=40, color=color_plate1[1], alpha=0.7, linewidth=1, linestyle=":", label="休息线 40")
ax1.axhline(y=140, color=color_plate1[1], alpha=0.7, linewidth=1, linestyle="-.", label="成长线 140")
ax1.set_ylim(0, max(160, df_period["Score"].max() * 1.1))
ax1.set_ylabel("Score")
ax1.grid(axis="y", alpha=0.7)
ax1.legend()

current_value = df_period["Growth_Value"].iloc[-1]
current_growth_pct = df_period["Cumulative_Growth_Pct"].iloc[-1]
ax2.plot("Time", "Growth_Value", data=df_period, color=color_plate1[2], linewidth=2,
         label=f"当前成长值 {current_value:.2f} | 累计成长 {current_growth_pct:+.2f}%")
ax2.axhline(y=100, color="gray", alpha=0.7, linewidth=1, linestyle="--", label="初始值 100")
ax2.fill_between(df_period["Time"], 100, df_period["Growth_Value"], alpha=0.15)
ax2.set_ylabel("Growth Value")
ax2.set_xlabel("Time")
ax2.grid(axis="y", alpha=0.7)
ax2.legend()
fig.suptitle(f"Time period: {open_day} to {close_day} (sample data)", fontsize=22)
plt.savefig("results_demo/score_trend.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---- chart 2: task allocation donut ----
non_zero_counts = df_period[["Task1", "Task2", "Task3", "task_1", "task_2", "task_3",
                              "Life_1", "Life_2", "Life_3"]].apply(lambda x: (x != 0).sum())
main_task_sum = non_zero_counts[0:3].sum()
skill_sum = non_zero_counts[3:6].sum()
life_sum = non_zero_counts[6:9].sum()

category_names = ["主要任务次数", "能力提升次数", "生活任务次数"]
category_sizes = [main_task_sum, skill_sum, life_sum]
subcategory_names = ["Task1", "Task2", "Task3", "task_1", "task_2", "task_3", "Life_1", "Life_2", "Life_3"]
subcategory_sizes = non_zero_counts.values.tolist()
category_colors = ["#e74c3c", "#3498db", "#2980b9"]
subcategory_colors = ["#99ccff", "#ffcccc", "#3399ff", "#ff6666", "#99ffff", "#2c3e50", "#ecf0f1", "#2c3e50", "#ffcccc"]

fig, ax = plt.subplots(figsize=(10, 10), dpi=150, facecolor="w", edgecolor="b")
ax.pie(subcategory_sizes, radius=1.1, colors=subcategory_colors, labels=subcategory_names,
       autopct="%1.1f%%", pctdistance=0.92, startangle=90, wedgeprops=dict(width=0.2, edgecolor="w"))
inner_pie = ax.pie(category_sizes, radius=0.7, colors=category_colors,
                    autopct="%1.1f%%", pctdistance=0.75, startangle=90, wedgeprops=dict(width=0.3, edgecolor="w"))
centre_circle = plt.Circle((0, 0), 0.4, fc="white")
fig.gca().add_artist(centre_circle)
plt.legend(inner_pie[0], category_names, title="Categories", loc="center left", bbox_to_anchor=(1, 0.7))
plt.tight_layout()
plt.savefig("results_demo/task_donut.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---- chart 3: weekly average bar ----
import seaborn as sns
colors = sns.color_palette("Paired")
df_bar = df_period.groupby("week_name")[["Score"]].mean()
fig, ax = plt.subplots(figsize=(16, 8), dpi=150, facecolor="w", edgecolor="b")
ax.vlines(df_bar.index, ymin=0, ymax=df_bar["Score"], color=colors, alpha=0.7, linewidth=16)
plt.gca().set(ylim=(0, 140), ylabel="Score")
plt.title("week average score (sample data)", fontsize=18)
plt.xticks(df_bar.index, df_bar.index, fontsize=10, rotation=90)
plt.xlabel("Week number", fontsize=14)
for i, counts in enumerate(df_bar["Score"]):
    ax.text(i, counts + 0.5, round(counts, 1), horizontalalignment="center", fontsize=8)
plt.tight_layout()
plt.savefig("results_demo/week_average.png", dpi=150)
plt.close(fig)

print("demo charts saved to results_demo/")
