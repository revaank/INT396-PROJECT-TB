import json
import re
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_rich_overcome import states_data

# Extract India SVG map from preview.html
preview_html = Path("preview.html").read_text(encoding="utf-8")
svg_match = re.search(r'(<svg class="india-map".*?</svg>)', preview_html, re.DOTALL)
assert svg_match, "Failed to find SVG map in preview.html"
svg_map_html = svg_match.group(1).replace('class="state-shape selected"', 'class="state-shape"')

states_json = json.dumps(states_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AeroTB | Road to Overcome — Executive Public Health Dossier</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-deep: #07080c;
      --bg-card: rgba(13, 19, 32, 0.78);
      --border-card: rgba(255, 255, 255, 0.07);
      --border-glow: rgba(56, 189, 248, 0.35);
      --cyan: #38bdf8;
      --gold: #f4be5e;
      --emerald: #10b981;
      --rose: #f43f5e;
      --purple: #a855f7;
      --indigo: #818cf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: var(--bg-deep);
      background-image: 
        radial-gradient(ellipse 90% 65% at 50% -12%, rgba(56, 189, 248, 0.12) 0%, rgba(18, 23, 34, 0.4) 50%, transparent 90%),
        radial-gradient(circle at 85% 90%, rgba(244, 190, 94, 0.06) 0%, transparent 60%);
      background-attachment: fixed;
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      padding-top: 75px;
      padding-bottom: 40px;
    }}

    /* ── FLOATING TOP NAVIGATION BAR ── */
    .top-header {{
      position: fixed;
      top: 12px;
      left: 24px;
      right: 24px;
      z-index: 1000;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(11, 16, 26, 0.92);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--border-card);
      border-radius: 9999px;
      padding: 7px 18px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }}
    .brand-bar {{
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
    }}
    .brand-logo {{
      width: 22px;
      height: 22px;
      border-radius: 6px;
      background: linear-gradient(135deg, var(--cyan), #4facfe);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      color: #050811;
      font-weight: 800;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }}
    .brand-name {{
      font-size: 0.92rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
    }}
    .brand-sub {{
      font-size: 0.62rem;
      color: #64748b;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    /* NAVIGATION PILLS */
    .nav-pill-group {{
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.65);
      padding: 3px 6px;
      border-radius: 9999px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }}
    .nav-pill {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 9999px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}
    .nav-pill:hover {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.08);
    }}
    .nav-pill.active {{
      background: rgba(244, 190, 94, 0.16);
      color: var(--gold);
      border: 1px solid rgba(244, 190, 94, 0.35);
      box-shadow: 0 0 14px rgba(244, 190, 94, 0.2);
    }}
    .provenance-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.70rem;
      color: var(--emerald);
      font-weight: 700;
    }}
    .pulse-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 8px var(--emerald);
      animation: blink 2s infinite ease-in-out;
    }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}

    /* ── PAGE LAYOUT ── */
    .container {{
      max-width: 1520px;
      margin: 0 auto;
      padding: 10px 20px;
    }}

    /* ── TWO-COLUMN WORKSPACE ── */
    .dashboard-grid {{
      display: grid;
      grid-template-columns: 430px 1fr;
      gap: 20px;
      align-items: start;
    }}

    /* ── LEFT PANE: STICKY MAP & SELECTOR ── */
    .left-pane {{
      background: var(--bg-card);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--border-card);
      border-radius: 20px;
      padding: 16px 18px;
      box-shadow: 0 16px 40px rgba(0,0,0,0.5);
      position: sticky;
      top: 80px;
    }}
    .selector-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.70rem;
      font-weight: 800;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }}
    .state-dropdown {{
      width: 100%;
      background: rgba(9, 13, 24, 0.95);
      border: 1px solid rgba(56, 189, 248, 0.40);
      color: #ffffff;
      font-family: inherit;
      font-size: 1rem;
      font-weight: 800;
      padding: 10px 14px;
      border-radius: 12px;
      cursor: pointer;
      outline: none;
      transition: all 0.2s ease;
      box-shadow: 0 4px 18px rgba(0,0,0,0.4);
      margin-bottom: 10px;
    }}
    .state-dropdown:focus {{
      border-color: var(--cyan);
      box-shadow: 0 0 18px rgba(56, 189, 248, 0.4);
    }}

    /* FILTER BUTTONS */
    .filter-pills {{
      display: flex;
      gap: 5px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}
    .filter-pill {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.07);
      color: var(--text-muted);
      font-size: 0.68rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .filter-pill:hover {{
      color: #ffffff;
      background: rgba(255, 255, 255, 0.08);
    }}
    .filter-pill.active {{
      background: rgba(56, 189, 248, 0.16);
      color: var(--cyan);
      border-color: rgba(56, 189, 248, 0.4);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
    }}

    /* MAP CONTAINER */
    .map-box {{
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      background: rgba(6, 10, 18, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 16px;
      padding: 8px;
    }}
    .india-map {{
      width: 100%;
      height: auto;
      max-height: 440px;
      display: block;
    }}
    .state-shape {{
      fill: #151d2f;
      stroke: #0a0d14;
      stroke-width: 0.8;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .state-shape:hover {{
      fill: #223755 !important;
      stroke: var(--cyan) !important;
      stroke-width: 1.5 !important;
    }}
    .state-shape[data-cluster-team="alpha"] {{
      fill: #1a324a;
    }}
    .state-shape[data-cluster-team="beta"] {{
      fill: #3a2e1d;
    }}
    .state-shape[data-cluster-team="gamma"] {{
      fill: #15382b;
    }}
    .state-shape.active-state {{
      stroke: #ffffff !important;
      stroke-width: 2.8 !important;
      fill: #38bdf8 !important;
      filter: drop-shadow(0 0 18px rgba(56, 189, 248, 0.95)) !important;
    }}
    .map-caption {{
      text-align: center;
      font-size: 0.66rem;
      color: #64748b;
      font-weight: 600;
      margin-top: 8px;
    }}

    /* ── RIGHT PANE: ULTRA-CLEAN BENTO GRID ── */
    .right-pane {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    /* EXECUTIVE HEADER BAR (COMPACT & SLEEK) */
    .state-exec-bar {{
      background: var(--bg-card);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--border-card);
      border-radius: 18px;
      padding: 14px 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.45);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .exec-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .exec-state-name {{
      font-size: 1.5rem;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
    }}
    .exec-team-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 4px 12px;
      border-radius: 9999px;
      background: rgba(56, 189, 248, 0.12);
      color: var(--cyan);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .exec-kpi-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .exec-kpi-pill {{
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
      padding: 6px 12px;
      display: flex;
      flex-direction: column;
    }}
    .exec-kpi-lbl {{
      font-size: 0.60rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .exec-kpi-val {{
      font-size: 0.95rem;
      font-weight: 800;
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* ── BENTO GRID ── */
    .bento-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    .bento-full {{
      grid-column: span 2;
    }}

    /* CLEAN BENTO CARD */
    .bento-card {{
      background: var(--bg-card);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--border-card);
      border-radius: 18px;
      padding: 18px 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.45);
      position: relative;
      display: flex;
      flex-direction: column;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .bento-card:hover {{
      border-color: rgba(56, 189, 248, 0.25);
    }}

    .card-kicker {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }}
    .kicker-rose {{ color: var(--rose); }}
    .kicker-purple {{ color: var(--purple); }}
    .kicker-gold {{ color: var(--gold); }}
    .kicker-indigo {{ color: var(--indigo); }}
    .kicker-emerald {{ color: var(--emerald); }}

    .bento-card-title {{
      font-size: 1.15rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.35;
      margin-bottom: 6px;
      letter-spacing: -0.01em;
    }}
    .bento-card-sub {{
      font-size: 0.82rem;
      color: #cbd5e1;
      line-height: 1.45;
      margin-bottom: 12px;
    }}

    /* ROOT DRIVERS LIST */
    .drivers-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: auto;
    }}
    .driver-item {{
      background: rgba(15, 23, 42, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 10px;
      padding: 8px 12px;
      display: flex;
      align-items: flex-start;
      gap: 8px;
    }}
    .driver-icon {{
      font-size: 0.90rem;
      flex-shrink: 0;
      margin-top: 1px;
    }}
    .driver-text {{
      font-size: 0.77rem;
      color: #94a3b8;
      line-height: 1.4;
    }}
    .driver-text b {{
      color: #e2e8f0;
      font-weight: 700;
    }}

    /* HEALTH TWINS CHIPS & CALLOUT */
    .twins-badge-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }}
    .twin-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(168, 85, 247, 0.12);
      border: 1px solid rgba(168, 85, 247, 0.35);
      color: #e9d5ff;
      font-size: 0.80rem;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 9999px;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .twin-pill:hover {{
      background: rgba(168, 85, 247, 0.25);
      border-color: var(--purple);
      color: #ffffff;
      transform: translateY(-1px);
    }}
    .twin-rationale-text {{
      font-size: 0.78rem;
      color: #94a3b8;
      margin-bottom: 10px;
      line-height: 1.4;
    }}
    .twin-model-box {{
      background: rgba(15, 23, 42, 0.70);
      border-left: 3px solid var(--purple);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.80rem;
      color: #cbd5e1;
      line-height: 1.45;
      margin-top: auto;
    }}

    /* BUDGET STACK (CLEAN ROWS) */
    .budget-stack {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .budget-line {{
      background: rgba(15, 23, 42, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 12px;
      padding: 10px 14px;
    }}
    .budget-label-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 5px;
      font-size: 0.82rem;
      font-weight: 700;
      color: #ffffff;
    }}
    .budget-pct-tag {{
      font-size: 0.95rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
    }}
    .meter-track {{
      width: 100%;
      height: 7px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 6px;
    }}
    .meter-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width 0.7s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    .budget-spend-detail {{
      font-size: 0.75rem;
      color: #94a3b8;
      line-height: 1.4;
    }}

    /* ROADMAP & MILESTONES */
    .roadmap-list {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .roadmap-item {{
      background: rgba(15, 23, 42, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 10px;
      padding: 8px 12px;
    }}
    .roadmap-phase-tag {{
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 800;
      color: var(--indigo);
      background: rgba(129, 140, 248, 0.12);
      padding: 2px 7px;
      border-radius: 9999px;
      margin-bottom: 4px;
    }}
    .roadmap-item-title {{
      font-size: 0.82rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 2px;
    }}
    .roadmap-item-desc {{
      font-size: 0.75rem;
      color: #94a3b8;
      line-height: 1.35;
    }}

    /* MILESTONES 2X2 GRID */
    .milestones-2x2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-top: auto;
    }}
    .milestone-box {{
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(16, 185, 129, 0.2);
      border-radius: 10px;
      padding: 10px 12px;
      text-align: center;
    }}
    .milestone-lbl {{
      font-size: 0.64rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 3px;
    }}
    .milestone-num {{
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--emerald);
      font-family: 'JetBrains Mono', monospace;
    }}
    .milestone-note {{
      font-size: 0.65rem;
      color: #94a3b8;
    }}

    @media (max-width: 1100px) {{
      .dashboard-grid {{
        grid-template-columns: 1fr;
      }}
      .left-pane {{
        position: static;
      }}
      .bento-grid {{
        grid-template-columns: 1fr;
      }}
      .bento-full {{
        grid-column: span 1;
      }}
    }}
  </style>
</head>
<body>

  <!-- FLOATING TOP NAVIGATION BAR -->
  <header class="top-header">
    <a href="preview.html" class="brand-bar">
      <div class="brand-logo">◈</div>
      <div>
        <span class="brand-name">AeroTB</span>
        <span class="brand-sub">/ INDIA REGIONAL INTELLIGENCE</span>
      </div>
    </a>

    <!-- UNIFIED 4 NAVIGATION PILLS -->
    <nav class="nav-pill-group">
      <a href="preview.html" class="nav-pill" onclick="return openAppPage(event, 'Home')">🗺️ Command Map</a>
      <a href="compare_preview.html" class="nav-pill" onclick="return openAppPage(event, 'compare')">📈 Compare States</a>
      <a href="overcome_preview.html" class="nav-pill active">🚀 Road to Overcome</a>
      <a href="/?page=knowledge" class="nav-pill" onclick="return openAppPage(event, 'knowledge')">🆘 TB Knowledge & Helplines</a>
    </nav>

    <div class="provenance-badge">
      <div class="pulse-dot"></div>
      <span>MoHFW Verified (N=36)</span>
    </div>
  </header>

  <div class="container">

    <!-- 2-COLUMN BALANCED WORKSPACE -->
    <div class="dashboard-grid">
      
      <!-- LEFT: SELECTOR & STICKY MAP -->
      <aside class="left-pane">
        <div class="selector-header">
          <span>📍 Select Target State</span>
          <span style="font-size:0.65rem; color:#64748b;">36 STATES & UTS</span>
        </div>
        <select id="state-select" class="state-dropdown" onchange="selectState(this.value)">
        </select>

        <div class="filter-pills">
          <button class="filter-pill active" onclick="filterMap('all', this)">All</button>
          <button class="filter-pill" onclick="filterMap('alpha', this)">🛡️ High-Volume</button>
          <button class="filter-pill" onclick="filterMap('beta', this)">⚡ Comorbidity</button>
          <button class="filter-pill" onclick="filterMap('gamma', this)">🏔️ Mountain/Frontier</button>
        </div>

        <div class="map-box">
          {svg_map_html}
        </div>
        <p class="map-caption">Click any state on the map to switch its public health dossier.</p>
      </aside>

      <!-- RIGHT: ULTRA-CLEAN BENTO WORKSPACE -->
      <main class="right-pane">
        
        <!-- COMPACT STATE EXECUTIVE HEADER -->
        <section class="state-exec-bar">
          <div class="exec-left">
            <h2 id="exec-state-title" class="exec-state-name">Uttar Pradesh</h2>
            <div id="exec-team-badge" class="exec-team-badge">🛡️ High-Volume Giant</div>
          </div>
          <div class="exec-kpi-row">
            <div class="exec-kpi-pill">
              <span class="exec-kpi-lbl">Annual Cases</span>
              <span id="kpi-cases" class="exec-kpi-val">620,325</span>
            </div>
            <div class="exec-kpi-pill">
              <span class="exec-kpi-lbl">Comorbidity</span>
              <span id="kpi-dm" class="exec-kpi-val">18.4%</span>
            </div>
            <div class="exec-kpi-pill">
              <span class="exec-kpi-lbl">Private Share</span>
              <span id="kpi-private" class="exec-kpi-val">28.2%</span>
            </div>
            <div class="exec-kpi-pill">
              <span class="exec-kpi-lbl">DBT Poshan</span>
              <span id="kpi-dbt" class="exec-kpi-val">74%</span>
            </div>
          </div>
        </section>

        <!-- BENTO GRID (CLEAN & BALANCED) -->
        <div class="bento-grid">
          
          <!-- BENTO 1: PROBLEM & ROOT CAUSES (LEFT 50%) -->
          <div class="bento-card">
            <div class="card-kicker kicker-rose">🔴 1. The Core Bottleneck & Root Drivers</div>
            <h3 id="problem-headline" class="bento-card-title">Overburdened District Labs & 10-Day Lag</h3>
            <p id="problem-sub" class="bento-card-sub">Massive patient volume concentrates at tertiary hospitals, causing diagnostic backlogs while patients continue household transmission.</p>
            <div id="drivers-container" class="drivers-list">
              <!-- Dynamically populated 3 root drivers -->
            </div>
          </div>

          <!-- BENTO 2: HEALTH TWINS & PROVEN POLICY (RIGHT 50%) -->
          <div class="bento-card">
            <div class="card-kicker kicker-purple">🤝 2. Regional Health Twins & Peer Blueprint</div>
            <div class="twins-badge-row" id="twins-row">
              <!-- Dynamically populated twin pills -->
            </div>
            <p id="twin-rationale" class="twin-rationale-text"></p>
            <div class="twin-model-box" id="twin-model-box">
              <!-- Dynamically populated case study -->
            </div>
          </div>

          <!-- BENTO 3: STRATEGIC BUDGET BREAKDOWN (FULL WIDTH 100%) -->
          <div class="bento-card bento-full">
            <div class="card-kicker kicker-gold">💰 3. Strategic Budget & Resource Allocation Matrix</div>
            <div class="budget-stack" id="budget-stack">
              <!-- Dynamically populated 3 budget rows -->
            </div>
          </div>

          <!-- BENTO 4: 90-DAY EXECUTION ROADMAP (LEFT 50%) -->
          <div class="bento-card">
            <div class="card-kicker kicker-indigo">📅 4. 90-Day Operational Roadmap (For IAS & CMOs)</div>
            <div class="roadmap-list" id="roadmap-list">
              <!-- Dynamically populated 30/60/90 day action steps -->
            </div>
          </div>

          <!-- BENTO 5: PROJECTED 12-MONTH IMPACT MILESTONES (RIGHT 50%) -->
          <div class="bento-card">
            <div class="card-kicker kicker-emerald">🎯 5. Projected 12-Month Impact Milestones</div>
            <p style="font-size:0.78rem; color:#94a3b8; margin-bottom:10px;">Measurable public health key performance indicators projected upon executing the 90-day plan:</p>
            <div class="milestones-2x2" id="milestones-grid">
              <!-- Dynamically populated 2x2 target metrics -->
            </div>
          </div>

        </div>

      </main>

    </div>

  </div>

  <script>
    const STATES_DATA = {states_json};
    let currentState = "Uttar Pradesh";

    // Populate dropdown
    const selectElem = document.getElementById("state-select");
    Object.keys(STATES_DATA).sort().forEach(stateName => {{
      const opt = document.createElement("option");
      opt.value = stateName;
      opt.textContent = stateName;
      selectElem.appendChild(opt);
    }});

    // Bind map paths
    function initMap() {{
      const paths = document.querySelectorAll(".state-shape");
      paths.forEach(path => {{
        const name = path.getAttribute("data-name");
        if (STATES_DATA[name]) {{
          path.setAttribute("data-cluster-team", STATES_DATA[name].team);
        }}
        path.addEventListener("click", () => {{
          if (STATES_DATA[name]) {{
            selectState(name);
          }}
        }});
      }});
    }}

    function selectState(stateName) {{
      if (!STATES_DATA[stateName]) return;
      currentState = stateName;
      selectElem.value = stateName;

      // Update map active class
      document.querySelectorAll(".state-shape").forEach(path => {{
        const name = path.getAttribute("data-name");
        if (name === stateName) {{
          path.classList.add("active-state");
        }} else {{
          path.classList.remove("active-state");
        }}
      }});

      const data = STATES_DATA[stateName];

      // Executive Header & Compact KPIs
      document.getElementById("exec-state-title").textContent = stateName;
      const teamBadge = document.getElementById("exec-team-badge");
      teamBadge.textContent = data.teamTitle;
      teamBadge.style.color = data.teamColor;
      teamBadge.style.borderColor = data.teamColor + "55";
      teamBadge.style.background = data.teamColor + "18";

      document.getElementById("kpi-cases").textContent = (data.kpi.cases || "").split(" ")[0];
      document.getElementById("kpi-dm").textContent = (data.kpi.dm || "").split(" ")[0];
      document.getElementById("kpi-private").textContent = (data.kpi.private || "").split(" ")[0];
      document.getElementById("kpi-dbt").textContent = (data.kpi.dbt || "").split(" ")[0];

      // 1. Problem & Root Drivers (Clean list)
      document.getElementById("problem-headline").textContent = data.problem;
      document.getElementById("problem-sub").textContent = data.problemSub;
      const driversContainer = document.getElementById("drivers-container");
      driversContainer.innerHTML = "";
      (data.rootDrivers || []).forEach(d => {{
        const row = document.createElement("div");
        row.className = "driver-item";
        row.innerHTML = `
          <span class="driver-icon">${{d.icon}}</span>
          <span class="driver-text"><b>${{d.title}}:</b> ${{d.desc}}</span>
        `;
        driversContainer.appendChild(row);
      }});

      // 2. Twins & Blueprint
      const twinsRow = document.getElementById("twins-row");
      twinsRow.innerHTML = "";
      data.twins.forEach(twin => {{
        const pill = document.createElement("button");
        pill.className = "twin-pill";
        pill.innerHTML = `<span>🤝</span> <span>${{twin}}</span>`;
        pill.onclick = () => selectState(twin);
        twinsRow.appendChild(pill);
      }});
      document.getElementById("twin-rationale").textContent = data.twinRationale || "Statistical peer based on notification volume and comorbidity triad clustering.";
      document.getElementById("twin-model-box").innerHTML = `<b>Proven Twin Blueprint:</b> ${{data.twinPolicy}}`;

      // 3. Budget Stack (Clean progress rows)
      const budgetStack = document.getElementById("budget-stack");
      budgetStack.innerHTML = "";
      data.budget.forEach(b => {{
        const line = document.createElement("div");
        line.className = "budget-line";
        line.innerHTML = `
          <div class="budget-label-row">
            <span>${{b.label}}</span>
            <span class="budget-pct-tag" style="color:${{b.color}}">${{b.pct}}%</span>
          </div>
          <div class="meter-track">
            <div class="meter-fill" style="width:${{b.pct}}%; background:${{b.color}};"></div>
          </div>
          <div class="budget-spend-detail">${{b.spend || ""}}</div>
        `;
        budgetStack.appendChild(line);
      }});

      // 4. Roadmap (Clean 3-step timeline)
      const roadmapList = document.getElementById("roadmap-list");
      roadmapList.innerHTML = "";
      (data.roadmap || []).forEach(r => {{
        const rbox = document.createElement("div");
        rbox.className = "roadmap-item";
        rbox.innerHTML = `
          <span class="roadmap-phase-tag">${{r.phase}}</span>
          <div class="roadmap-item-title">${{r.title}}</div>
          <div class="roadmap-item-desc">${{r.desc}}</div>
        `;
        roadmapList.appendChild(rbox);
      }});

      // 5. Target Milestones (2x2 Grid)
      const milestonesGrid = document.getElementById("milestones-grid");
      milestonesGrid.innerHTML = "";
      (data.milestones || []).forEach(m => {{
        const mbox = document.createElement("div");
        mbox.className = "milestone-box";
        mbox.innerHTML = `
          <div class="milestone-lbl">${{m.label}}</div>
          <div class="milestone-num">${{m.val}}</div>
          <div class="milestone-note">${{m.sub}}</div>
        `;
        milestonesGrid.appendChild(mbox);
      }});
    }}

    function filterMap(team, btn) {{
      document.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".state-shape").forEach(path => {{
        const t = path.getAttribute("data-cluster-team");
        if (team === "all" || t === team) {{
          path.style.opacity = "1";
        }} else {{
          path.style.opacity = "0.15";
        }}
      }});
    }}

    // Navigation bridging for Streamlit iframe
    function openAppPage(e, key) {{
      if (e && e.preventDefault) e.preventDefault();
      try {{
        if (window.parent && window.parent.document) {{
          const link = window.parent.document.getElementById('st-nav-link-' + key);
          if (link) {{ link.click(); return false; }}
        }}
      }} catch(err) {{}}
      try {{
        if (window.parent && window.parent !== window) {{
          window.parent.postMessage({{ type: 'aerotb-nav', page: key }}, '*');
        }}
      }} catch(err) {{}}
      const targetUrl = (key === 'Home') ? 'preview.html' : (key === 'compare' ? 'compare_preview.html' : '/?page=' + encodeURIComponent(key));
      try {{
        if (window.top && window.top !== window) {{ window.top.location.href = targetUrl; return false; }}
      }} catch(e) {{}}
      window.location.href = targetUrl;
      return false;
    }}

    // Init on load
    initMap();
    selectState(currentState);
  </script>
</body>
</html>"""

Path("overcome_preview.html").write_text(html_content, encoding="utf-8")
print(f"Generated clean bento overcome_preview.html! File size: {len(html_content)} bytes")
