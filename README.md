# Global Superstore 销售经营驾驶舱

基于 `Global Superstore` 数据集开发的 Streamlit 销售大屏，适合本地演示、项目交付和二次修改。

## 项目结构

```text
数据大屏/
├─ app.py
├─ requirements.txt
├─ start_dashboard.bat
├─ README.md
├─ data/
│  └─ Global Superstore.csv
└─ .gitignore
```

## 功能概览

- 6 个核心 KPI 指标
- 左侧筛选器：年份、Market、Category
- 销售趋势、市场分布、品类构成、利润排行、客户分布、折扣利润关系等专题图表
- 深色驾驶舱风格布局
- 支持 `@st.cache_data` 数据缓存

## 预览图
<img width="2232" height="1202" alt="image" src="https://github.com/user-attachments/assets/bcbea974-0e1f-4d44-8a62-da3dec09d61b" />


## 运行方式

### 方式一：双击启动

直接双击：

`start_dashboard.bat`

### 方式二：命令行启动

在项目目录执行：

```bash
pip install -r requirements.txt
streamlit run app.py
```

启动后浏览器访问：

[http://127.0.0.1:8501](http://127.0.0.1:8501)

## 数据说明

- 主数据文件：`data/Global Superstore.csv`
- 当前项目仅包含销售主表
- 如果后续补充退货明细表，并命名为包含 `return` 的 CSV 文件放入 `data/` 目录，应用会自动识别并计算退货率

## 交付建议

发给雇主时，建议直接打包整个项目文件夹，而不是只发 `app.py`。  
最少应包含以下文件：

- `app.py`
- `requirements.txt`
- `README.md`
- `data/Global Superstore.csv`

## 备注

- 当前页面已按本地横屏驾驶舱样式完成适配
- 若雇主希望线上访问，可进一步部署到 Streamlit Community Cloud、服务器或内网环境
