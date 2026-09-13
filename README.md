<title>工作效率打分 / Daily Productivity Scoring</title>

# 工作效率打分 · Daily Productivity Scoring

个人每日效率打分的可视化分析工具：从一张 Excel 周计划表出发，统计一段时间内的平均分、任务完成情况，并自动生成分数趋势图、周均分图、任务占比环形图、里程碑时间轴和词云。

A visualization toolkit for personal daily productivity scores: starting from a weekly-plan spreadsheet, it computes period averages and task-completion stats, and auto-generates a score trend chart, weekly-average bar chart, task-share donut chart, a milestone timeline, and a word cloud.

[中文说明](#中文说明) | [English](#english)

---

## 中文说明

### 这是什么

这是我个人用来记录每日效率（工作 / 能力提升 / 生活）的打分系统的分析脚本。每天在 Excel 里记一行：今天的分数、完成了哪些主要任务/技能提升/生活事项、有没有重大事件、写一句每日感悟。`Analysis.ipynb` 负责把这些原始记录清洗、统计、画图，帮我复盘一段时间（比如一个月、一个季度）的状态。

### 功能

- **数据清洗**：读取周计划表，补全空值，按周/星期解析时间。
- **区间统计**：任选起止日期，计算区间内的平均分、天数、主要任务完成次数、能力提升次数、生活任务次数。
- **成长值曲线**：按每日分数区间（<80 / 80-110 / 110-140 / ≥140）赋予不同的日增长率，滚动计算一个类似"复利成长值"的指标，用来看长期趋势而不是被单日波动干扰。
- **可视化**：
  - 分数趋势图（每日分数 + 成长值双图）
  - 周均分 bar 图
  - 任务时间分配环形图（主要任务 / 能力提升 / 生活，双层）
  - 里程碑时间轴（基于"重大事件"列）
  - 每日感悟词云（jieba 分词 + 停用词过滤）

### 数据结构

代码依赖一份 Excel 文件 `周计划.xlsx`（**真实数据未包含在本仓库中，见下方"隐私说明"**），需要包含以下列：

| 列名 | 类型 | 说明 |
|---|---|---|
| `Time` | 日期 | 当天日期 |
| `Score` | 数字 | 当天效率分数 |
| `Task1` / `Task2` / `Task3` | 文本 | 当天完成的主要任务（无则填 0） |
| `task_1` / `task_2` / `task_3` | 文本 | 当天的能力提升类事项（无则填 0） |
| `Life_1` / `Life_2` / `Life_3` | 文本 | 当天的生活类事项（无则填 0） |
| `重大事件` | 文本 | 当天的重大事件/里程碑（无则填 0） |
| `每日感悟` | 文本 | 一句话感悟，用于生成词云 |
| `预算挑战06` | 数字 | 自定义的额外指标（示例中为预算相关挑战分，可按需替换/删除） |

### 快速开始

```bash
pip install -r requirements.txt
```

准备好符合上表结构的 `周计划.xlsx`，放在项目根目录，然后：

```bash
jupyter notebook Analysis.ipynb
```

按顺序运行单元格即可；生成的图片会保存在 `results_bild/` 目录下。

### 隐私说明

`周计划.xlsx` 是我的真实个人日记式记录（包含每日感悟、生活细节等隐私内容），因此**没有**包含在这个公开仓库里（见 `.gitignore`）。仓库里只公开了分析代码本身。如果你想直接体验效果，请自行准备一份符合上述数据结构的 Excel 文件。

### License

本项目使用 [MIT License](LICENSE)。

---

## English

### What is this

This is the analysis notebook I use to track my own daily "productivity score" (work / skill-building / life). Every day I log one row in Excel: a score, which main tasks / skill-building items / life items got done, any major event, and a one-line daily reflection. `Analysis.ipynb` cleans that raw log, computes statistics, and renders charts so I can review a period (a month, a quarter) at a glance.

### Features

- **Data cleaning**: loads the weekly-plan spreadsheet, fills missing values, derives weekday/ISO week from the date.
- **Period statistics**: pick any start/end date and get the period's average score, day count, main-task completions, skill-building completions, and life-task completions.
- **"Growth value" curve**: buckets each day's score (<80 / 80-110 / 110-140 / ≥140) into a daily growth rate and compounds it over time — a smoothed, compound-interest-style indicator of long-term trend, less noisy than the raw daily score.
- **Visualizations**:
  - Score trend chart (daily score + compounded growth value)
  - Weekly-average bar chart
  - Task-allocation donut chart (main tasks / skill-building / life, two rings)
  - Milestone timeline (from the "major events" column)
  - Word cloud of daily reflections (jieba segmentation + stopword filtering)

### Data schema

The notebook expects an Excel file named `周计划.xlsx` (**the real data file is not included in this repo** — see Privacy below) with these columns:

| Column | Type | Description |
|---|---|---|
| `Time` | date | The date of the entry |
| `Score` | number | That day's productivity score |
| `Task1` / `Task2` / `Task3` | text | Main tasks completed that day (`0` if none) |
| `task_1` / `task_2` / `task_3` | text | Skill-building items that day (`0` if none) |
| `Life_1` / `Life_2` / `Life_3` | text | Life/personal items that day (`0` if none) |
| `重大事件` (major event) | text | Any milestone/major event that day (`0` if none) |
| `每日感悟` (daily reflection) | text | A one-line reflection, used to build the word cloud |
| `预算挑战06` (budget challenge) | number | A custom extra metric (a budget-challenge score in my own log — replace or drop as needed) |

### Quick start

```bash
pip install -r requirements.txt
```

Prepare a `周计划.xlsx` matching the schema above and place it in the project root, then:

```bash
jupyter notebook Analysis.ipynb
```

Run the cells in order; generated charts are saved to `results_bild/`.

### Privacy note

`周计划.xlsx` is my real personal, diary-like log (daily reflections, personal life details, etc.), so it is **intentionally excluded** from this public repo (see `.gitignore`). Only the analysis code is published. To try it yourself, prepare your own spreadsheet following the schema above.

### License

[MIT License](LICENSE).
