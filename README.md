# paper-lab-demo-perovskite

一个 **Paper Lab** 出图流水线的演示仓库：以 NASA GISTEMP v4 全球气温记录为数据集，
用三个可独立运行的出图脚本生成论文级图件，并由 `ledger.json` 记录数据、事实与图件的可追溯性。

## 仓库内容

| 路径 | 说明 |
|---|---|
| `scripts/fig1_annual_anomaly.py` + `.spec.json` | 图 1：1880–2025 年全球年均气温距平折线图（含 OLS 趋势线） |
| `scripts/fig2_monthly_heatmap.py` + `.spec.json` | 图 2：逐年 × 逐月距平热力图 |
| `scripts/fig3_decadal_means.py` + `.spec.json` | 图 3：十年均值柱状图（误差棒为 s.e.m.，n = 10） |
| `data/GLB.Ts+dSST.csv` | GISTEMP v4 land–ocean 全球均值数据集（1880–2025） |
| `ledger.json` | 数据 / 事实 / 图件台账：SHA-256 溯源、图件统计量、完整性审计结果 |

## 数据来源

- 数据集：**NASA Goddard Institute for Space Studies (GISS), GISTEMP v4**
- 文件：`Land-Ocean: Global Means (GLB.Ts+dSST.csv)`
- 原始地址：<https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv>
- 记录于 ledger：`data/GLB.Ts+dSST.csv`，12887 bytes
- SHA-256：`c9ce0750ca93a8241c42fe86cd5bf54d07b28b21ae650b0ae49a206907018cd9`

距平基准为 1951–1980 年均值。缺失值在原始 CSV 中标记为 `***`，由 spec 的
`naValues` 配置为 NaN。

## 环境要求

- Python 3.10+（本仓库用 3.12 验证）
- `numpy`、`pandas`、`matplotlib`

```bash
pip install numpy pandas matplotlib
```

## 运行

三个脚本都是**自包含**的：Paper Lab 的绘图引擎被逐字内联进每个文件，不依赖任何
私有包。脚本从 `<script>.spec.json` 读取绘图配置（kind、坐标轴、样式、区间统计等），
从仓库根目录解析数据路径（`script.parent.parent`）。

```bash
cd paper-lab-demo-perovskite

python scripts/fig1_annual_anomaly.py
python scripts/fig2_monthly_heatmap.py
python scripts/fig3_decadal_means.py
```

输出为 `scripts/figN_*.pdf` 与 `scripts/figN_*.png`（600 dpi）。默认输出目录是脚本所在
目录，可用 `--out` 改写：

```bash
python scripts/fig1_annual_anomaly.py --out ./out
```

运行时会向 stdout 打印三类结构化记录：

- `[paper-lab] …` —— 数据加载信息与逐项统计
- `PAPER_LAB_STATS {…}` —— 每个被绘制列的描述统计、OLS 斜率与标准误、区间均值
- `PAPER_LAB_RESULT {…}` —— 产出文件路径与数据集校验信息

脚本会校验数据集 SHA-256 与 spec 中的 `expectSha256` 是否一致；不一致会直接报错退出，
而不是画出一张对不上的图。这是本仓库可复现性的关键约束。

## 可追溯性（ledger.json）

`ledger.json` 记录了：

- `datasets` —— 数据集文件、字节数、SHA-256、来源说明
- `facts` —— 正文中引用的每个数字及其推导方式与出处
- `figures` —— 每个图件的脚本、spec、输出文件及其 SHA-256、绘图统计量
- `lastAudit` —— 最近一次完整性审计结果：`critical: 0`、`warnings: 0`、
  `untraceableNumbers: 0`、`verdict: "PASS"`

> **注意（与原工程的差异）**：在原 Paper Lab 工程中这三个脚本位于 `figures/` 目录。
> 本仓库把它们放在 `scripts/` 以获得更清晰的目录语义，因此 `ledger.json` 内的
> `script` / `spec` / `outputs` 路径已同步由 `figures/` 改写为 `scripts/`。
> 脚本正文、spec 内容、数据集以及 ledger 中所有 SHA-256 均**未改动**；
> 脚本可复现原图件（见下）。

## 验证状态

在把文件收入本仓库前，三个脚本都在本目录结构下重新运行过：

- 三个脚本均以退出码 0 结束，成功生成 PDF + PNG；
- 加载到的数据集 SHA-256 与 spec 中 `expectSha256` 一致
  （`c9ce0750…18cd9`）；
- 重新生成的 PNG 与原工程中的图件**逐字节一致**（SHA-256 相同），
  说明目录调整未影响输出。

## 许可与引用

数据集版权归 NASA GISS 所有，使用请引用 GISTEMP v4：

- GISTEMP Team, *GISS Surface Temperature Analysis (GISTEMP), version 4*.
  NASA Goddard Institute for Space Studies.
- Lenssen, N., G. Schmidt, J. Hansen, M. Menne, A. Persin, R. Ruedy, and
  D. Zyss (2019). *Improvements in the GISTEMP uncertainty model*.
  J. Geophys. Res. Atmos., 124(12), 6307–6326.
