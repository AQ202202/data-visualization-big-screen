import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from plotly.utils import PlotlyJSONEncoder


st.set_page_config(
    page_title="Global Superstore 销售驾驶舱",
    page_icon="📊",
    layout="wide",
)


PALETTE = {
    "bg": "#030A12",
    "bg_2": "#061522",
    "panel": "#0B1C2E",
    "panel_2": "#0F2740",
    "border": "#1D537F",
    "text": "#EAF6FF",
    "muted": "#8FB3D9",
    "blue_1": "#D7EFFF",
    "blue_2": "#94D3FF",
    "blue_3": "#58B7FF",
    "blue_4": "#2D8BFF",
    "blue_5": "#1C61BE",
    "blue_6": "#123B78",
    "cyan": "#39C6FF",
    "cyan_2": "#6BE4FF",
    "green": "#39D98A",
    "gold": "#FFC857",
    "rose": "#FF7CA8",
    "grid": "rgba(120, 185, 255, 0.10)",
}
BLUE_SERIES = [
    PALETTE["blue_1"],
    PALETTE["blue_2"],
    PALETTE["blue_3"],
    PALETTE["blue_4"],
    PALETTE["blue_5"],
    PALETTE["blue_6"],
]


st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at 12% 10%, rgba(57,198,255,0.16), transparent 22%),
            radial-gradient(circle at 88% 8%, rgba(45,139,255,0.12), transparent 18%),
            linear-gradient(180deg, {PALETTE["bg"]} 0%, {PALETTE["bg_2"]} 100%);
        color: {PALETTE["text"]};
    }}
    .block-container {{
        max-width: 118rem;
        padding-top: 1.1rem;
        padding-bottom: 0.3rem;
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
    }}
    [data-testid="stToolbar"] {{
        right: 0.75rem;
        top: 0.35rem;
        background: rgba(6, 21, 34, 0.55);
        border: 1px solid rgba(107,228,255,0.08);
        border-radius: 999px;
        backdrop-filter: blur(8px);
    }}
    .stAppToolbar {{
        background: transparent !important;
    }}
    [data-testid="stDecoration"] {{
        display: none;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(8,22,36,0.98), rgba(5,15,26,0.98));
        border-right: 1px solid rgba(107,228,255,0.10);
    }}
    [data-testid="stSidebar"] * {{
        color: {PALETTE["text"]};
    }}
    [data-testid="stMetric"] {{
        background: linear-gradient(180deg, rgba(12,33,54,0.98), rgba(8,22,36,0.98));
        border: 1px solid rgba(107,228,255,0.14);
        border-radius: 16px;
        padding: 10px 14px;
        box-shadow: 0 0 0 1px rgba(57,198,255,0.04), 0 10px 24px rgba(0,0,0,0.22);
        overflow: hidden;
        position: relative;
    }}
    [data-testid="stMetric"]::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(107,228,255,0.08), transparent);
        animation: sweep 5.2s linear infinite;
        transform: translateX(-100%);
    }}
    [data-testid="stMetricLabel"] {{
        color: {PALETTE["muted"]};
        letter-spacing: .04em;
    }}
    [data-testid="stMetricValue"] {{
        color: {PALETTE["text"]};
        font-weight: 800;
    }}
    [data-testid="stMetricDelta"] {{
        color: {PALETTE["blue_2"]};
    }}
    div[data-testid="stPlotlyChart"] {{
        background: linear-gradient(180deg, rgba(11,28,46,0.96), rgba(7,18,30,0.98));
        border: 1px solid rgba(107,228,255,0.12);
        border-radius: 18px;
        padding: .22rem .28rem .05rem .28rem;
        box-shadow: inset 0 0 18px rgba(57,198,255,0.03), 0 10px 24px rgba(0,0,0,0.22);
    }}
    .hero {{
        border: 1px solid rgba(107,228,255,0.14);
        border-radius: 20px;
        padding: 1.35rem .9rem .6rem .9rem;
        background: linear-gradient(180deg, rgba(11,31,50,0.96), rgba(7,18,30,0.96));
        position: relative;
        overflow: visible;
        box-shadow: inset 0 0 22px rgba(57,198,255,0.03), 0 12px 28px rgba(0,0,0,0.24);
    }}
    .hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(57,198,255,0.07), transparent);
        animation: sweep 7s linear infinite;
        transform: translateX(-100%);
    }}
    .hero-title {{
        text-align: center;
        font-size: 1.72rem;
        line-height: 1.38;
        font-weight: 800;
        letter-spacing: .10em;
        color: {PALETTE["text"]};
        text-shadow: 0 0 20px rgba(57,198,255,0.20);
        margin-top: .35rem;
        margin-bottom: .35rem;
    }}
    .hero-sub {{
        text-align: center;
        color: {PALETTE["muted"]};
        font-size: .88rem;
        margin-bottom: .3rem;
    }}
    .hero-row {{
        display:grid;
        grid-template-columns: 1.1fr 1fr 1fr 1fr;
        gap: .75rem;
    }}
    .hero-chip {{
        border: 1px solid rgba(107,228,255,0.10);
        border-radius: 14px;
        padding: .42rem .65rem;
        background: rgba(7,19,31,0.72);
    }}
    .hero-chip-label {{
        color: {PALETTE["muted"]};
        font-size: .78rem;
        margin-bottom: .15rem;
    }}
    .hero-chip-value {{
        color: {PALETTE["text"]};
        font-size: 1.05rem;
        font-weight: 700;
    }}
    .panel-wrap {{
        border: 1px solid rgba(107,228,255,0.12);
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(11,28,46,0.96), rgba(7,18,30,0.98));
        box-shadow: inset 0 0 18px rgba(57,198,255,0.03), 0 10px 24px rgba(0,0,0,0.22);
        padding: .25rem;
    }}
    .footer {{
        margin-top: .35rem;
        border: 1px solid rgba(107,228,255,0.10);
        border-radius: 14px;
        padding: .42rem .8rem;
        background: linear-gradient(180deg, rgba(11,28,46,0.94), rgba(7,18,30,0.96));
        color: {PALETTE["muted"]};
        line-height: 1.45;
        font-size: .8rem;
    }}
    @keyframes sweep {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    @media (max-width: 1300px) {{
        .hero-row {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def apply_theme(fig: go.Figure, height: int) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], family="Microsoft YaHei, Segoe UI, sans-serif"),
        margin=dict(l=28, r=28, t=54, b=28),
        hoverlabel=dict(
            bgcolor="#091726",
            bordercolor=PALETTE["border"],
            font=dict(color=PALETTE["text"]),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=PALETTE["text"]),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=PALETTE["grid"],
        zeroline=False,
        linecolor="rgba(143,179,217,0.18)",
        tickfont=dict(color=PALETTE["muted"]),
        title_font=dict(color=PALETTE["muted"]),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=PALETTE["grid"],
        zeroline=False,
        linecolor="rgba(143,179,217,0.18)",
        tickfont=dict(color=PALETTE["muted"]),
        title_font=dict(color=PALETTE["muted"]),
    )
    return fig


def apply_carousel_theme(fig: go.Figure, height: int = 400) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], family="Microsoft YaHei, Segoe UI, sans-serif"),
        margin=dict(l=24, r=24, t=64, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(color=PALETTE["text"], size=11),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=30,
        ),
        hoverlabel=dict(
            bgcolor="#091726",
            bordercolor=PALETTE["border"],
            font=dict(color=PALETTE["text"]),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(143,179,217,0.18)",
        tickfont=dict(color=PALETTE["muted"]),
        title_font=dict(color=PALETTE["muted"]),
        automargin=True,
    )
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(143,179,217,0.18)",
        tickfont=dict(color=PALETTE["muted"]),
        title_font=dict(color=PALETTE["muted"]),
        title_standoff=14,
        automargin=True,
    )
    return fig


def format_currency(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}%"


def format_delta(current: float, previous: float) -> str:
    if pd.isna(previous) or previous == 0:
        return "同比 N/A"
    delta = (current - previous) / abs(previous) * 100
    return f"{'↑' if delta >= 0 else '↓'} {abs(delta):.1f}%"


def resolve_data_files() -> tuple[Path, Path | None]:
    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    csv_files = sorted(data_dir.glob("*.csv")) if data_dir.exists() else []
    if not csv_files:
        csv_files = sorted(root.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("未找到 CSV 数据文件。")

    sales_file = next(
        (path for path in csv_files if "superstore" in path.name.lower() and "return" not in path.name.lower()),
        None,
    )
    if sales_file is None:
        sales_file = next((path for path in csv_files if "return" not in path.name.lower()), csv_files[0])
    returns_file = next((path for path in csv_files if "return" in path.name.lower()), None)
    return sales_file, returns_file


def parse_date_column(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(pd.NaT, index=df.index)

    raw = df[column].astype(str).str.strip()
    # The source file stores placeholder time-only text like "00:00.0",
    # which pandas may parse as "today at midnight". Treat these as invalid.
    time_only_mask = raw.str.fullmatch(r"\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?")
    normalized = raw.mask(time_only_mask, pd.NA)
    parsed = pd.to_datetime(normalized, errors="coerce")

    if parsed.notna().sum() == 0 and {"Year", "weeknum"}.issubset(df.columns):
        years = pd.to_numeric(df["Year"], errors="coerce").fillna(2011).astype(int)
        weeks = pd.to_numeric(df["weeknum"], errors="coerce").fillna(1).clip(lower=1, upper=53).astype(int)
        base = pd.to_datetime(
            years.astype(str) + "-W" + weeks.astype(str).str.zfill(2) + "-1",
            format="%G-W%V-%u",
            errors="coerce",
        )
        parsed = base + pd.to_timedelta(4 if column == "Ship Date" else 0, unit="D")
    return parsed


def build_return_flags(df: pd.DataFrame, returns_file: Path | None) -> tuple[pd.Series, bool]:
    if returns_file is None or "Order ID" not in df.columns:
        return pd.Series(False, index=df.index), False
    returns_df = pd.read_csv(returns_file)
    returns_df.columns = [col.strip() for col in returns_df.columns]
    order_col = next((col for col in returns_df.columns if col.lower() == "order id"), None)
    status_col = next((col for col in returns_df.columns if "return" in col.lower()), None)
    if order_col is None:
        return pd.Series(False, index=df.index), False
    if status_col:
        ids = returns_df.loc[
            returns_df[status_col].astype(str).str.contains("yes|return", case=False, na=False),
            order_col,
        ]
    else:
        ids = returns_df[order_col]
    order_ids = set(ids.dropna().astype(str).str.strip())
    return df["Order ID"].astype(str).str.strip().isin(order_ids), bool(order_ids)


@st.cache_data(show_spinner=False)
def load_data():
    sales_file, returns_file = resolve_data_files()
    df = pd.read_csv(sales_file)
    df.columns = [col.strip() for col in df.columns]

    for column in ["Sales", "Profit", "Discount", "Quantity", "Shipping Cost", "Year", "weeknum"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["Parsed Order Date"] = parse_date_column(df, "Order Date")
    df["Parsed Ship Date"] = parse_date_column(df, "Ship Date")
    df["Month"] = df["Parsed Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Shipping Days"] = (df["Parsed Ship Date"] - df["Parsed Order Date"]).dt.days
    df.loc[df["Shipping Days"] < 0, "Shipping Days"] = pd.NA
    df["Returned"], has_returns = build_return_flags(df, returns_file)
    meta = {
        "sales_file": sales_file,
        "returns_file": returns_file,
        "has_returns": has_returns,
    }
    return df, meta


def filter_data(df: pd.DataFrame, year_range: tuple[int, int], markets: list[str], categories: list[str]) -> pd.DataFrame:
    filtered = df[df["Year"].between(year_range[0], year_range[1], inclusive="both")].copy()
    if markets:
        filtered = filtered[filtered["Market"].isin(markets)]
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]
    return filtered


def summarize_metrics(frame: pd.DataFrame, has_returns: bool) -> dict[str, float]:
    sales = frame["Sales"].sum()
    profit = frame["Profit"].sum()
    orders = frame["Order ID"].nunique()
    customers = frame["Customer ID"].nunique()
    margin = (profit / sales * 100) if sales else float("nan")
    avg_order_value = (sales / orders) if orders else float("nan")
    return_orders = frame.loc[frame["Returned"], "Order ID"].nunique()
    return_rate = return_orders / orders * 100 if has_returns and orders else float("nan")
    avg_discount = frame["Discount"].mean() * 100 if "Discount" in frame.columns else float("nan")
    avg_shipping = frame["Shipping Days"].mean() if "Shipping Days" in frame.columns else float("nan")
    return {
        "sales": sales,
        "profit": profit,
        "orders": orders,
        "customers": customers,
        "margin": margin,
        "avg_order_value": avg_order_value,
        "return_rate": return_rate,
        "avg_discount": avg_discount,
        "avg_shipping": avg_shipping,
    }


def live_clock() -> None:
    now = datetime.now()
    st.markdown(
        f"""
        <div style="
            height:84px;
            margin-top:38px;
            border:1px solid rgba(107,228,255,.14);
            border-radius:16px;
            background:linear-gradient(180deg, rgba(12,32,52,.96), rgba(8,21,35,.96));
            box-shadow:0 10px 24px rgba(0,0,0,.22);
            color:#EAF6FF;
            text-align:center;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;">
          <div style="font-size:12px;color:#8FB3D9;letter-spacing:.15em;">运行时钟</div>
          <div style="font-size:24px;font-weight:800;color:#6BE4FF;line-height:1.1;margin-top:3px;">{now.strftime("%H:%M:%S")}</div>
          <div style="font-size:12px;color:#8FB3D9;margin-top:1px;">{now.strftime("%Y-%m-%d")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_marquee(messages: list[str]) -> None:
    text = "  |  ".join(messages)
    components.html(
        f"""
        <html><body style="margin:0;background:transparent;overflow:hidden;">
        <div style="
            width:100%;
            height:42px;
            border:1px solid rgba(107,228,255,.12);
            border-radius:999px;
            background:linear-gradient(180deg, rgba(10,27,44,.96), rgba(8,18,30,.96));
            overflow:hidden;
            display:flex;
            align-items:center;">
          <div style="
              white-space:nowrap;
              display:inline-block;
              padding-left:100%;
              color:#94D3FF;
              font-family:'Segoe UI','Microsoft YaHei',sans-serif;
              font-size:14px;
              animation:mar 22s linear infinite;">
            运行播报：{text}
          </div>
        </div>
        <style>
        @keyframes mar {{ 0% {{ transform:translateX(0); }} 100% {{ transform:translateX(-100%); }} }}
        </style>
        </body></html>
        """,
        height=46,
    )


def control_panel_html(current: dict[str, float], active_market: str, top_category: str) -> None:
    components.html(
        f"""
        <html><body style="margin:0;background:transparent;overflow:hidden;">
        <div style="
            position:relative;
            height:160px;
            border:1px solid rgba(107,228,255,.14);
            border-radius:18px;
            background:
                radial-gradient(circle at center, rgba(57,198,255,.13), transparent 34%),
                linear-gradient(180deg, rgba(11,30,48,.96), rgba(7,18,30,.98));
            overflow:hidden;
            font-family:'Segoe UI','Microsoft YaHei',sans-serif;
            color:#EAF6FF;">
          <div style="position:absolute;left:50%;top:50%;width:118px;height:118px;transform:translate(-50%,-50%);border-radius:50%;
              border:1px solid rgba(107,228,255,.18);box-shadow:0 0 24px rgba(57,198,255,.18), inset 0 0 18px rgba(57,198,255,.06);
              animation:pulse 3s ease-in-out infinite;"></div>
          <div style="position:absolute;left:50%;top:50%;width:164px;height:164px;transform:translate(-50%,-50%);
              border-radius:50%;border:1px dashed rgba(107,228,255,.14);animation:spin 16s linear infinite;"></div>
          <div style="position:absolute;left:50%;top:50%;width:208px;height:208px;transform:translate(-50%,-50%);
              border-radius:50%;border:1px dashed rgba(45,139,255,.08);animation:spin2 20s linear infinite;"></div>

          <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-56%);text-align:center;">
            <div style="font-size:12px;color:#8FB3D9;letter-spacing:.14em;">经营总控核心</div>
            <div style="font-size:26px;font-weight:800;color:#6BE4FF;line-height:1.15;">{format_currency(current["sales"])}</div>
            <div style="font-size:12px;color:#D7EFFF;">累计销售额</div>
          </div>
          <div style="position:absolute;left:16px;top:14px;">
            <div style="font-size:11px;color:#8FB3D9;">焦点市场</div>
            <div style="font-size:18px;font-weight:700;color:#94D3FF;">{active_market}</div>
          </div>
          <div style="position:absolute;right:16px;top:14px;text-align:right;">
            <div style="font-size:11px;color:#8FB3D9;">重点品类</div>
            <div style="font-size:18px;font-weight:700;color:#94D3FF;">{top_category}</div>
          </div>
          <div style="position:absolute;left:16px;bottom:14px;">
            <div style="font-size:11px;color:#8FB3D9;">利润率</div>
            <div style="font-size:18px;font-weight:700;color:#94D3FF;">{format_percent(current["margin"])}</div>
          </div>
          <div style="position:absolute;right:16px;bottom:14px;text-align:right;">
            <div style="font-size:11px;color:#8FB3D9;">订单总量</div>
            <div style="font-size:18px;font-weight:700;color:#94D3FF;">{int(current["orders"]):,}</div>
          </div>
        </div>
        <style>
        @keyframes spin {{ from {{ transform:translate(-50%,-50%) rotate(0deg); }} to {{ transform:translate(-50%,-50%) rotate(360deg); }} }}
        @keyframes spin2 {{ from {{ transform:translate(-50%,-50%) rotate(360deg); }} to {{ transform:translate(-50%,-50%) rotate(0deg); }} }}
        @keyframes pulse {{
            0% {{ box-shadow:0 0 12px rgba(57,198,255,.12), inset 0 0 12px rgba(57,198,255,.04); }}
            50% {{ box-shadow:0 0 28px rgba(57,198,255,.26), inset 0 0 24px rgba(57,198,255,.10); }}
            100% {{ box-shadow:0 0 12px rgba(57,198,255,.12), inset 0 0 12px rgba(57,198,255,.04); }}
        }}
        </style>
        </body></html>
        """,
        height=164,
    )


def build_market_map_fig(market_sales: pd.DataFrame, active_market: str) -> go.Figure:
    coords = {
        "US": (-98.5, 39.8),
        "Canada": (-106.3, 56.1),
        "LATAM": (-58.4, -15.6),
        "EU": (15.0, 50.0),
        "EMEA": (32.0, 24.0),
        "Africa": (20.0, 4.0),
        "APAC": (110.0, 20.0),
    }
    map_df = market_sales.copy()
    map_df["lon"] = map_df["Market"].map(lambda x: coords.get(x, (0, 0))[0])
    map_df["lat"] = map_df["Market"].map(lambda x: coords.get(x, (0, 0))[1])
    max_sales = map_df["Sales"].max() if not map_df.empty else 1
    map_df["size"] = map_df["Sales"] / max_sales * 22 + 8

    fig = go.Figure()
    active_rows = map_df.loc[map_df["Market"] == active_market]
    if not active_rows.empty:
        src_lon = active_rows["lon"].iat[0]
        src_lat = active_rows["lat"].iat[0]
        for _, row in map_df.iterrows():
            if row["Market"] == active_market:
                continue
            fig.add_trace(
                go.Scattergeo(
                    lon=[src_lon, row["lon"]],
                    lat=[src_lat, row["lat"]],
                    mode="lines",
                    line=dict(width=1.2, color="rgba(107,228,255,0.46)"),
                    opacity=0.95,
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    fig.add_trace(
        go.Scattergeo(
            lon=map_df["lon"],
            lat=map_df["lat"],
            text=map_df["Market"],
            customdata=map_df["Sales"],
            mode="markers+text",
            textposition="top center",
            marker=dict(
                size=map_df["size"],
                color=[PALETTE["cyan"] if m == active_market else PALETTE["blue_4"] for m in map_df["Market"]],
                line=dict(width=1.4, color="rgba(215,239,255,0.82)"),
                opacity=0.92,
            ),
            hovertemplate="%{text}<br>销售额: %{customdata:,.0f}<extra></extra>",
            showlegend=False,
        )
    )
    fig.update_layout(
        title="全球市场流向总览",
        height=325,
        margin=dict(l=8, r=8, t=50, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], family="Microsoft YaHei, Segoe UI, sans-serif"),
        geo=dict(
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)",
            showland=True,
            landcolor="rgba(15,39,64,0.94)",
            showcountries=True,
            countrycolor="rgba(107,228,255,0.16)",
            showocean=True,
            oceancolor="rgba(5,13,22,0.96)",
            showlakes=True,
            lakecolor="rgba(5,13,22,0.96)",
            coastlinecolor="rgba(107,228,255,0.12)",
        ),
    )
    return fig


def build_animated_map_component(market_sales: pd.DataFrame) -> None:
    coords = {
        "US": (-98.5, 39.8),
        "Canada": (-106.3, 56.1),
        "LATAM": (-58.4, -15.6),
        "EU": (15.0, 50.0),
        "EMEA": (32.0, 24.0),
        "Africa": (20.0, 4.0),
        "APAC": (110.0, 20.0),
    }
    market_sales = market_sales.copy()
    market_sales["lon"] = market_sales["Market"].map(lambda x: coords.get(x, (0, 0))[0])
    market_sales["lat"] = market_sales["Market"].map(lambda x: coords.get(x, (0, 0))[1])
    max_sales = market_sales["Sales"].max() if not market_sales.empty else 1
    market_sales["size"] = market_sales["Sales"] / max_sales * 22 + 8
    payload = json.dumps(
        {
            "market": market_sales["Market"].tolist(),
            "sales": market_sales["Sales"].round(2).tolist(),
            "lon": market_sales["lon"].tolist(),
            "lat": market_sales["lat"].tolist(),
            "size": market_sales["size"].tolist(),
        },
        ensure_ascii=False,
    )
    components.html(
        f"""
        <html>
        <head><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script></head>
        <body style="margin:0;background:transparent;overflow:hidden;">
        <div id="map" style="width:100%;height:258px;"></div>
        <script>
        const cfg = {payload};
        let active = 0;
        function buildLineTraces(focus) {{
          const lines = [];
          for (let i = 0; i < cfg.market.length; i++) {{
            if (i === focus) continue;
            lines.push({{
              type:'scattergeo',
              lon:[cfg.lon[focus], cfg.lon[i]],
              lat:[cfg.lat[focus], cfg.lat[i]],
              mode:'lines',
              line:{{width:1.2, color:'rgba(107,228,255,.42)'}},
              hoverinfo:'skip',
              showlegend:false
            }});
          }}
          return lines;
        }}
        function buildNodeTrace(focus) {{
          return {{
            type:'scattergeo',
            lon:cfg.lon,
            lat:cfg.lat,
            text:cfg.market,
            customdata:cfg.sales,
            mode:'markers+text',
            textposition:'top center',
            marker:{{
              size:cfg.size.map((v, i) => i === focus ? v + 8 : v),
              color:cfg.market.map((_, i) => i === focus ? '#39C6FF' : '#2D8BFF'),
              opacity:.92,
              line:{{color:'rgba(215,239,255,.82)', width:1.2}}
            }},
            hovertemplate:'%{{text}}<br>销售额: %{{customdata:,.0f}}<extra></extra>',
            showlegend:false
          }};
        }}
        const layout = {{
          title: {{text:'全球市场流向总览', font:{{color:'#EAF6FF', size:18}}}},
          paper_bgcolor:'rgba(0,0,0,0)',
          margin:{{l:8,r:8,t:46,b:6}},
          font:{{color:'#EAF6FF', family:'Microsoft YaHei, Segoe UI, sans-serif'}},
          geo:{{
            projection:{{type:'natural earth'}},
            bgcolor:'rgba(0,0,0,0)',
            showland:true,
            landcolor:'rgba(15,39,64,.94)',
            showcountries:true,
            countrycolor:'rgba(107,228,255,.16)',
            showocean:true,
            oceancolor:'rgba(5,13,22,.96)',
            showlakes:true,
            lakecolor:'rgba(5,13,22,.96)',
            coastlinecolor:'rgba(107,228,255,.12)'
          }}
        }};
        function render() {{
          const data = [...buildLineTraces(active), buildNodeTrace(active)];
          Plotly.react('map', data, layout, {{displayModeBar:false, responsive:true}});
        }}
        render();
        setInterval(() => {{
          active = (active + 1) % cfg.market.length;
          render();
        }}, 2200);
        </script>
        </body></html>
        """,
        height=262,
    )


def build_trend_showcase_component(monthly: pd.DataFrame) -> None:
    if monthly.empty:
        st.info("暂无月度趋势数据。")
        return

    monthly = monthly.copy()
    monthly["Label"] = monthly["Month"].dt.strftime("%Y-%m")

    payload = json.dumps(
        {
            "labels": monthly["Label"].tolist(),
            "sales": monthly["Sales"].round(2).tolist(),
            "profit": monthly["Profit"].round(2).tolist(),
            "margin": monthly["Profit Margin"].round(2).fillna(0).tolist(),
            "tickvals": monthly["Label"].iloc[::3].tolist(),
        },
        ensure_ascii=False,
    )

    components.html(
        f"""
        <html>
        <head><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script></head>
        <body style="margin:0;background:transparent;overflow:hidden;">
        <div id="trend_showcase" style="width:100%;height:418px;"></div>
        <script>
        const cfg = {payload};
        const data = [
          {{
            x: cfg.labels,
            y: cfg.sales,
            type: 'scatter',
            mode: 'lines+markers',
            name: '销售额底线',
            line: {{color:'rgba(57,198,255,0.22)', width:2}},
            marker: {{size:4, color:'rgba(57,198,255,0.22)'}},
            yaxis: 'y'
          }},
          {{
            x: cfg.labels,
            y: cfg.profit,
            type: 'scatter',
            mode: 'lines+markers',
            name: '利润底线',
            line: {{color:'rgba(57,217,138,0.18)', width:2}},
            marker: {{size:4, color:'rgba(57,217,138,0.18)'}},
            yaxis: 'y2'
          }},
          {{
            x: cfg.labels,
            y: cfg.margin,
            type: 'scatter',
            mode: 'lines',
            name: '利润率底线',
            line: {{color:'rgba(255,200,87,0.20)', width:2, dash:'dot'}},
            yaxis: 'y3'
          }},
          {{
            x: [cfg.labels[0]],
            y: [cfg.sales[0]],
            type: 'scatter',
            mode: 'lines+markers',
            name: '销售额',
            line: {{color:'#39C6FF', width:3.4}},
            marker: {{size:6, color:'#39C6FF'}},
            fill: 'tozeroy',
            fillcolor: 'rgba(57,198,255,0.08)',
            yaxis: 'y'
          }},
          {{
            x: [cfg.labels[0]],
            y: [cfg.profit[0]],
            type: 'scatter',
            mode: 'lines+markers',
            name: '利润',
            line: {{color:'#39D98A', width:2.8}},
            marker: {{size:5, color:'#39D98A'}},
            yaxis: 'y2'
          }},
          {{
            x: [cfg.labels[0]],
            y: [cfg.margin[0]],
            type: 'scatter',
            mode: 'lines',
            name: '利润率',
            line: {{color:'#FFC857', width:2.2, dash:'dot'}},
            yaxis: 'y3'
          }}
        ];

        const layout = {{
          title: {{text:'月度销售、利润与利润率趋势', font:{{color:'#EAF6FF', size:18}}}},
          paper_bgcolor:'rgba(0,0,0,0)',
          plot_bgcolor:'rgba(0,0,0,0)',
          margin:{{l:30,r:30,t:58,b:46}},
          font:{{color:'#EAF6FF', family:'Microsoft YaHei, Segoe UI, sans-serif'}},
          legend:{{orientation:'h', y:1.12, x:1, xanchor:'right'}},
          xaxis:{{
            type:'category',
            tickangle:-35,
            tickmode:'array',
            tickvals: cfg.tickvals,
            tickfont:{{color:'#8FB3D9'}},
            showgrid:false,
            zeroline:false
          }},
          yaxis:{{title:'销售额', tickfont:{{color:'#8FB3D9'}}, showgrid:false, zeroline:false}},
          yaxis2:{{title:'利润', overlaying:'y', side:'right', tickfont:{{color:'#8FB3D9'}}, showgrid:false, zeroline:false}},
          yaxis3:{{title:'利润率', overlaying:'y', side:'right', anchor:'free', position:.92, ticksuffix:'%', tickfont:{{color:'#8FB3D9'}}, showgrid:false, zeroline:false}}
        }};

        Plotly.newPlot('trend_showcase', data, layout, {{displayModeBar:false, responsive:true}});

        function interpolateSeries(values, progress) {{
          const maxIndex = values.length - 1;
          const scaled = progress * maxIndex;
          const idx = Math.floor(scaled);
          const frac = scaled - idx;
          const result = values.slice(0, idx + 1);
          if (idx < maxIndex) {{
            const nextVal = values[idx] + (values[idx + 1] - values[idx]) * frac;
            result.push(nextVal);
          }}
          return result;
        }}

        function interpolateLabels(labels, progress) {{
          const maxIndex = labels.length - 1;
          const scaled = progress * maxIndex;
          const idx = Math.floor(scaled);
          const result = labels.slice(0, idx + 1);
          if (idx < maxIndex) {{
            result.push(labels[idx + 1]);
          }}
          return result;
        }}

        let startTs = null;
        const duration = 5200;

        function animate(ts) {{
          if (!startTs) startTs = ts;
          const elapsed = (ts - startTs) % duration;
          const progress = elapsed / duration;

          const xVals = interpolateLabels(cfg.labels, progress);
          Plotly.restyle('trend_showcase', {{
            x: [xVals],
            y: [interpolateSeries(cfg.sales, progress)]
          }}, [3]);
          Plotly.restyle('trend_showcase', {{
            x: [xVals],
            y: [interpolateSeries(cfg.profit, progress)]
          }}, [4]);
          Plotly.restyle('trend_showcase', {{
            x: [xVals],
            y: [interpolateSeries(cfg.margin, progress)]
          }}, [5]);

          requestAnimationFrame(animate);
        }}

        requestAnimationFrame(animate);
        </script>
        </body></html>
        """,
        height=422,
    )


def build_rotating_pie_component(segment_sales: pd.DataFrame) -> None:
    if segment_sales.empty:
        st.info("暂无客户类型分布数据。")
        return
    labels = segment_sales["Segment"].tolist()
    values = segment_sales["Sales"].round(2).tolist()
    colors = [PALETTE["cyan"], PALETTE["green"], PALETTE["gold"], PALETTE["rose"]][: len(labels)]
    payload = json.dumps({"labels": labels, "values": values, "colors": colors}, ensure_ascii=False)
    components.html(
        f"""
        <html>
        <head><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script></head>
        <body style="margin:0;background:transparent;overflow:hidden;">
        <div id="pie" style="width:100%;height:236px;"></div>
        <script>
        const cfg = {payload};
        let rotation = 0;
        let focus = 0;
        const baseTrace = {{
          type: 'pie',
          labels: cfg.labels,
          values: cfg.values,
          hole: 0.62,
          sort: false,
          textinfo: 'percent',
          textfont: {{color:'#EAF6FF', size:12}},
          marker: {{colors: cfg.colors, line: {{color:'rgba(215,239,255,.86)', width:1.2}}}},
          pull: cfg.values.map(() => 0)
        }};
        const layout = {{
          title: {{text:'客户类型分布', font:{{color:'#EAF6FF', size:18}}}},
          paper_bgcolor:'rgba(0,0,0,0)',
          plot_bgcolor:'rgba(0,0,0,0)',
          margin:{{l:10,r:10,t:48,b:10}},
          showlegend:true,
          legend:{{orientation:'h', y:-0.05, font:{{color:'#EAF6FF'}}}},
          font:{{color:'#EAF6FF', family:'Microsoft YaHei, Segoe UI, sans-serif'}}
        }};
        Plotly.newPlot('pie', [baseTrace], layout, {{displayModeBar:false, responsive:true}});
        function tick(){{
          rotation = (rotation + 18) % 360;
          focus = (focus + 1) % cfg.values.length;
          const pull = cfg.values.map(() => 0);
          pull[focus] = 0.12;
          Plotly.restyle('pie', {{pull:[pull], rotation:[rotation]}});
        }}
        setInterval(tick, 1800);
        </script>
        </body>
        </html>
        """,
        height=240,
    )


def build_right_carousel_component(figures: list[go.Figure]) -> None:
    fig_json = [fig.to_plotly_json() for fig in figures]
    payload = json.dumps(fig_json, ensure_ascii=False, cls=PlotlyJSONEncoder)
    components.html(
        f"""
        <html>
        <head><script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script></head>
        <body style="margin:0;background:transparent;overflow:hidden;">
        <div style="
            height:430px;
            border:1px solid rgba(107,228,255,.12);
            border-radius:18px;
            background:linear-gradient(180deg, rgba(11,28,46,.96), rgba(7,18,30,.98));
            box-shadow:inset 0 0 18px rgba(57,198,255,.03), 0 10px 24px rgba(0,0,0,.22);
            overflow:hidden;
            position:relative;">
          <div style="
              position:absolute;left:16px;top:12px;z-index:5;
              color:#EAF6FF;font-family:'Microsoft YaHei','Segoe UI',sans-serif;
              font-size:16px;font-weight:700;letter-spacing:.04em;">
            右侧专题轮播区
          </div>
          <div id="dots" style="position:absolute;right:18px;top:14px;z-index:5;"></div>
          <div id="slide0" style="position:absolute;inset:40px 14px 12px 14px;"></div>
          <div id="slide1" style="position:absolute;inset:40px 14px 12px 14px;display:none;"></div>
          <div id="slide2" style="position:absolute;inset:40px 14px 12px 14px;display:none;"></div>
          <div id="slide3" style="position:absolute;inset:40px 14px 12px 14px;display:none;"></div>
        </div>
        <script>
        const figs = {payload};
        const ids = ['slide0','slide1','slide2','slide3'];
        let idx = 0;
        function renderDotBar(active){{
          const wrap = document.getElementById('dots');
          wrap.innerHTML = '';
          ids.forEach((_, i) => {{
            const dot = document.createElement('span');
            dot.style.display = 'inline-block';
            dot.style.width = i === active ? '18px' : '8px';
            dot.style.height = '8px';
            dot.style.borderRadius = '999px';
            dot.style.marginLeft = '6px';
            dot.style.transition = 'all .35s ease';
            dot.style.background = i === active ? '#6BE4FF' : 'rgba(148,211,255,.35)';
            wrap.appendChild(dot);
          }});
        }}
        function animateBuild(divId, fig){{
          const d = document.getElementById(divId);
          d.style.opacity = 0;
          d.style.transform = 'translateY(10px)';
          d.style.transition = 'all .55s ease';
          Plotly.react(d, fig.data, fig.layout, {{displayModeBar:false, responsive:true}}).then(() => {{
            Plotly.Plots.resize(d);
            requestAnimationFrame(() => {{
              d.style.opacity = 1;
              d.style.transform = 'translateY(0)';
            }});
          }});
        }}
        function show(i){{
          ids.forEach((id, n) => {{
            document.getElementById(id).style.display = n === i ? 'block' : 'none';
          }});
          renderDotBar(i);
          animateBuild(ids[i], figs[i]);
        }}
        show(0);
        setInterval(() => {{
          idx = (idx + 1) % ids.length;
          show(idx);
        }}, 3600);
        </script>
        </body>
        </html>
        """,
        height=434,
    )


df, meta = load_data()

required = {
    "Sales",
    "Profit",
    "Order ID",
    "Customer ID",
    "Market",
    "Category",
    "Sub-Category",
    "Product Name",
    "Segment",
    "Discount",
    "Year",
}
missing = sorted(required - set(df.columns))
if missing:
    st.error(f"数据缺少必要字段：{', '.join(missing)}")
    st.stop()


with st.sidebar:
    st.header("筛选器")
    year_min = int(df["Year"].dropna().min())
    year_max = int(df["Year"].dropna().max())
    year_range = st.slider("年份范围", year_min, year_max, (year_min, year_max))
    market_options = sorted(df["Market"].dropna().astype(str).unique().tolist())
    selected_markets = st.multiselect("Market", market_options, default=market_options)
    category_options = sorted(df["Category"].dropna().astype(str).unique().tolist())
    selected_categories = st.multiselect("Category", category_options, default=category_options)
    st.caption("当前布局为横屏驾驶舱，所有主要区域同时展示，右侧轮播只在区域内部切换。")


filtered_df = filter_data(df, year_range, selected_markets, selected_categories)
previous_df = filter_data(df, (year_range[0] - 1, year_range[1] - 1), selected_markets, selected_categories)
if filtered_df.empty:
    st.warning("当前筛选条件下没有可展示的数据，请调整左侧筛选器。")
    st.stop()


current = summarize_metrics(filtered_df, meta["has_returns"])
previous = summarize_metrics(previous_df, meta["has_returns"]) if not previous_df.empty else {
    key: float("nan") for key in current
}

market_sales = filtered_df.groupby("Market", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
top_market = market_sales["Market"].iat[0] if not market_sales.empty else "N/A"
top_category_df = (
    filtered_df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
)
top_category = top_category_df["Category"].iat[0] if not top_category_df.empty else "N/A"

header_cols = st.columns([5.2, 1.15])
with header_cols[0]:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">GLOBAL SUPERSTORE 销售经营驾驶舱</div>
            <div class="hero-sub">市场表现 / 商品结构 / 客户洞察 / 发货效率 / 退货监测</div>
            <div class="hero-row">
                <div class="hero-chip">
                    <div class="hero-chip-label">焦点市场</div>
                    <div class="hero-chip-value">{top_market}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">重点品类</div>
                    <div class="hero-chip-value">{top_category}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">平均折扣</div>
                    <div class="hero-chip-value">{format_percent(current["avg_discount"])}</div>
                </div>
                <div class="hero-chip">
                    <div class="hero-chip-label">平均发货时长</div>
                    <div class="hero-chip-value">{current["avg_shipping"]:.1f} 天</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_cols[1]:
    live_clock()

alert_marquee(
    [
        f"筛选区间 {year_range[0]} - {year_range[1]} 年，当前关注市场 {top_market}",
        f"总销售额 {format_currency(current['sales'])}，利润率 {format_percent(current['margin'])}",
        f"客单价 {format_currency(current['avg_order_value'])}，订单数 {int(current['orders']):,}",
        f"当前大屏为横屏主控模式，右侧轮播区正在自动切换专题图表",
    ]
)


kpi_cols = st.columns(6)
kpi_cols[0].metric("总销售额", format_currency(current["sales"]), format_delta(current["sales"], previous["sales"]))
kpi_cols[1].metric("总利润", format_currency(current["profit"]), format_delta(current["profit"], previous["profit"]))
kpi_cols[2].metric("订单数", f"{int(current['orders']):,}", format_delta(current["orders"], previous["orders"]))
kpi_cols[3].metric("利润率", format_percent(current["margin"]), format_delta(current["margin"], previous["margin"]))
kpi_cols[4].metric("客户数", f"{int(current['customers']):,}", format_delta(current["customers"], previous["customers"]))
kpi_cols[5].metric("客单价", format_currency(current["avg_order_value"]), format_delta(current["avg_order_value"], previous["avg_order_value"]))


monthly = (
    filtered_df.dropna(subset=["Month"])
    .groupby("Month", as_index=False)[["Sales", "Profit"]]
    .sum()
    .sort_values("Month")
)
monthly["Profit Margin"] = monthly["Profit"] / monthly["Sales"] * 100

segment_sales = filtered_df.groupby("Segment", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
subcat_top_sales = (
    filtered_df.groupby("Sub-Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
    .sort_values("Sales", ascending=True)
)
category_mix = (
    filtered_df.groupby(["Category", "Sub-Category"], as_index=False)["Sales"]
    .sum()
    .sort_values(["Category", "Sales"], ascending=[True, False])
)
product_profit = (
    filtered_df.groupby("Product Name", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
    .head(10)
    .sort_values("Profit", ascending=True)
)
scatter_df = filtered_df.dropna(subset=["Discount", "Profit", "Sales", "Category"]).copy()
shipping_df = filtered_df.dropna(subset=["Shipping Days"]).copy()


trend_fig = go.Figure()
trend_fig.add_trace(
    go.Scatter(
        x=monthly["Month Label"] if "Month Label" in monthly.columns else monthly["Month"].dt.strftime("%Y-%m"),
        y=monthly["Sales"],
        mode="lines+markers",
        name="销售额",
        line=dict(color=PALETTE["cyan"], width=3),
        marker=dict(size=6),
    )
)
trend_fig.add_trace(
    go.Scatter(
        x=monthly["Month Label"] if "Month Label" in monthly.columns else monthly["Month"].dt.strftime("%Y-%m"),
        y=monthly["Profit"],
        mode="lines+markers",
        name="利润",
        line=dict(color=PALETTE["green"], width=2.6),
        marker=dict(size=6),
        yaxis="y2",
    )
)
trend_fig.add_trace(
    go.Scatter(
        x=monthly["Month Label"] if "Month Label" in monthly.columns else monthly["Month"].dt.strftime("%Y-%m"),
        y=monthly["Profit Margin"],
        mode="lines",
        name="利润率",
        line=dict(color=PALETTE["gold"], width=2.2, dash="dot"),
        yaxis="y3",
    )
)
trend_fig.update_layout(
    title="月度销售、利润与利润率趋势",
    xaxis=dict(title="", type="category", tickangle=-35),
    yaxis=dict(title="销售额"),
    yaxis2=dict(title="利润", overlaying="y", side="right"),
    yaxis3=dict(title="利润率", overlaying="y", side="right", anchor="free", position=0.92, ticksuffix="%"),
)
apply_theme(trend_fig, 420)


subcat_top_fig = px.bar(
    subcat_top_sales,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="子品类销售 Top 10",
    color="Sales",
    text_auto=".2s",
    color_continuous_scale=[PALETTE["blue_2"], PALETTE["cyan"], PALETTE["green"]],
)
subcat_top_fig.update_layout(coloraxis_showscale=False, xaxis_title="销售额", yaxis_title="")
apply_theme(subcat_top_fig, 236)


scatter_fig = px.scatter(
    scatter_df,
    x="Discount",
    y="Profit",
    size="Sales",
    color="Category",
    title="折扣与利润关系",
    opacity=0.72,
    hover_data=["Product Name", "Market", "Sub-Category"],
    color_discrete_sequence=[PALETTE["cyan"], PALETTE["green"], PALETTE["gold"], PALETTE["rose"]],
)
scatter_fig.update_layout(xaxis_title="折扣", yaxis_title="利润")
apply_theme(scatter_fig, 236)


market_bar_fig = px.bar(
    market_sales,
    x="Market",
    y="Sales",
    title="地区销售分布",
    color="Market",
    text_auto=".2s",
    color_continuous_scale=BLUE_SERIES,
)
market_bar_fig.update_layout(coloraxis_showscale=False, xaxis_title="", yaxis_title="销售额")
apply_theme(market_bar_fig, 186)


category_fig = px.bar(
    category_mix,
    x="Category",
    y="Sales",
    color="Sub-Category",
    barmode="stack",
    title="品类销售构成",
    color_discrete_sequence=[
        "#87A9C4",
        "#A4C49A",
        "#C8BC78",
        "#97B6CF",
        "#B6CFAE",
        "#D4C88F",
        "#789FC0",
        "#95BA89",
        "#B6AA63",
        "#ABC5DB",
        "#C0D7B8",
        "#E0D3A0",
    ],
)
category_fig.update_layout(title="品类销售构成", xaxis_title="", yaxis_title="销售额")
category_fig.update_traces(marker_line_color="rgba(220,238,255,0.08)", marker_line_width=0.6)
category_fig.update_layout(showlegend=False)
apply_carousel_theme(category_fig, 400)


product_fig = px.bar(
    product_profit,
    x="Profit",
    y="Product Name",
    orientation="h",
    title="Top 10 产品利润排名",
    color="Profit",
    text_auto=".2s",
    color_continuous_scale=["#D9ECFB", "#9FCAF5", "#4E92DF", "#244C8E"],
)
product_fig.update_layout(coloraxis_showscale=False, xaxis_title="利润", yaxis_title="")
apply_carousel_theme(product_fig, 400)


market_share_df = market_sales.copy()
market_share_df["Share"] = market_share_df["Sales"] / market_share_df["Sales"].sum() * 100
share_palette = ["#96A9D8", "#AFC2DE", "#C2D9D1", "#D6DEC6", "#E4D8C4", "#CACFE0", "#979EB7"]
market_share_fig = px.pie(
    market_share_df.sort_values("Share", ascending=False),
    names="Market",
    values="Share",
    title="\u5e02\u573a\u9500\u552e\u4efd\u989d",
    hole=0.60,
    color_discrete_sequence=share_palette,
)
market_share_fig.update_traces(
    textinfo="percent",
    textposition="inside",
    hovertemplate="\u5e02\u573a: %{label}<br>\u4efd\u989d: %{value:.1f}%<extra></extra>",
    marker=dict(line=dict(color="rgba(6,18,30,0.82)", width=1.6)),
    sort=False,
    rotation=270,
)
apply_carousel_theme(market_share_fig, 400)
legend_annotations = [
    dict(
        text="\u5e02\u573a\u4efd\u989d",
        x=0.66,
        y=0.50,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=16, color=PALETTE["text"]),
    )
]
legend_shapes = []
legend_y = 0.67
for i, row in enumerate(market_share_df.sort_values("Share", ascending=False).itertuples(index=False)):
    y = legend_y - i * 0.075
    legend_annotations.append(
        dict(
            text=f"{row.Market}",
            x=0.15,
            y=y,
            xref="paper",
            yref="paper",
            xanchor="left",
            showarrow=False,
            font=dict(size=11, color=PALETTE["text"]),
        )
    )
    legend_shapes.append(
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0.10,
            x1=0.12,
            y0=y - 0.013,
            y1=y + 0.013,
            line=dict(width=0),
            fillcolor=share_palette[i % len(share_palette)],
        )
    )
market_share_fig.update_layout(
    showlegend=False,
    margin=dict(l=14, r=18, t=64, b=18),
    annotations=legend_annotations,
    shapes=legend_shapes,
)
market_share_fig.update_traces(domain=dict(x=[0.42, 0.90], y=[0.14, 0.88]))

market_bar_carousel_fig = px.bar(
    market_sales,
    x="Market",
    y="Sales",
    title="地区销售分布",
    text_auto=".2s",
    color="Market",
    color_discrete_sequence=["#728FAE", "#87A9AA", "#9EBE9D", "#BEB39F", "#C9B6C2", "#A7B7CA", "#889FB3"],
)
market_bar_carousel_fig.update_traces(
    marker_line_color="rgba(220,238,255,0.18)",
    marker_line_width=1.2,
)
apply_carousel_theme(market_bar_carousel_fig, 400)
market_bar_carousel_fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="销售额")


row1_left, row1_center, row1_right = st.columns([1.18, 1.72, 1.30])
with row1_left:
    build_trend_showcase_component(monthly)

with row1_center:
    control_panel_html(current, top_market, top_category)
    build_animated_map_component(market_sales)

with row1_right:
    build_right_carousel_component([product_fig, market_bar_carousel_fig, category_fig, market_share_fig])

row2_left, row2_center, row2_right = st.columns([1.18, 1.72, 1.30])
with row2_left:
    st.plotly_chart(subcat_top_fig, width="stretch")

with row2_center:
    st.plotly_chart(scatter_fig, width="stretch")

with row2_right:
    build_rotating_pie_component(segment_sales)


sales_mtime = datetime.fromtimestamp(meta["sales_file"].stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
footer_lines = [
    f"数据来源：{meta['sales_file'].name}",
    f"数据文件最后修改时间：{sales_mtime}",
    f"页面当前更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "布局说明：中间总控区为主视觉，左侧为经营监控，右侧为专题轮播区；所有核心块同时展示。",
]
if meta["returns_file"] is not None:
    footer_lines.insert(1, f"退货率口径：{meta['returns_file'].name} 通过 Order ID 与订单表关联计算。")

st.markdown('<div class="footer">' + "<br>".join(footer_lines) + "</div>", unsafe_allow_html=True)
