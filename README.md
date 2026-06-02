# Global Superstore Sales Dashboard

基于 `Global Superstore` 数据集开发的 Streamlit 销售经营驾驶舱。

在线演示：
[https://data-visualization-big-screen-wcsda4px4b2trrffg9rkuk.streamlit.app/](https://data-visualization-big-screen-wcsda4px4b2trrffg9rkuk.streamlit.app/)

## Preview

<img width="2232" height="1202" alt="dashboard preview" src="https://github.com/user-attachments/assets/bcbea974-0e1f-4d44-8a62-da3dec09d61b" />

演示视频：
[Dashboard Demo](https://github.com/user-attachments/assets/5eec6aa0-b161-47f2-a523-ce4e084daed7)

## Features

- 6 个核心 KPI：总销售额、总利润、订单数、利润率、客户数、客单价
- 左侧筛选器：年份范围、Market、Category
- 深色驾驶舱风格布局
- 多专题分析图表：
  - 月度销售、利润与利润率趋势
  - 地区销售分布
  - 品类销售构成
  - Top 10 产品利润排名
  - 客户类型分布
  - 折扣与利润关系
- 数据缓存：`@st.cache_data`
- 支持后续接入退货表并扩展退货分析

## Project Structure

```text
data-visualization-big-screen/
├─ app.py
├─ requirements.txt
├─ start_dashboard.bat
├─ README.md
├─ .gitignore
└─ data/
   └─ Global Superstore.csv
```

## Quick Start

### Option 1: Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

启动后访问：
[http://127.0.0.1:8501](http://127.0.0.1:8501)

### Option 2: Windows One-Click Launch

直接双击：

`start_dashboard.bat`

## Data

- 主数据文件：`data/Global Superstore.csv`
- 当前仓库默认包含销售主表
- 如果后续补充退货明细 CSV，并命名为包含 `return` 的文件放入 `data/` 目录，应用可自动识别并用于退货相关分析

## Deployment

本项目已可直接部署到 Streamlit Community Cloud。

部署参数：

- Repository: `AQ202202/data-visualization-big-screen`
- Branch: `main`
- Main file path: `app.py`

## Delivery Notes

如果需要发给客户或雇主，建议直接提供以下任一方式：

- 在线演示链接
- GitHub 仓库链接
- 完整项目压缩包

最少交付内容建议包含：

- `app.py`
- `requirements.txt`
- `README.md`
- `data/Global Superstore.csv`

## Tech Stack

- Streamlit
- Plotly
- Pandas

