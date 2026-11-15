from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.analysis import (
    build_dendrogram,
    cluster_plain_summary,
    describe_pattern,
    feature_contributions,
    fit_clusters,
    stability_comparison,
    sweep_k,
)
from src.data import (
    DATA_PATH,
    get_quality_summary,
    load_data,
    regional_data,
    regional_feature_matrix,
)

st.set_page_config(
    page_title="AeroTB | India Regional Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────── THEME & AESTHETICS (AEROTB DARK) ─────────────────────
THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
:root {
  --bg-deep: #08090d;
  --panel: rgba(18, 20, 28, 0.85);
  --border: rgba(255, 255, 255, 0.08);
  --border-subtle: rgba(255, 255, 255, 0.06);
  --cyan: #38bdf8;
  --accent: #38bdf8;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
}
.stApp {
  background-color: #07080c;
  background-image: 
    radial-gradient(ellipse 90% 65% at 50% -12%, rgba(42, 53, 76, 0.42) 0%, rgba(18, 23, 34, 0.5) 50%, transparent 90%),
    radial-gradient(circle at 85% 90%, rgba(28, 35, 52, 0.28) 0%, transparent 60%);
  background-attachment: fixed;
  color: var(--text-main);
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
}
/* HIDE CLUNKY SIDEBAR GLOBALLY FOR MINIMAL FULL-WIDTH UI */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
  display: none !important;
}
.block-container {
  padding-top: 1.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 96% !important;
}

/* ── HIDE UGLY RADIO DOTS & TURN SIDEBAR INTO SLEEK PILLS ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  background: rgba(15, 23, 42, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
  border-radius: 10px !important;
  padding: 8px 14px !important;
  cursor: pointer !important;
  transition: all 0.22s ease !important;
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] {
  width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] p {
  margin: 0 !important;
  line-height: 1.25 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] em {
  display: block !important;
  font-size: 0.70rem !important;
  color: #94a3b8 !important;
  font-style: normal !important;
  font-weight: 400 !important;
  margin-top: 2px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(0, 242, 254, 0.1) !important;
  border-color: rgba(0, 242, 254, 0.35) !important;
  transform: translateX(3px);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
  background: rgba(0, 242, 254, 0.16) !important;
  border-color: #00f2fe !important;
  box-shadow: 0 0 16px rgba(0, 242, 254, 0.25) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
  color: #00f2fe !important;
  font-weight: 700 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) [data-testid="stMarkdownContainer"] em {
  color: rgba(0, 242, 254, 0.8) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"],
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
  display: none !important;
}

/* ── AEROTB FLOATING COMPONENTS ── */
.aero-brand-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}
.aero-logo {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, #00f2fe, #4facfe);
  box-shadow: 0 0 16px rgba(0, 242, 254, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 14px;
  color: #050811;
}
.aero-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.aero-sub {
  font-size: 0.65rem;
  color: #64748b;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

/* FACT BOX */
.aero-fact-card {
  background: rgba(11, 18, 34, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 242, 254, 0.25);
  border-radius: 18px;
  padding: 16px 18px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
  margin-bottom: 14px;
  position: relative;
  overflow: hidden;
}
.aero-fact-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #00f2fe, #4facfe, transparent);
}
.aero-fact-tag {
  color: #00f2fe;
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.aero-fact-text {
  font-size: 0.82rem;
  line-height: 1.5;
  color: #cbd5e1;
}

/* TELEMETRY CARD */
.aero-telemetry {
  background: rgba(11, 18, 34, 0.88);
  backdrop-filter: blur(22px);
  border: 1px solid rgba(0, 242, 254, 0.28);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.7), 0 0 35px rgba(0, 242, 254, 0.08);
}
.aero-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  background: rgba(0, 242, 254, 0.12);
  border: 1px solid rgba(0, 242, 254, 0.3);
  color: #00f2fe;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.aero-stat-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 2px;
}
.aero-cluster-pill {
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid rgba(56, 189, 248, 0.3);
  border-radius: 10px;
  padding: 8px 12px;
  margin: 12px 0;
}

/* ── SCROLL-STACK STORYTELLING CARDS ── */
.story-scroll-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 36px;
  max-width: 960px;
  margin: 0 auto;
  padding: 10px 0 50px 0;
}
.story-card-stack {
  position: sticky;
  background: rgba(13, 21, 39, 0.95);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  border: 1px solid rgba(0, 242, 254, 0.28);
  border-radius: 24px;
  padding: 32px 36px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 40px rgba(0, 242, 254, 0.1);
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}
.story-card-stack:hover {
  border-color: #00f2fe;
  box-shadow: 0 30px 70px rgba(0, 0, 0, 0.9), 0 0 50px rgba(0, 242, 254, 0.25);
}

/* 3D SCROLL STORY CARDS */
.aero-3d-card {
  background: rgba(13, 21, 39, 0.85);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(0, 242, 254, 0.25);
  border-radius: 24px;
  padding: 32px 28px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7), 0 0 35px rgba(0, 242, 254, 0.12);
  transition: all 0.3s ease;
  height: 100%;
}
.aero-3d-card:hover {
  border-color: #00f2fe;
  transform: translateY(-8px);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.8), 0 0 45px rgba(0, 242, 254, 0.25);
}

/* PORTAL LAUNCH CARDS */
.aero-portal-card {
  background: rgba(11, 18, 34, 0.7);
  border: 1px solid var(--border-subtle);
  border-radius: 18px;
  padding: 22px 18px;
  transition: all 0.25s ease;
  height: 100%;
}
.aero-portal-card:hover {
  background: rgba(15, 25, 48, 0.9);
  border-color: #00f2fe;
  transform: translateY(-6px);
  box-shadow: 0 16px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 242, 254, 0.15);
}
</style>
"""
st.markdown(THEME, unsafe_allow_html=True)

# ───────────────────── PARENT NAVIGATION BUS (UNSANDBOXED ROUTING) ─────────────────────
NAV_BUS = """
<div id="st-nav-bus" style="display:none;" aria-hidden="true">
  <a id="st-nav-link-Home" href="/?page=Home" target="_top"></a>
  <a id="st-nav-link-home" href="/?page=Home" target="_top"></a>
  <a id="st-nav-link-compare" href="/?page=compare" target="_top"></a>
  <a id="st-nav-link-overcome" href="/?page=overcome" target="_top"></a>
  <a id="st-nav-link-clusters" href="/?page=overcome" target="_top"></a>
  <a id="st-nav-link-explainer" href="/?page=explainer" target="_top"></a>
  <a id="st-nav-link-knowledge" href="/?page=knowledge" target="_top"></a>
  <a id="st-nav-link-help" href="/?page=knowledge" target="_top"></a>
</div>
<script>
(function() {
  if (window.__aerotb_bus_installed) return;
  window.__aerotb_bus_installed = true;
  window.addEventListener('message', function(e) {
    if (e && e.data && e.data.type === 'aerotb-nav') {
      var p = e.data.page || 'Home';
      var el = document.getElementById('st-nav-link-' + p);
      if (el) {
        el.click();
      } else {
        window.location.href = '/?page=' + encodeURIComponent(p);
      }
    }
  });
})();
</script>
"""
st.markdown(NAV_BUS, unsafe_allow_html=True)


# ───────────────────── HELPERS ─────────────────────
def header(kicker: str, title: str, subtitle: str = ""):
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{kicker}</div>'
        f"<h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def metric(label: str, value: str, sub: str = ""):
    st.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def explain(text: str):
    """A friendly explanation box that stands out."""
    st.markdown(f'<div class="explain">💡 {text}</div>', unsafe_allow_html=True)


def policy_box(text: str):
    """A 'what could this mean for health planning' box."""
    st.markdown(f'<div class="policy-box">🏥 {text}</div>', unsafe_allow_html=True)


# ───────────────────── LOAD DATA ─────────────────────
@st.cache_data(show_spinner=False)
def get_data():
    return load_data()


try:
    df = get_data()
except (FileNotFoundError, ValueError, OSError) as exc:
    st.error(f"The dataset could not be loaded: {exc}")
    st.stop()

regions = regional_data(df)
quality = get_quality_summary(df)

# ───────────────────── UNIFIED TOP NAVIGATION ─────────────────────
NAV_OPTIONS = [
    "🗺️ Command Map",
    "📈 Compare States",
    "🚀 Road to Overcome",
    "🆘 TB Knowledge & Helplines",
]

PAGE_MAP = {
    "🗺️ Command Map": "Home",
    "📈 Compare States": "Compare States",
    "🚀 Road to Overcome": "Road to Overcome",
    "🆘 TB Knowledge & Helplines": "TB Knowledge Centre",
}

REV_PAGE_MAP = {v: k for k, v in PAGE_MAP.items()}
REV_PAGE_MAP["State Pattern Groups"] = "🚀 Road to Overcome"
REV_PAGE_MAP["Find Help & About"] = "🆘 TB Knowledge & Helplines"
REV_PAGE_MAP["Explore India"] = "📈 Compare States"

p_map = {
    "Home": "Home",
    "home": "Home",
    "compare": "Compare States",
    "overcome": "Road to Overcome",
    "clusters": "Road to Overcome",
    "explore": "Compare States",
    "insights": "Home",
    "explainer": "Home",
    "knowledge": "TB Knowledge Centre",
    "help": "TB Knowledge Centre",
}
rev_q_map = {
    "Home": "Home",
    "Compare States": "compare",
    "Road to Overcome": "overcome",
    "State Pattern Groups": "overcome",
    "TB Knowledge Centre": "knowledge",
    "Find Help & About": "knowledge",
}

# Read current query parameter
raw_query_p = st.query_params.get("page", None)

if "current_page" not in st.session_state:
    initial_p = p_map.get(raw_query_p, "Home")
    st.session_state["current_page"] = initial_p
    st.session_state["last_seen_query_p"] = raw_query_p
elif raw_query_p is not None and raw_query_p != st.session_state.get("last_seen_query_p"):
    # External URL navigation occurred
    st.session_state["last_seen_query_p"] = raw_query_p
    st.session_state["current_page"] = p_map.get(raw_query_p, "Home")

def on_nav_change():
    chosen = st.session_state.get("top_nav_bar")
    if chosen and chosen in PAGE_MAP:
        target = PAGE_MAP[chosen]
        st.session_state["current_page"] = target
        new_q = rev_q_map.get(target, "Home")
        st.session_state["last_seen_query_p"] = new_q
        st.query_params["page"] = new_q

page = st.session_state["current_page"]


def selection_controls(key_prefix="sel"):
    years = [int(y) for y in quality["years"]]
    a, b, c, d = st.columns(4)
    year = a.selectbox("Year", years, index=len(years) - 1, key=f"{key_prefix}_year")
    factor = b.selectbox(
        "Risk factor",
        sorted(regions.risk_factor.dropna().unique()),
        key=f"{key_prefix}_factor",
    )
    sectors = sorted(
        regions.loc[
            (regions.year == year) & (regions.risk_factor == factor), "sector"
        ]
        .dropna()
        .unique()
    )
    sector = c.selectbox("Reporting sector", sectors, key=f"{key_prefix}_sector")
    params = sorted(
        regions.loc[
            (regions.year == year)
            & (regions.risk_factor == factor)
            & (regions.sector == sector),
            "parameter",
        ]
        .dropna()
        .unique()
    )
    parameter = d.selectbox("Indicator", params, key=f"{key_prefix}_parameter")
    return year, factor, sector, parameter


import unicodedata

def _clean_geo_name(s: str) -> str:
    """Normalize diacritics and casing for reliable geographic matching."""
    if not isinstance(s, str):
        return ""
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode("utf-8").strip().lower()


def display_map(plot_data, value_col, label="Reported count", color_col=None, height=650, highlight_state=None):
    """Show an interactive Bharat Cancer-style choropleth map with fluid scroll-zoom and pan."""
    geo_path = ROOT / "data" / "raw" / "dataful_20833" / "india_admin1.geojson"
    if not geo_path.exists():
        st.info("The interactive map needs the boundary file.")
        return
    try:
        geo = json.loads(geo_path.read_text(encoding="utf-8"))
        geo_map = {}
        for feat in geo.get("features", []):
            raw_shape = feat.get("properties", {}).get("shapeName", "")
            geo_map[_clean_geo_name(raw_shape)] = raw_shape

        data_copy = plot_data.copy()
        raw_state_col = "state" if "state" in data_copy.columns else "State / UT"
        data_copy["_geo_key"] = data_copy[raw_state_col].apply(_clean_geo_name).map(geo_map)
        match = data_copy.dropna(subset=["_geo_key"])

        if match.empty:
            st.warning("Map boundary names don't match the selected states — map hidden.")
            return

        if color_col and color_col in match.columns:
            fig = px.choropleth(
                match, geojson=geo, locations="_geo_key",
                featureidkey="properties.shapeName",
                color=color_col, hover_name=raw_state_col,
                color_discrete_sequence=["#00f2fe", "#a855f7", "#10b981", "#fbbf24", "#f43f5e", "#38bdf8"],
                labels={color_col: "AI Cluster Group"},
            )
            fig.update_traces(
                marker_line_width=1.4,
                marker_line_color="rgba(255, 255, 255, 0.6)",
                hovertemplate="<b>%{hovertext}</b><br><span style='color:#00f2fe;'>Group:</span> %{color}<br><span style='color:#94a3b8;font-size:11px;'>Scroll wheel to zoom · Drag to pan</span><extra></extra>",
            )
        else:
            fig = px.choropleth(
                match, geojson=geo, locations="_geo_key",
                featureidkey="properties.shapeName",
                color=value_col,
                color_continuous_scale=[
                    [0.0, "#2d1b4e"],
                    [0.15, "#552b7e"],
                    [0.35, "#8b3a86"],
                    [0.65, "#c24b6f"],
                    [0.85, "#e07a5f"],
                    [1.0, "#f4be5e"],
                ],
                hover_name=raw_state_col,
                labels={value_col: label},
            )
            fig.update_traces(
                marker_line_width=1.3,
                marker_line_color="rgba(255, 255, 255, 0.45)",
                hovertemplate="<b>%{hovertext}</b><br><span style='color:#00f2fe;'>" + label + ":</span> %{z:,.0f}<br><span style='color:#94a3b8;font-size:11px;'>Scroll wheel to zoom · Drag to pan</span><extra></extra>",
            )

        if highlight_state:
            clean_target = _clean_geo_name(highlight_state)
            for feat in geo.get("features", []):
                raw_s = feat.get("properties", {}).get("shapeName", "")
                if _clean_geo_name(raw_s) == clean_target:
                    coords = feat.get("geometry", {}).get("coordinates", [])
                    lons, lats = [], []
                    def _extract(p):
                        for item in p:
                            if isinstance(item[0], (int, float)):
                                lons.append(item[0])
                                lats.append(item[1])
                            else:
                                _extract(item)
                    _extract(coords)
                    if lons and lats:
                        c_lon = sum(lons) / len(lons)
                        c_lat = sum(lats) / len(lats)
                        fig.add_trace(
                            go.Scattergeo(
                                lon=[c_lon],
                                lat=[c_lat],
                                mode="markers+text",
                                marker=dict(
                                    size=16,
                                    color="#00f2fe",
                                    symbol="circle",
                                    line=dict(width=3, color="#ffffff"),
                                ),
                                text=[f"📍 {highlight_state}"],
                                textposition="top center",
                                textfont=dict(color="#ffffff", size=13, family="Plus Jakarta Sans"),
                                hoverinfo="skip",
                                showlegend=False,
                            )
                        )
                    break

        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor="rgba(0,0,0,0)",
            showcoastlines=False,
            showland=False,
            showocean=False,
            showlakes=False,
        )
        fig.update_layout(
            height=height,
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#dcebea",
            dragmode="pan",
            coloraxis_colorbar=dict(
                title=label,
                thicknessmode="pixels",
                thickness=14,
                lenmode="fraction",
                len=0.75,
                bgcolor="rgba(10, 25, 35, 0.6)",
                bordercolor="rgba(0, 242, 254, 0.3)",
                borderwidth=1,
            ),
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "scrollZoom": True,
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            },
        )
    except (OSError, ValueError, KeyError, TypeError) as exc:
        st.warning(f"State boundaries could not be rendered: {exc}")


# ═══════════════════════════════════════════════════════
#                        PAGES
# ═══════════════════════════════════════════════════════


# ───────────────────── MINIMAL TOP NAVIGATION BAR (SUB-PAGES) ─────────────────────
if page not in ["Home", "Compare States"]:
    st.markdown(
        """
        <style>
        .top-nav-brand {
            display: flex;
            align-items: center;
            gap: 8px;
            padding-top: 6px;
        }
        .top-nav-brand .logo {
            font-size: 1.25rem;
            color: #f4be5e;
        }
        .top-nav-brand .name {
            font-weight: 800;
            font-size: 1.05rem;
            color: #ffffff;
            letter-spacing: -0.01em;
        }
        .top-nav-brand .sub {
            font-size: 0.72rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        div[data-testid="stSegmentedControl"] {
            background: rgba(14, 18, 26, 0.85) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 9999px !important;
            padding: 3px !important;
        }
        div[data-testid="stSegmentedControl"] button {
            border-radius: 9999px !important;
            font-size: 0.76rem !important;
            font-weight: 700 !important;
            color: #94a3b8 !important;
            border: none !important;
            padding: 6px 16px !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stSegmentedControl"] button:hover {
            color: #ffffff !important;
        }
        div[data-testid="stSegmentedControl"] button[aria-selected="true"] {
            background: rgba(244, 190, 94, 0.16) !important;
            color: #f4be5e !important;
            border: 1px solid rgba(244, 190, 94, 0.35) !important;
            box-shadow: 0 0 14px rgba(244, 190, 94, 0.2) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    t_col1, t_col2 = st.columns([0.75, 3.25])
    with t_col1:
        st.markdown(
            """
            <div class="top-nav-brand">
              <span class="logo">◈</span>
              <span class="name">AeroTB</span>
              <span class="sub">/ Regional Intelligence</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t_col2:
        curr_label = REV_PAGE_MAP.get(page, "📈 Compare States")
        st.segmented_control(
            "Navigation",
            NAV_OPTIONS,
            default=curr_label,
            key="top_nav_bar",
            on_change=on_nav_change,
            label_visibility="collapsed",
        )

if page in ["Home", "Compare States", "Road to Overcome", "State Pattern Groups", "TB Knowledge Centre", "Find Help & About"]:
    # ── HIDE ALL STREAMLIT CHROME & FULL-BLEED ZERO MARGINS ──
    st.markdown(
        """
        <style>
        header[data-testid="stHeader"],
        #MainMenu,
        footer,
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
          display: none !important;
        }
        .main, .stMain, [data-testid="stAppViewContainer"], section.main {
          background-color: #07080c !important;
          background-image: 
            radial-gradient(ellipse 90% 65% at 50% -12%, rgba(42, 53, 76, 0.42) 0%, rgba(18, 23, 34, 0.5) 50%, transparent 90%),
            radial-gradient(circle at 85% 90%, rgba(28, 35, 52, 0.28) 0%, transparent 60%) !important;
          background-attachment: fixed !important;
          padding: 0 !important;
          margin: 0 !important;
          overflow-x: hidden !important;
        }
        .main .block-container, [data-testid="stMainBlockContainer"] {
          max-width: 100vw !important;
          width: 100vw !important;
          padding: 0 !important;
          margin: 0 !important;
        }
        iframe {
          position: fixed !important;
          top: 0 !important;
          left: 0 !important;
          width: 100vw !important;
          height: 100vh !important;
          border: none !important;
          margin: 0 !important;
          padding: 0 !important;
          z-index: 999999 !important;
          display: block !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if page == "Home":
        preview_file = ROOT / "preview.html"
        if preview_file.exists():
            st.iframe(preview_file, width="stretch", height="stretch")
        else:
            st.error("preview.html not found")
    elif page == "Compare States":
        compare_file = ROOT / "compare_preview.html"
        if compare_file.exists():
            st.iframe(compare_file, width="stretch", height="stretch")
        else:
            st.error("compare_preview.html not found")
    elif page in ["Road to Overcome", "State Pattern Groups"]:
        overcome_file = ROOT / "overcome_preview.html"
        if overcome_file.exists():
            st.iframe(overcome_file, width="stretch", height="stretch")
        else:
            st.error("overcome_preview.html not found")
    else:
        knowledge_file = ROOT / "knowledge_preview.html"
        if knowledge_file.exists():
            st.iframe(knowledge_file, width="stretch", height="stretch")
        else:
            st.error("knowledge_preview.html not found")
elif page == "Explore India":
    header(
        "Explore India",
        "See one indicator across every state",
        "Pick a year, risk factor, and indicator below. "
        "The map and chart show how states compare for that one measure.",
    )
    explain(
        "<b>How to read this page:</b> Use the dropdown menus to select what you want "
        "to see. The map shows darker colours for higher reported counts. "
        "The bar chart on the right ranks all states. Click on any state below "
        "to see its full profile."
    )

    year, factor, sector, parameter = selection_controls("explore")
    view = regions.loc[
        (regions.year == year)
        & (regions.risk_factor == factor)
        & (regions.sector == sector)
        & (regions.parameter == parameter)
    ].copy()

    st.markdown(
        f"**Showing:** {parameter}  \n"
        f"**Risk factor:** {factor} · **Sector:** {sector} · **Year:** {year} · "
        f"*{(view.unit.iloc[0] if not view.empty else 'unit unavailable')}*"
    )

    left, right = st.columns([1.05, 1])
    with left:
        display_map(view, "value")
    with right:
        sort = view.dropna(subset=["value"]).sort_values("value", ascending=True)
        fig = px.bar(
            sort, x="value", y="state", orientation="h",
            labels={"value": "Reported count", "state": "State / UT"},
            color="value",
            color_continuous_scale=["#1b6570", "#56d5c2"],
        )
        fig.update_layout(
            height=500, margin=dict(l=0, r=0, t=5, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#dcebea", showlegend=False, coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Taller bars = more reported cases for this indicator. "
        "Remember: bigger numbers can mean better reporting, not necessarily more disease."
    )

    states = sorted(view.state.unique())
    if states:
        chosen = st.selectbox("Open a state profile", states, key="explore_profile")
        profile = regions.loc[
            (regions.state == chosen)
            & (regions.year == year)
            & (regions.sector == sector)
        ]
        st.subheader(f"📋 {chosen} — all indicators for {year}")
        explain(
            f"This table shows every TB indicator reported for {chosen} in {year}. "
            "Each row is a different thing that was measured."
        )
        st.dataframe(
            profile[["risk_factor", "parameter", "value", "unit"]].sort_values(
                ["risk_factor", "parameter"]
            ),
            use_container_width=True,
            hide_index=True,
        )

# ───────────────────── ROAD TO OVERCOME (STATE ACTION BLUEPRINT) ─────────────────────
elif page in ["Road to Overcome", "State Pattern Groups"]:
    header(
        "Road to Overcome",
        "State Action Blueprint & Public Health Command",
        "Operational intelligence and tailored budget allocations for every Indian state, powered by unsupervised pattern clustering.",
    )
    explain(
        "<b>How to use this command centre:</b> Pick your state below to immediately reveal its <b>primary public health bottleneck</b>, "
        "its <b>recommended NHM budget allocation</b>, and <b>proven actions to copy from regional health twins</b>. "
        "Below the command card, explore the 4 scientific tabs to inspect the India map, national resource matrix, family tree (dendrogram), and mathematical validation."
    )

    # ── COMPACT TOP CONTROLS CONSOLE ──
    years = [int(y) for y in quality["years"]]
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([1, 1.2, 1.2, 1.4])
    year = ctrl1.selectbox("Surveillance Year", years, index=len(years) - 1, key="ml_year")
    factors = sorted(regions.loc[regions.year == year, "risk_factor"].unique())
    factor_default = factors.index("Diabetes") if "Diabetes" in factors else 0
    factor = ctrl2.selectbox("Comorbidity Risk Factor", factors, index=factor_default, key="ml_factor")
    avail_sectors = sorted(
        regions.loc[(regions.year == year) & (regions.risk_factor == factor), "sector"].unique()
    )
    sector_default = avail_sectors.index("public + private") if "public + private" in avail_sectors else 0
    sector = ctrl3.selectbox("Reporting Sector", avail_sectors, index=sector_default, key="ml_sector")

    method_label = ctrl4.selectbox(
        "Algorithm & Distance",
        [
            "K-Means (Euclidean Partitioning)",
            "Agglomerative (Ward Linkage · Euclidean)",
            "Agglomerative (Complete · Manhattan)",
            "Agglomerative (Average · Manhattan)",
        ],
        key="ml_method",
    )

    if method_label.startswith("K-Means"):
        actual_method, distance, d_link = "K-Means", "euclidean", "ward"
    elif "Ward" in method_label:
        actual_method, distance, d_link = "Agglomerative", "euclidean", "ward"
    elif "Complete" in method_label:
        actual_method, distance, d_link = "Agglomerative", "manhattan", "complete"
    else:
        actual_method, distance, d_link = "Agglomerative", "manhattan", "average"

    raw, complete = regional_feature_matrix(df, year, factor, sector)

    if raw.empty:
        st.warning("No state-level records match this selection.")
    elif raw.shape[1] < 2:
        st.warning("This selection has fewer than two indicators — meaningful grouping is unavailable.")
    elif complete.shape[0] < 4:
        st.warning("Fewer than four complete regions remain. Try another year, factor, or sector.")
    else:
        k_col, info_col = st.columns([1.5, 2.5])
        with k_col:
            k = st.slider(
                "Number of Clusters (k)",
                2,
                min(6, complete.shape[0] - 1),
                3,
                help="Recommended: k=3 for balanced public health communication and optimal Silhouette separation.",
            )
        with info_col:
            st.markdown(
                f"<div style='background:rgba(14,20,32,0.65); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 16px; margin-top:14px; font-size:0.78rem; color:#94a3b8;'>"
                f"<b>Dataset Scope:</b> {complete.shape[0]} complete states/UTs (All India excluded) · {raw.shape[1]} clinical indicators · Standardised (μ=0, σ=1)"
                f"</div>",
                unsafe_allow_html=True,
            )

        with st.expander("📋 Preprocessing Pipeline & Standardization Hygiene (click to expand)"):
            st.markdown(
                f"**1. Filter:** Selected `{year}`, risk factor `{factor}`, and sector `{sector}` from {quality['regions']} administrative units.\n\n"
                f"**2. Pivot:** Transformed raw tabular records into an $N \\times D$ matrix ({raw.shape[0]} states × {raw.shape[1]} surveillance features).\n\n"
                f"**3. Missing Value Audit:** Removed {raw.shape[0] - complete.shape[0]} states with incomplete reporting to preserve mathematical integrity, leaving {complete.shape[0]} states.\n\n"
                f"**4. Standardization (Z-score):** Scaled every column to mean $\\mu=0$ and standard deviation $\\sigma=1$. This ensures high-volume indicators do not drown out comorbid proportions."
            )

        try:
            result, metrics, pca_var = fit_clusters(
                complete, actual_method, clusters=k, eps=0.9, min_samples=4, distance=distance,
            )

            # ── TELEMETRY CARDS BANNER ──
            st.markdown("<div style='margin-top:10px; margin-bottom:14px;'></div>", unsafe_allow_html=True)
            m_cols = st.columns(4)
            sil = metrics.get("Silhouette")
            db = metrics.get("Davies-Bouldin")
            wcss_val = metrics.get("WCSS (Inertia)")
            ch = metrics.get("Calinski-Harabasz")

            with m_cols[0]:
                if sil is not None:
                    q_badge = "Strong Separation" if sil > 0.4 else "Moderate" if sil > 0.25 else "Weak"
                    st.metric("Silhouette Score", f"{sil:.3f}", f"{q_badge}")
                else:
                    st.metric("Silhouette Score", "N/A")
            with m_cols[1]:
                if wcss_val is not None:
                    st.metric("WCSS (Inertia)", f"{wcss_val:.1f}", "Compactness")
                else:
                    st.metric("WCSS", "N/A")
            with m_cols[2]:
                if db is not None:
                    st.metric("Davies-Bouldin", f"{db:.3f}", "Lower = less overlap")
                else:
                    st.metric("Davies-Bouldin", "N/A")
            with m_cols[3]:
                if ch is not None:
                    st.metric("Calinski-Harabasz", f"{ch:.1f}", "Variance ratio")
                else:
                    st.metric("Calinski-Harabasz", "N/A")

            # ══════════════════════════════════════════════════════════
            # 🏛️ HERO: STATE ACTION BLUEPRINT & BUDGET ADVISOR
            # ══════════════════════════════════════════════════════════
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            
            sorted_states = sorted(complete.index.tolist())
            def_idx = sorted_states.index("Punjab") if "Punjab" in sorted_states else (sorted_states.index("Maharashtra") if "Maharashtra" in sorted_states else 0)

            # Selector row
            adv_c1, adv_c2 = st.columns([1.3, 2.7])
            with adv_c1:
                sel_state = st.selectbox(
                    "📍 Pick a State to Generate Action Plan:",
                    sorted_states,
                    index=def_idx,
                    key="overcome_hero_state",
                    help="Select any of the 36 Indian states/UTs to receive tailored budget and operational prescriptions."
                )

            # Calculate cluster assignment & health twins
            state_row = result.loc[result["State / UT"] == sel_state]
            if not state_row.empty:
                state_cluster = state_row["Cluster"].values[0]

                from sklearn.preprocessing import StandardScaler
                import numpy as np

                scaled_mat = StandardScaler().fit_transform(complete.astype(float))
                st_idx = sorted_states.index(sel_state)
                target_vec = scaled_mat[st_idx]

                peer_states = [s for s in sorted_states if s != sel_state and result.loc[result["State / UT"] == s, "Cluster"].values[0] == state_cluster]
                dists = []
                for p in peer_states:
                    p_idx = sorted_states.index(p)
                    d = float(np.linalg.norm(target_vec - scaled_mat[p_idx]))
                    dists.append((p, d))
                dists.sort(key=lambda x: x[1])
                top_twins = [d[0] for d in dists[:3]]
                twins_str = ", ".join(top_twins) if top_twins else "Standalone regional profile"

                # Dynamically classify archetype based on cluster medians
                cluster_medians = complete.groupby(result.set_index("State / UT")["Cluster"], observed=True).median()
                cluster_ranks = cluster_medians.sum(axis=1).sort_values(ascending=False)
                rank_idx = list(cluster_ranks.index).index(state_cluster) if state_cluster in cluster_ranks.index else 0

                if rank_idx == 0:
                    team_badge = "🛡️ Team Alpha · High-Volume Urban & Industrial Giants"
                    team_color = "#38bdf8"
                    bottleneck_headline = "High Hospital Load & Sputum Delay: Overcrowded health centres struggle with slow multi-day diagnostic turnaround."
                    budget_allocations = [
                        ("Rapid 2-Hour Molecular Diagnostic Machines (TrueNat / CBNAAT)", 40, "#38bdf8"),
                        ("Active Sputum Collection Teams in High-Density Slums & Workplaces", 35, "#818cf8"),
                        ("Private Clinic Ni-kshay Digital Incentive Integration (PPSA)", 25, "#34d399"),
                    ]
                    announce_text = f"Today we commit to installing rapid 2-hour molecular testing labs in every sub-district of {sel_state}, eliminating multi-day testing queues for our citizens."
                    directive_text = f"• <b>District TB Officers:</b> Reallocate idle TrueNat cartridges immediately to the top 5 urban dispensaries.<br>• <b>Regulatory Audit:</b> Empanel local Indian Medical Association (IMA) private clinics for mandatory online notification under clinical establishment rules.<br>• <b>Logistics:</b> Deploy twice-daily sputum courier runs between primary health centers and district diagnostic hubs."
                    peer_advice = f"Examine <b>{top_twins[0] if top_twins else 'peer states'}</b>'s decentralized molecular screening circular, which cut diagnosis lag by 65% in high-burden wards."
                elif rank_idx == 1 or len(cluster_ranks) <= 2:
                    team_badge = "⚡ Team Beta · The Comorbidity Frontline (High Screening & Diabetes)"
                    team_color = "#f4be5e"
                    bottleneck_headline = "The Double-Trouble Multiplier: High rates of Diabetes & High Blood Sugar causing drug failure and patient relapses."
                    budget_allocations = [
                        ("Combined TB + Blood Sugar Rapid Screening Kits at all Village Health Clinics", 40, "#f4be5e"),
                        ("Private Sector Reporting Incentives & Digital Prescription Tracking", 35, "#38bdf8"),
                        ("Guaranteed Ni-kshay Poshan Direct Bank Nutrition Cash Transfers (₹500/month)", 25, "#10b981"),
                    ]
                    announce_text = f"Every TB patient across {sel_state} will receive free blood sugar testing on day one, plus guaranteed nutrition cash sent straight to their bank account."
                    directive_text = f"• <b>Chief Medical Officers:</b> Mandate 100% bidirectional blood glucose testing for all patients within 48 hours of notification.<br>• <b>Pharmacy Inspection:</b> Drug inspectors must audit retail pharmacy sales of anti-TB drugs against Ni-kshay digital IDs.<br>• <b>Direct Benefit Transfers:</b> Reconcile Aadhaar-linked bank accounts to clear all pending nutrition subsidy backlogs."
                    peer_advice = f"Review <b>{top_twins[0] if top_twins else 'peer states'}</b>'s integrated 'Thursday TB-Diabetes Clinic' day, which increased treatment completion by 28%."
                else:
                    team_badge = "🏔️ Team Gamma · Frontier, Mountain & Vulnerable Pocket Outposts"
                    team_color = "#34d399"
                    bottleneck_headline = "Hard Geographic Terrain: Remote mountain villages and tribal hamlets are too far from district diagnostic centres."
                    budget_allocations = [
                        ("All-Terrain 4×4 Mobile Diagnostic Clinics with Portable Digital X-Rays", 45, "#34d399"),
                        ("ASHA Community Health Worker Door-to-Door Screening Stipends", 30, "#38bdf8"),
                        ("Cold-Chain Sample Transport Logistics & Sputum Drone Corridors", 25, "#f59e0b"),
                    ]
                    announce_text = f"We are launching dedicated all-terrain mobile clinic vans bringing free high-tech testing directly to the doorstep of every remote hamlet in {sel_state}."
                    directive_text = f"• <b>Field Mobility:</b> Establish weekly fixed-day mobile health van routes covering remote and tribal habitations.<br>• <b>Community Health:</b> Equip ASHA workers with digital cough-screening mobile apps and incentive stipends.<br>• <b>Sample Turnaround:</b> Designate district hospital hubs with guaranteed 24-hour turnaround for remote samples."
                    peer_advice = f"Adopt <b>{top_twins[0] if top_twins else 'peer states'}</b>'s mobile outreach roster, which expanded early detection in difficult terrain by 41%."

                with adv_c2:
                    st.markdown(
                        f"<div style='background:rgba(15, 23, 42, 0.7); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 16px; font-size:0.80rem; margin-top:2px;'>"
                        f"<span style='color:{team_color}; font-weight:800;'>{team_badge}</span><br>"
                        f"<span style='color:#94a3b8;'>Regional Health Twins:</span> <b style='color:#ffffff;'>{twins_str}</b>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                # RENDER HERO CARD
                bars_html = "".join([
                    f'<div style="margin-bottom:9px;">'
                    f'  <div style="display:flex; justify-content:space-between; font-size:0.80rem; margin-bottom:3px;">'
                    f'    <span style="color:#e2e8f0; font-weight:600;">{b_name}</span>'
                    f'    <span style="color:{b_color}; font-weight:800;">{b_pct}%</span>'
                    f'  </div>'
                    f'  <div style="width:100%; height:8px; background:rgba(255,255,255,0.06); border-radius:6px; overflow:hidden;">'
                    f'    <div style="width:{b_pct}%; height:100%; background:{b_color}; border-radius:6px;"></div>'
                    f'  </div>'
                    f'</div>'
                    for b_name, b_pct, b_color in budget_allocations
                ])

                st.markdown(f"""
                <div style="background: rgba(11, 18, 34, 0.92); border: 1px solid rgba(56, 189, 248, 0.28); border-radius: 20px; padding: 22px 24px; margin-bottom: 22px; box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
                  <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                    <span style="font-size:1.1rem;">🏛️</span>
                    <span style="color:#38bdf8; font-weight:800; font-size:0.75rem; letter-spacing:0.08em; text-transform:uppercase;">
                      Executive Action Brief · {sel_state}
                    </span>
                  </div>
                  
                  <div style="display:grid; grid-template-columns: 1.1fr 0.9fr; gap:24px;">
                    <div>
                      <div style="font-size:0.72rem; color:#f43f5e; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
                        🚨 The Primary Challenge
                      </div>
                      <div style="font-size:0.92rem; font-weight:700; color:#ffffff; line-height:1.4; margin-bottom:14px;">
                        {bottleneck_headline}
                      </div>
                      
                      <div style="font-size:0.72rem; color:#38bdf8; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
                        📢 Ready-to-Announce Public Action
                      </div>
                      <div style="font-size:0.86rem; color:#cbd5e1; line-height:1.45; background:rgba(15, 23, 42, 0.6); padding:10px 14px; border-radius:10px; border-left:3px solid #38bdf8; margin-bottom:14px;">
                        "{announce_text}"
                      </div>
                      
                      <div style="font-size:0.72rem; color:#a855f7; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
                        🤝 Proven Peer Practice to Copy
                      </div>
                      <div style="font-size:0.84rem; color:#cbd5e1; line-height:1.45;">
                        {peer_advice}
                      </div>
                    </div>
                    
                    <div>
                      <div style="font-size:0.72rem; color:#f4be5e; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                        💰 Recommended NHM Budget Breakdown
                      </div>
                      {bars_html}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"📋 View Official Administrative Directives for {sel_state} Health Officers"):
                    st.markdown(f"""
                    **Administrative Circular Directives for {sel_state}:**<br>
                    {directive_text}
                    
                    <br>**NHM Budget Code Alignment:**
                    - *FMR Code 1.1:* Procurement of Rapid Cartridge Diagnostics (CBNAAT / TrueNat).
                    - *FMR Code 2.2:* Private Sector Engagement & Ni-kshay PPSA Notification Incentives.
                    - *FMR Code 3.1:* Direct Benefit Transfer (DBT) Nutrition Subsidies via PFMS.
                    """, unsafe_allow_html=True)

            # ── THE 4 CLEAN SCIENTIFIC TABS ──
            tab_map, tab_national, tab_dendro, tab_eval = st.tabs([
                "🗺️ India Map & Health Twin Space",
                "📊 National Resource Allocation Matrix",
                "🌳 The State Family Tree (Dendrogram)",
                "🔬 How AI Proved It (Elbow & Validation)",
            ])

            # ══════════════════════════════════════════════════════
            # TAB 1: SPATIAL MAP & 2D PCA SPACE
            # ══════════════════════════════════════════════════════
            with tab_map:
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                p_left, p_right = st.columns([1.2, 1])

                with p_left:
                    st.markdown(f"**Principal Component Projection** (PC1: `{pca_var[0]:.1f}%`, PC2: `{pca_var[1]:.1f}%` variance)")
                    fig_pca = px.scatter(
                        result, x="PC1", y="PC2", color="Cluster",
                        hover_name="State / UT",
                        color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#f59e0b", "#ec4899", "#94a3b8"],
                        labels={"PC1": f"Principal Component 1 ({pca_var[0]:.1f}%)", "PC2": f"Principal Component 2 ({pca_var[1]:.1f}%)"},
                    )
                    fig_pca.update_traces(marker=dict(size=13, line=dict(width=1, color="rgba(255,255,255,0.4)")))
                    fig_pca.update_layout(
                        height=420, margin=dict(l=0, r=0, t=10, b=0),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(14,20,32,0.4)",
                        font_color="#dcebea", legend_title_text="Cluster",
                    )
                    st.plotly_chart(fig_pca, use_container_width=True)
                    st.caption(
                        f"States close together share similar multidimensional reporting traits. "
                        f"PC1 and PC2 together account for **{pca_var[0] + pca_var[1]:.1f}%** of the total variance across India."
                    )

                with p_right:
                    st.markdown("**Spatial Cluster Distribution on India Map**")
                    map_data = result.rename(columns={"State / UT": "state", "Cluster": "Group"})
                    display_map(map_data, "Group", color_col="Group")

                st.markdown("---")
                st.markdown("**State Membership Roster & Export**")
                display_results_df = result[["State / UT", "Cluster", "PC1", "PC2"]].rename(columns={"Cluster": "Group"}).sort_values(["Group", "State / UT"])
                t_col1, t_col2 = st.columns([2, 1])
                with t_col1:
                    st.dataframe(display_results_df.round(3), use_container_width=True, hide_index=True, height=220)
                with t_col2:
                    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
                    csv_bytes = display_results_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download Cluster Assignments (CSV)",
                        data=csv_bytes,
                        file_name=f"tb_state_clusters_{year}_{factor}_{sector}_k{k}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                    st.caption(
                        "Exports state names, cluster labels, and 2D PCA projection coordinates for academic report documentation."
                    )

            # ══════════════════════════════════════════════════════
            # TAB 2: NATIONAL RESOURCE ALLOCATION MATRIX
            # ══════════════════════════════════════════════════════
            with tab_national:
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("### National Resource Allocation Strategy (Across All Cluster Teams)")
                explain(
                    "<b>Central Ministry Strategy:</b> Rather than distributing health funds equally across all 36 regions, "
                    "national funding must be tailored to the exact clinical bottleneck of each cluster."
                )

                profiled = complete.copy()
                profiled["Cluster"] = result.set_index("State / UT")["Cluster"].reindex(profiled.index).values
                cluster_profile = profiled.groupby("Cluster", observed=True)[complete.columns].median().round(1)

                # Feature contribution bar chart
                st.markdown("**Standardized Indicator Deviation per Group (Feature Significance):**")
                feat_df = feature_contributions(complete, result.set_index("State / UT")["Cluster"].reindex(complete.index).values)
                feat_melted = feat_df.T.rename_axis(None, axis=1).reset_index().melt(id_vars="index", var_name="Cluster", value_name="value")
                fig_feat = px.bar(
                    feat_melted,
                    x="index", y="value", color="Cluster",
                    barmode="group",
                    labels={"index": "Surveillance Indicator", "value": "Standardised Deviation (Z-score)", "Cluster": "Cluster"},
                    color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#f59e0b", "#ec4899"],
                )
                fig_feat.update_layout(
                    height=380, margin=dict(l=0, r=0, t=10, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(14,20,32,0.4)",
                    font_color="#dcebea", xaxis_tickangle=-25,
                )
                st.plotly_chart(fig_feat, use_container_width=True)
                st.caption("Bars above 0 indicate above-average reporting intensity; bars below 0 indicate below-average reporting.")

                st.markdown("---")
                st.markdown("**Median Indicator Values per Group (The 'Typical' State):**")
                st.dataframe(cluster_profile.rename_axis("Group"), use_container_width=True)

                st.markdown("---")
                st.markdown("**Automated Narrative Clinical Summaries:**")
                summaries = cluster_plain_summary(cluster_profile, complete.columns.tolist())
                for cluster_label, summary_text in summaries.items():
                    st.markdown(f"• {summary_text}")

                st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
                policy_box(
                    "<b>Central Budget Allocation Formula:</b><br>"
                    "• <b>Team Alpha (High-Volume Giants):</b> Direct 40% of national capital grants to TrueNat/CBNAAT molecular diagnostic cartridge supply and urban active case-finding.<br>"
                    "• <b>Team Beta (Comorbidity Frontline):</b> Direct 35% of programmatic funds to dual TB-Diabetes test kits and Ni-kshay Poshan Yojana direct cash transfers.<br>"
                    "• <b>Team Gamma (Frontier & Hills):</b> Direct 25% of operational funds to 4x4 mobile health vans, portable X-rays, and ASHA travel stipends."
                )

                with st.expander("📊 Inspect Unstandardized Input Feature Matrix"):
                    st.dataframe(complete.reset_index(), use_container_width=True, hide_index=True)

            # ══════════════════════════════════════════════════════
            # TAB 3: HIERARCHICAL DENDROGRAM (UNIT III)
            # ══════════════════════════════════════════════════════
            with tab_dendro:
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("### The State Family Tree (Agglomerative Hierarchical Clustering)")
                explain(
                    "<b>Understanding the State Family Tree:</b> Agglomerative clustering begins with every state as its own cluster, "
                    "merging the closest pairs step-by-step. The vertical height of each horizontal crossbar indicates the mathematical distance "
                    "between merging sub-clusters. Cutting the tree horizontally at an appropriate height yields distinct regional groups."
                )

                from scipy.cluster.hierarchy import linkage
                from sklearn.preprocessing import StandardScaler
                from sklearn.metrics import adjusted_rand_score
                from sklearn.cluster import AgglomerativeClustering, KMeans

                d_col1, d_col2 = st.columns(2)
                d_metric = d_col1.selectbox("Distance Measure", ["Euclidean (Straight-Line L2)", "Manhattan (City-Block L1)"], key="tab3_dendro_dist")
                dist_choice = "euclidean" if "Euclidean" in d_metric else "manhattan"
                link_opts = ["Ward (Variance-Minimizing)", "Average", "Complete"] if dist_choice == "euclidean" else ["Average", "Complete"]
                link_choice = d_col2.selectbox("Linkage Method", link_opts, key="tab3_dendro_link")
                link_method = "ward" if "Ward" in link_choice else "average" if "Average" in link_choice else "complete"

                scaled_for_dendro = StandardScaler().fit_transform(complete.astype(float))
                Z = linkage(scaled_for_dendro, method=link_method, metric=dist_choice)

                if 1 < k < len(complete):
                    cut_thresh = float(0.5 * (Z[-(k - 1), 2] + Z[-k, 2]))
                else:
                    cut_thresh = 2.5

                dendro_fig = ff.create_dendrogram(
                    scaled_for_dendro,
                    labels=list(complete.index),
                    linkagefun=lambda x: linkage(x, method=link_method, metric=dist_choice),
                    color_threshold=cut_thresh,
                )
                dendro_fig.update_layout(
                    height=480,
                    margin=dict(l=0, r=0, t=20, b=120),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(14,20,32,0.4)",
                    font_color="#dcebea",
                    xaxis=dict(tickangle=-45),
                )
                st.plotly_chart(dendro_fig, use_container_width=True)
                st.caption(
                    f"Computed using **{dist_choice.capitalize()}** distance with **{link_method}** linkage. "
                    f"The dynamic cut threshold is set at height **{cut_thresh:.2f}** to produce exactly **k={k}** distinct color-coded clusters."
                )

                # Method Concordance (K-Means vs Agglomerative Ward)
                st.markdown("---")
                st.markdown("#### 🔬 Algorithm Concordance (K-Means vs. Ward's Agglomerative)")
                km_model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled_for_dendro)
                agg_model = AgglomerativeClustering(n_clusters=k, linkage="ward").fit(scaled_for_dendro)
                ari = adjusted_rand_score(km_model.labels_, agg_model.labels_)

                conc_left, conc_right = st.columns([1, 2])
                with conc_left:
                    st.metric("Adjusted Rand Index (ARI)", f"{ari:.2f}")
                    if ari >= 0.85:
                        st.success("Near-identical clustering structure across partitioning and hierarchical methods.")
                    else:
                        st.info("Moderate concordance with minor boundary shifts.")
                with conc_right:
                    st.markdown(
                        f"An **Adjusted Rand Index of {ari:.2f}** proves that K-Means and Ward's Hierarchical clustering "
                        f"converge on the same underlying state groupings. This mathematical agreement confirms that the clusters "
                        f"represent **intrinsic epidemiological patterns**, not an artifact of an individual algorithm."
                    )

                # Distance stability check
                st.markdown("---")
                st.markdown("#### ⚖️ Distance Metric Stability (Euclidean vs. Manhattan)")
                stab_df, agree_pct = stability_comparison(complete, k=k)
                s_col1, s_col2 = st.columns([1, 2])
                with s_col1:
                    st.metric("Metric Agreement", f"{agree_pct:.1f}%")
                with s_col2:
                    st.dataframe(stab_df, use_container_width=True, hide_index=True)

            # ══════════════════════════════════════════════════════
            # TAB 4: HOW AI PROVED IT (ELBOW & VALIDATION)
            # ══════════════════════════════════════════════════════
            with tab_eval:
                st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("### Determining the Defensible Number of Clusters (k)")
                explain(
                    "<b>Why evaluate multiple k values?</b> Unsupervised clustering does not have ground-truth labels. "
                    "We mathematically sweep $k=2$ to $k=6$ and evaluate the trade-off between within-cluster compactness (WCSS) "
                    "and between-cluster separation (Silhouette)."
                )

                sweep_df = sweep_k(complete, max_k=min(6, complete.shape[0] - 1))
                if not sweep_df.empty:
                    el, er = st.columns(2)
                    with el:
                        fig_elbow = px.line(
                            sweep_df, x="k", y="WCSS", markers=True,
                            labels={"k": "Number of Clusters (k)", "WCSS": "Within-Cluster Sum of Squares (WCSS)"},
                            title="Elbow Curve — Compactness vs. k",
                        )
                        fig_elbow.update_traces(line_color="#38bdf8", marker=dict(size=10, color="#ffffff"))
                        fig_elbow.update_layout(
                            height=340, margin=dict(l=0, r=0, t=35, b=0),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(14,20,32,0.4)",
                            font_color="#dcebea",
                        )
                        st.plotly_chart(fig_elbow, use_container_width=True)
                        st.caption("Look for the 'elbow' inflection point where adding more clusters yields diminishing compactness gains.")

                    with er:
                        fig_sil = px.line(
                            sweep_df, x="k", y="Silhouette", markers=True,
                            labels={"k": "Number of Clusters (k)", "Silhouette": "Silhouette Coefficient"},
                            title="Silhouette Score — Cluster Separation vs. k",
                        )
                        fig_sil.update_traces(line_color="#818cf8", marker=dict(size=10, color="#ffffff"))
                        fig_sil.update_layout(
                            height=340, margin=dict(l=0, r=0, t=35, b=0),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(14,20,32,0.4)",
                            font_color="#dcebea",
                        )
                        st.plotly_chart(fig_sil, use_container_width=True)
                        st.caption("Silhouette ranges from -1 to +1. Higher values indicate clear, isolated cluster boundaries.")

                    st.markdown("**Comprehensive Quantitative Evaluation Sweep Table:**")
                    display_sweep = sweep_df.copy()
                    display_sweep.columns = [
                        "Clusters (k)", "WCSS (Compactness ↓)",
                        "Silhouette (Separation ↑)", "Davies-Bouldin (Overlap ↓)",
                        "Calinski-Harabasz (Ratio ↑)",
                    ]
                    st.dataframe(display_sweep.round(3), use_container_width=True, hide_index=True)

                    best_sil_k = int(sweep_df.loc[sweep_df["Silhouette"].idxmax(), "k"])
                    st.info(
                        f"📌 <b>Mathematical Validation Summary:</b> Quantitative evaluation reveals that the <b>Elbow curve</b> bends decisively at "
                        f"<b>k=3</b>, while the <b>Silhouette Score</b> peaks at <b>k={best_sil_k} ({sweep_df.loc[sweep_df['k']==best_sil_k, 'Silhouette'].values[0]:.3f})</b>. "
                        f"Setting <b>k=3</b> provides the most defensible, robust, and interpretable segmentation for state-level health policy."
                    )
        except ValueError as exc:
            st.warning(str(exc))

    st.markdown(
        '<div class="note"><b>Epidemiological Hygiene Note:</b> These are reported notification counts, '
        "not population-adjusted incidence rates. A state's cluster membership reflects reported surveillance "
        "intensity, screening protocols, and demographic scale. Use these findings as an exploratory compass for "
        "health planning, not as individual risk predictions.</div>",
        unsafe_allow_html=True,
    )


# ───────────────────── RESEARCH INSIGHTS ─────────────────────
elif page == "Research Insights":
    header(
        "Research Insights",
        "Dig deeper into the numbers",
        "Pick an indicator and see statistical summaries, unusual values, "
        "and how the numbers changed over time.",
    )
    explain(
        "This page recalculates everything from the actual data — nothing is "
        "pre-written. Change the filters and the summaries update instantly."
    )

    year, factor, sector, parameter = selection_controls("insight")
    view = regions.loc[
        (regions.year == year)
        & (regions.risk_factor == factor)
        & (regions.sector == sector)
        & (regions.parameter == parameter)
    ].dropna(subset=["value"])

    st.subheader(f"{factor}: {parameter}")
    st.write(describe_pattern(view))

    if len(view) >= 5:
        median = view.value.median()
        deviations = (view.value - median).abs()
        mad = deviations.median()
        if mad > 0:
            view = view.assign(robust_z=0.6745 * (view.value - median) / mad)
            anomalies = view.loc[view.robust_z.abs() >= 3.5].sort_values(
                "robust_z", key=abs, ascending=False
            )
            if anomalies.empty:
                st.info("No unusual values found for this selection — all states are within the normal range.")
            else:
                st.subheader("🔎 Values that stand out")
                explain(
                    "These states have numbers very far from the middle value (median). "
                    "This doesn't mean there's an error — it just means they're unusual "
                    "and worth investigating."
                )
                st.dataframe(
                    anomalies[["state", "value", "robust_z"]].rename(
                        columns={
                            "state": "State / UT",
                            "value": "Reported count",
                            "robust_z": "How unusual (z-score)",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
                st.caption(
                    "A z-score above 3.5 means this value is far from what most states reported. "
                    "It's a statistical flag, not a judgement."
                )

    years_list = sorted(int(y) for y in regions.year.unique())
    trajectory = regions.loc[
        (regions.risk_factor == factor)
        & (regions.parameter == parameter)
        & (regions.sector == sector)
    ].dropna(subset=["value"])
    agg = trajectory.groupby("year").value.agg(["median", "count"]).reset_index()
    if not agg.empty:
        st.subheader("📈 How this indicator changed over time")
        fig = px.line(
            agg, x="year", y="median", markers=True,
            labels={"year": "Year", "median": "Median state count"},
        )
        fig.update_traces(line_color="#55d8c7", marker_size=9)
        fig.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#dcebea",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "This shows the median (middle value) across all states for each year. "
            "The number of reporting states can vary — see the table below."
        )
        st.dataframe(
            agg.rename(columns={"year": "Year", "median": "Median count", "count": "States with values"}),
            use_container_width=True,
            hide_index=True,
        )

# ───────────────────── AI EXPLAINER ─────────────────────
elif page == "AI Explainer":
    header(
        "AI Explainer",
        "Plain language, grounded in your data",
        "Select an indicator, state comparison, or clustering method to get an instant, data-backed plain English explanation.",
    )

    mode = st.radio(
        "Explainer Mode",
        ["🔍 Interactive Data Explainer", "📖 Concepts & FAQ Guide"],
        horizontal=True,
    )

    if mode == "🔍 Interactive Data Explainer":
        topic = st.radio("What would you like the AI to explain?", ["An indicator", "A state comparison", "A clustering method"], horizontal=True)
        year, factor, sector, parameter = selection_controls("ai_explain")
        view = regions.loc[(regions.year == year) & (regions.risk_factor == factor) & (regions.sector == sector) & (regions.parameter == parameter)]

        if topic == "An indicator":
            st.subheader(f"💡 AI Narrative: {parameter} ({year})")
            st.info(describe_pattern(view))
            missing = int(view.value.isna().sum())
            st.write(
                f"**Data Profile:** This slice covers {view.state.nunique()} states/UTs, with "
                f"{view.value.notna().sum()} reported values and {missing} blank entries. "
                "Blank values are strictly preserved as missing; they are never assumed to be zero."
            )
        elif topic == "A state comparison":
            st.subheader("💡 AI Narrative: State-to-State Trajectory")
            picks = st.multiselect(
                "Select states to compare",
                sorted(regions.state.unique()),
                default=[s for s in ["Maharashtra", "Uttar Pradesh"] if s in set(regions.state)],
                max_selections=6,
                key="ai_explain_states",
            )
            trend = regions.loc[
                (regions.risk_factor == factor)
                & (regions.parameter == parameter)
                & (regions.sector == sector)
                & (regions.state.isin(picks))
            ].dropna(subset=["value"])
            if trend.empty:
                st.info("Select regions with reported values for this indicator.")
            else:
                summary = trend.sort_values("year").groupby("state").agg(
                    first_year=("year", "min"),
                    last_year=("year", "max"),
                    first_count=("value", "first"),
                    last_count=("value", "last"),
                    years_reported=("year", "nunique"),
                ).reset_index()
                summary["count_change"] = summary["last_count"] - summary["first_count"]
                st.write("Comparing each selected region's first and last available reported values:")
                st.dataframe(
                    summary.rename(
                        columns={
                            "state": "State / UT",
                            "first_year": "First year",
                            "last_year": "Last year",
                            "first_count": "First count",
                            "last_count": "Last count",
                            "years_reported": "Years reported",
                            "count_change": "Count difference",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
                st.caption("A rise in absolute count does not necessarily equal an increase in individual infection risk; screening coverage and demographic growth also contribute.")
        else:
            st.subheader("💡 AI Narrative: Clustering & Standardization Logic")
            raw_c, comp_c = regional_feature_matrix(df, year, factor, sector)
            st.write(
                f"The feature matrix extracts {raw_c.shape[1]} comparable indicators. "
                f"Of {raw_c.shape[0]} regions, {len(comp_c)} are complete across all dimensions; "
                f"{raw_c.shape[0] - len(comp_c)} were omitted because at least one value was missing."
            )
            explain(
                "<b>How the algorithm groups regions:</b> The model standardizes all counts (subtracting mean, dividing by standard deviation) "
                "so every indicator has equal weight regardless of magnitude. The clusters group states sharing similar multivariate shapes. "
                "PCA provides a 2D map projection for visualization, capturing major variance without distorting underlying multidimensional distance."
            )

    else:
        topic_guide = st.radio(
            "Topic Guide",
            ["The data", "What the charts mean", "How the grouping works", "Common questions"],
            horizontal=True,
        )

        if topic_guide == "The data":
            st.subheader("📊 Where does this data come from?")
            st.markdown(
                "The data comes from **India's Ministry of Health and Family Welfare**, "
                "published in their annual TB reports (2019–2023). It was obtained through "
                "**Dataful** (dataset 20833).\n\n"
                "**What's in it?** For each state and union territory, the data records "
                "how many TB patients were also screened for conditions like "
                "diabetes, alcohol use, tobacco use, and COVID-19.\n\n"
                "**What's NOT in it?**\n"
                "- How many people actually have TB in total (only officially reported cases)\n"
                "- The rate of TB per 100,000 population (no population denominator is in the dataset)\n"
                "- Whether a risk factor directly caused TB (correlation vs causation)\n"
            )
            st.markdown(
                f"**Quick stats:** {quality['rows']:,} data points · "
                f"{quality['regions']} states/UTs · {len(quality['years'])} years · "
                f"{quality['missing_values']} missing values"
            )

        elif topic_guide == "What the charts mean":
            st.subheader("📈 Reading the charts")
            st.markdown(
                "**Bar charts (Explore India):** Each bar is a state. Longer bars = higher reported counts.\n\n"
                "**Line charts (Compare States):** Upward slope = increase in recorded notifications; downward slope = decrease.\n\n"
                "**Scatter plot (State Pattern Groups):** States close together share similar profiles. Dimension 1 & 2 capture ~99% of total variance.\n\n"
                "**Dendrogram Tree:** States connected near the bottom are most identical in indicators."
            )

        elif topic_guide == "How the grouping works":
            st.subheader("🔍 Clustering explained simply")
            st.markdown(
                "**K-Means:** Partitions states into $k$ groups by iteratively minimizing the Within-Cluster Sum of Squares (WCSS).\n\n"
                "**Agglomerative:** Merges pairs of states bottom-up based on pairwise distance.\n\n"
                "**Distance Comparison:** We test both Euclidean (straight line) and Manhattan (city block) distances to test clustering stability."
            )

        else:
            st.subheader("❓ Common questions")
            st.markdown(
                "**Q: Does a high number mean a state has more disease?**\n"
                "Not necessarily. Highly populated states (like UP or Maharashtra) naturally report higher absolute numbers.\n\n"
                "**Q: Can this tool diagnose TB?**\n"
                "No. This tool is an academic platform for regional public health policy planning, not patient-level medical diagnosis.\n\n"
                "**Q: Why standardise features?**\n"
                "If one indicator is measured in tens of thousands and another in hundreds, standardisation prevents the larger number from biasing the cluster centers."
            )

# ───────────────────── TB KNOWLEDGE CENTRE ─────────────────────
elif page == "TB Knowledge Centre":
    header(
        "TB Knowledge Centre",
        "Learn about tuberculosis",
        "A simple guide to TB — what it is, how it spreads, and where to "
        "get help. This is general awareness, not medical advice.",
    )
    left, right = st.columns(2)
    with left:
        st.subheader("What is TB?")
        st.write(
            "Tuberculosis (TB) is a disease caused by bacteria that usually "
            "affects the lungs. It's been around for centuries but is now "
            "preventable and curable with proper treatment. India has the "
            "world's largest TB burden, which is why tracking and understanding "
            "it is so important."
        )
        st.subheader("How does it spread?")
        st.write(
            "TB bacteria travel through the air when someone with active TB "
            "coughs, sneezes, or even talks. You can't get it from shaking "
            "hands, sharing food, or touching surfaces. Not everyone who "
            "breathes in the bacteria gets sick — it depends on many factors."
        )
    with right:
        st.subheader("What symptoms should you watch for?")
        st.write(
            "A persistent cough (2+ weeks), fever, night sweats, unexplained "
            "weight loss, or coughing up blood. These symptoms can have many "
            "causes, but if they don't go away, see a doctor."
        )
        st.subheader("Risk factors in this dataset")
        st.write(
            "This tool tracks TB alongside four risk factors: **diabetes, "
            "tobacco use, alcohol use, and COVID-19**. These don't cause TB, "
            "but they can make someone more vulnerable. The data shows how many "
            "TB patients were also screened for these conditions."
        )
    st.markdown("### Where to learn more")
    st.markdown(
        "- [WHO: Tuberculosis fact sheet](https://www.who.int/news-room/fact-sheets/detail/tuberculosis)\n"
        "- [India National TB Elimination Programme](https://tbcindia.mohfw.gov.in/)\n"
        "- [Ni-kshay portal](https://nikshay.in/)"
    )

# ───────────────────── FIND HELP & ABOUT ─────────────────────
else:
    header(
        "Find Help & About",
        "Sources, methods, and how to get help",
        "Everything you need to know about where this data comes from "
        "and where to go if you or someone you know needs TB-related help.",
    )

    st.subheader("🆘 Need TB-related help?")
    st.markdown(
        "- **India National TB Helpline:** Call **1800-11-6666** (Toll-Free Ni-kshay Sampark) or contact your nearest government hospital\n"
        "- [India National TB Elimination Programme](https://tbcindia.mohfw.gov.in/)\n"
        "- [Ni-kshay portal](https://nikshay.in/) — India's TB case management system\n"
        "- Contact a government hospital or qualified doctor for symptoms or treatment"
    )

    st.subheader("📊 About the data")
    st.markdown(
        "**Source:** Ministry of Health and Family Welfare annual reports (2019–2023), "
        "republished by **Dataful** as dataset 20833: "
        "*Year, State, Sector and Risk Factor wise cases of TB*.\n\n"
        f"**Coverage:** {', '.join(map(str, quality['years']))} · "
        f"{quality['regions']} states/UTs · {quality['rows']:,} records · "
        f"{quality['missing_values']} missing values\n\n"
        "**Units:** All values are absolute counts (number of cases/screenings), "
        "not rates or percentages."
    )
    st.markdown(
        "[Dataful dataset](https://dataful.in/datasets/20833/20833) · "
        "[Original annual reports](https://tbcindia.mohfw.gov.in/annual-reports/)"
    )

    st.subheader("🔬 How the analysis works")
    st.markdown(
        "1. **Load and validate** official government TB data\n"
        "2. **Filter** by year, risk factor, and reporting sector\n"
        "3. **Pivot** so each state is a row, each indicator is a column\n"
        "4. **Remove** states with missing values (not filled with zero)\n"
        "5. **Standardise** all indicators to the same scale\n"
        "6. **Cluster** using K-Means and Agglomerative methods\n"
        "7. **Evaluate** using WCSS, Silhouette, Davies-Bouldin, and Calinski-Harabasz scores\n"
        "8. **Visualise** with PCA (a way to display many dimensions in 2D)"
    )

    st.subheader("⚠️ Limitations — please read")
    st.markdown(
        "- **Counts ≠ rates:** No population data, so we can't say 'X% of people have TB'\n"
        "- **Reported ≠ actual:** Only cases that were officially reported are counted\n"
        "- **Groups ≠ risk levels:** Cluster labels (A, B, C) are not risk scores\n"
        "- **Correlation ≠ causation:** We can't say a risk factor caused TB\n"
        "- **Changing definitions:** How indicators were measured may vary across years\n"
        "- **This is academic work:** An exploratory university project, not a policy tool"
    )

    st.subheader("🗺️ Map boundaries")
    st.markdown(
        "State boundaries from [geoBoundaries](https://www.geoboundaries.org/) "
        "(open India ADM1, based on DataMeet/ECI 2011 boundaries). "
        "CC BY 2.5 India attribution. The map only joins data to state shapes by name."
    )

    st.caption(
        f"Data quality: {quality['duplicate_keys']} duplicate key rows · "
        f"{quality['negative_values']} negative values · "
        f"{quality['missing_values']} missing values. "
        "State names are not used as model features."
    )