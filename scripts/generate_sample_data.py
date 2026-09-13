# -*- coding: utf-8 -*-
"""
生成脱敏示例数据 周计划_template.xlsx
Generates an anonymized sample dataset matching the schema of 周计划.xlsx,
using only generic, non-personal placeholder content.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

start = pd.Timestamp("2025-01-01")
n_days = 180
dates = pd.date_range(start, periods=n_days, freq="D")

# generic, non-personal placeholder pools
main_tasks = ["写代码", "开会", "读文档", "调试", "0"]
skill_tasks = ["学习新技术", "复盘", "看课程", "写笔记", "0"]
life_tasks = ["运动", "阅读", "休息", "做饭", "0"]
reflections = [
    "专注", "状态不错", "有点累", "收获很大", "按部就班", "需要调整", "效率很高",
    "灵感爆发", "保持节奏", "继续加油", "日常打卡", "满血复活", "慢慢来",
    "小小疲惫", "值得庆祝", "稳步推进", "还需努力", "心态平稳", "精力充沛",
    "",
]
milestones = ["0"] * 40 + ["阶段总结", "项目里程碑", "小目标达成"]

rows = []
for d in dates:
    weekday = d.weekday()
    base = 100 if weekday < 5 else 70
    score = float(np.clip(rng.normal(base, 20), 20, 150).round(0))
    rows.append({
        "Time": d,
        "Score": score,
        "Task1": rng.choice(main_tasks, p=[0.35, 0.2, 0.15, 0.1, 0.2]),
        "Task2": rng.choice(main_tasks, p=[0.2, 0.15, 0.15, 0.1, 0.4]),
        "Task3": rng.choice(main_tasks, p=[0.1, 0.1, 0.1, 0.1, 0.6]),
        "task_1": rng.choice(skill_tasks, p=[0.3, 0.2, 0.15, 0.1, 0.25]),
        "task_2": rng.choice(skill_tasks, p=[0.15, 0.15, 0.1, 0.1, 0.5]),
        "task_3": rng.choice(skill_tasks, p=[0.05, 0.05, 0.05, 0.05, 0.8]),
        "Life_1": rng.choice(life_tasks, p=[0.3, 0.2, 0.2, 0.1, 0.2]),
        "Life_2": rng.choice(life_tasks, p=[0.15, 0.15, 0.15, 0.1, 0.45]),
        "Life_3": rng.choice(life_tasks, p=[0.05, 0.05, 0.05, 0.05, 0.8]),
        "重大事件": rng.choice(milestones),
        "每日感悟": rng.choice(reflections),
        "预算挑战06": float(rng.integers(0, 30)) if rng.random() < 0.3 else 0.0,
    })

df = pd.DataFrame(rows)
df.to_excel("周计划_template.xlsx", index=False)
print("rows:", len(df))
print(df.head())
