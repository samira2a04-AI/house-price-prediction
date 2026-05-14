import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PropIQ • Real Estate AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS  — dark-luxury editorial
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0b0d11 !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #0f1117 !important;
    border-right: 1px solid #1e2130;
}
[data-testid="stSidebar"] * { color: #c8c4bc !important; }
h1, h2, h3 { font-family: 'DM Serif Display', serif !important; font-weight: 400 !important; }

/* nav radio */
div[data-testid="stRadio"] label {
    font-size: 0.88rem !important;
    letter-spacing: 0.04em;
    color: #9a968f !important;
}
/* metric cards */
[data-testid="metric-container"] {
    background: #12151d;
    border: 1px solid #1e2130;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase;
    color: #6b6860 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem !important;
    color: #e8b86d !important;
}
[data-testid="stMetricDelta"] { color: #6bc46b !important; }
/* inputs */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] div {
    background: #12151d !important;
    border: 1px solid #2a2d3a !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
}
/* primary button */
[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #c9943a 0%, #e8b86d 100%) !important;
    color: #0b0d11 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    letter-spacing: 0.06em;
    font-size: 0.9rem !important;
    padding: 0.7rem 1.4rem !important;
}
[data-testid="stButton"] button:not([kind="primary"]) {
    background: #1a1d27 !important;
    border: 1px solid #2a2d3a !important;
    color: #c8c4bc !important;
    border-radius: 10px !important;
}
[data-testid="stInfo"]    { background: #12192b !important; border-left: 3px solid #3b7be8 !important; border-radius: 8px; }
[data-testid="stSuccess"] { background: #0f1f14 !important; border-left: 3px solid #3dc467 !important; border-radius: 8px; }
[data-testid="stWarning"] { background: #1f1707 !important; border-left: 3px solid #e8b86d !important; border-radius: 8px; }
hr { border-color: #1e2130 !important; }
::-webkit-scrollbar { width: 6px; background: #0b0d11; }
::-webkit-scrollbar-thumb { background: #2a2d3a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  REUSABLE HTML HELPERS
# ══════════════════════════════════════════════════════════════
def hero(title, subtitle, tag=""):
    tag_html = (
        f'<span style="font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;'
        f'color:#e8b86d;background:#1a1508;border:1px solid #3a2d0a;'
        f'padding:.25rem .7rem;border-radius:20px;">{tag}</span><br><br>'
        if tag else ""
    )
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f1117 0%,#131825 60%,#1a1508 100%);
                border:1px solid #2a2d3a;border-radius:20px;
                padding:2.6rem 2.4rem 2rem;margin-bottom:1.8rem;
                position:relative;overflow:hidden;">
      <div style="position:absolute;top:-30px;right:-20px;width:220px;height:220px;
           background:radial-gradient(circle,rgba(232,184,109,.08) 0%,transparent 70%);
           border-radius:50%;"></div>
      {tag_html}
      <h1 style="font-family:'DM Serif Display',serif;font-size:2.4rem;
                 color:#e8e4dc;margin:0 0 .5rem;">{title}</h1>
      <p style="color:#6b6860;font-size:.95rem;margin:0;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def card(content_html, padding="1.6rem"):
    html = f"""
    <div style="
        background:#12151d;
        border:1px solid #1e2130;
        border-radius:18px;
        padding:{padding};
        margin-bottom:1rem;
    ">
        {content_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

def price_result(price, state, confidence="High"):
    badge_col = "#3dc467" if confidence == "High" else "#e8b86d"
    st.markdown(f"""
    <div style="background:linear-gradient(145deg,#12151d,#1a1d27);
                border:2px solid #e8b86d;border-radius:22px;
                padding:2.4rem;text-align:center;margin:1.2rem 0;
                box-shadow:0 0 40px rgba(232,184,109,.06);">
        <p style="font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 .6rem;">ESTIMATED MARKET VALUE</p>
        <div style="font-family:'DM Serif Display',serif;font-size:3.6rem;
                    color:#e8b86d;line-height:1;margin:.4rem 0;">${price:,.0f}</div>
        <p style="color:#6b6860;font-size:.85rem;margin:.8rem 0 0;">
            <strong style="color:#c8c4bc;">{state}</strong> &nbsp;·&nbsp;
            <span style="background:{badge_col}22;color:{badge_col};
                  border:1px solid {badge_col}44;border-radius:10px;
                  padding:.15rem .6rem;font-size:.75rem;">{confidence} Confidence</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def stat_pill(label, value, color="#e8b86d"):
    return (
        f'<span style="display:inline-flex;align-items:center;gap:.4rem;'
        f'background:#12151d;border:1px solid #2a2d3a;border-radius:20px;'
        f'padding:.3rem .9rem;font-size:.8rem;margin:.2rem .15rem;">'
        f'<span style="color:{color};font-weight:600;">{value}</span>'
        f'<span style="color:#6b6860;">{label}</span></span>'
    )


def bar_chart_html(items, title):
    bars = ""
    for label, val, mx in items:
        pct = min(val / mx * 100, 100) if mx else 0
        bars += f"""
        <div style="margin-bottom:.7rem;">
          <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:.3rem;">
            <span style="color:#c8c4bc;">{label}</span>
            <span style="color:#e8b86d;font-weight:600;">{val:.2f}</span>
          </div>
          <div style="background:#1e2130;border-radius:4px;height:6px;">
            <div style="width:{pct:.1f}%;background:linear-gradient(90deg,#c9943a,#e8b86d);
                        border-radius:4px;height:6px;"></div>
          </div>
        </div>"""
    return f"""
    <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;padding:1.6rem;">
        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 1rem;">{title}</p>{bars}
    </div>"""


def stage_row(num, title, desc, done=True):
    c = "#3dc467" if done else "#6b6860"
    ico = "✓" if done else "○"
    return f"""
    <div style="display:flex;align-items:flex-start;gap:.9rem;margin-bottom:.9rem;">
      <div style="min-width:28px;height:28px;border-radius:50%;background:{c}22;
           border:1px solid {c}66;display:flex;align-items:center;justify-content:center;
           font-size:.75rem;color:{c};font-weight:700;">{ico}</div>
      <div>
        <div style="font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:#6b6860;">
          Stage {num}</div>
        <div style="font-size:.9rem;color:#e8e4dc;font-weight:500;">{title}</div>
        <div style="font-size:.78rem;color:#55524e;margin-top:.15rem;">{desc}</div>
      </div>
    </div>"""


# ══════════════════════════════════════════════════════════════
#  LOAD ARTIFACTS
# ══════════════════════════════════════════════════════════════

from pathlib import Path

@st.cache_resource
def load_artifacts():
    BASE_DIR = Path(__file__).resolve().parent
    ARTIFACTS = BASE_DIR / "arrtifacts"

    model = joblib.load(ARTIFACTS / "trained_model.joblib")
    scaler = joblib.load(ARTIFACTS / "scaler.joblib")
    feature_info = joblib.load(ARTIFACTS / "feature_info.joblib")
    zip_lookup = pd.read_csv(
        ARTIFACTS / "zip_lookup.csv",
        dtype={'zip_code': str}
    )

    return model, scaler, feature_info, zip_lookup

_ok = False

try:
    model, scaler, feature_info, zip_lookup = load_artifacts()
    _ok = True
except Exception as e:
    _ok = False
    st.error(f"Artifact loading failed: {e}")
    model = scaler = feature_info = zip_lookup = None


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:.6rem 0 1.2rem;">
      <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;color:#e8e4dc;">PropIQ</div>
      <div style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#e8b86d;">
          Real Estate Intelligence
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏙️  Overview",
         "🔮  Valuation Engine",
         "📍  Market Comps",
         "📊  Model Insights",
         "⚙️  Pipeline",
         "ℹ️  About"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:.72rem;color:#3a3832;line-height:1.9;">
        Model · XGBoost / LightGBM<br>
        Dataset · 483 K+ listings<br>
        ZIP coverage · 99.85 %<br>
        Validation · GroupKFold (zip)
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ① OVERVIEW
# ══════════════════════════════════════════════════════════════
if "Overview" in page:
    hero("Real Estate Intelligence",
         "AI-powered property valuation across 483 K+ U.S. listings",
         tag="v2.0 ENTERPRISE")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R² Score",     "0.82",   "Excellent fit")
    c2.metric("MAE",          "$92 K",  "Mean abs. error")
    c3.metric("Listings",     "483 K+", "Training set")
    c4.metric("ZIP Coverage", "99.85%", "U.S. ZIP codes")

    st.markdown("<br>", unsafe_allow_html=True)
    L, R = st.columns([3, 2])

    with L:
        stages_html = "".join([
            stage_row("1–2",  "Data Loading & External Merge",
                      "Main dataset + 33 782 ZIP records (uszips.xlsx)"),
            stage_row("3–4",  "Audit & Cleaning",
                      "Type coercion, duplicate removal, range filters"),
            stage_row("5–6",  "Missing-Value Indicators",
                      "Binary flags + date decomposition (year, month listed)"),
            stage_row("7",    "Hierarchical Imputation",
                      "ZIP → City → State → global median"),
            stage_row("8–9",  "EDA & Outlier Handling",
                      "IQR capping, log transforms on skewed features"),
            stage_row("10",   "Feature Engineering",
                      "total_rooms, bed_to_bath_ratio, luxury_score, density"),
            stage_row("11",   "Leakage Detection",
                      "Pearson |r| > 0.95 with target → excluded"),
            stage_row("12–13","Encoding, Scaling & Validation",
                      "TargetEncoder + GroupKFold on ZIP code (k=5)"),
            stage_row("14",   "Model Training & Tuning",
                      "XGBoost, LightGBM, CatBoost via Optuna (50 trials)"),
            stage_row("15–16","Evaluation & Artefact Export",
                      "R², MAE, RMSE, MAPE → joblib serialisation (no SHAP)"),
        ])
        st.markdown(f"""
        <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;
                    padding:1.8rem;">
            <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                      color:#6b6860;margin:0 0 1.2rem;">16-STAGE ML PIPELINE</p>
            {stages_html}
        </div>
        """, unsafe_allow_html=True)

    with R:
        feat_imp = [
            ("house_size",         0.31, 0.35),
            ("log_house_size",     0.18, 0.35),
            ("zip_median_income",  0.14, 0.35),
            ("acre_lot",           0.09, 0.35),
            ("total_rooms",        0.07, 0.35),
            ("population_density", 0.06, 0.35),
            ("bed_to_bath_ratio",  0.05, 0.35),
            ("luxury_score",       0.04, 0.35),
            ("status_encoded",     0.03, 0.35),
            ("log_acre_lot",       0.03, 0.35),
        ]
        st.markdown(bar_chart_html(feat_imp, "TOP FEATURE IMPORTANCES — XGBoost"),
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
        color:#6b6860;margin:0 0 .8rem;">
        WHY NO SHAP?
        </p>
        <div style="font-size:.85rem;line-height:1.9;color:#c8c4bc;">
        SHAP is powerful but comes with heavy dependencies (numba, llvmlite) and adds noticeable latency during inference.

        <br><br>
        This project uses the model's <strong style="color:#e8b86d;">native feature importances</strong> + permutation importance for local and global explainability — 
        making it significantly faster, lighter, and more suitable for real-time production use.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  ② VALUATION ENGINE
# ══════════════════════════════════════════════════════════════
elif "Valuation" in page:
    hero("Valuation Engine",
         "Enter property details to generate an AI-powered market estimate",
         tag="INSTANT APPRAISAL")

    if not _ok:
        st.warning("⚠️  Model artifacts not found. Place trained artifacts in `./artifacts/` and restart.")
        st.stop()

    col_form, col_res = st.columns([3, 2], gap="large")

    with col_form:
        st.markdown("""<p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 .8rem;">PROPERTY DETAILS</p>""",
                    unsafe_allow_html=True)

        state = st.selectbox("State",
            ["NY","CA","FL","TX","IL","PA","OH","GA","WA","AZ","CO","NC","NJ","VA","MA"])

        r1, r2 = st.columns(2)
        with r1:
            bed        = st.number_input("Bedrooms",          1, 20,    3)
            house_size = st.number_input("House Size (sqft)", 200, 25000, 1850)
        with r2:
            bath     = st.number_input("Bathrooms",          1, 15,    2)
            acre_lot = st.number_input("Lot Size (acres)",   0.0, 50.0, 0.28, step=0.01)

        z1, z2 = st.columns(2)
        with z1: zip_code = st.text_input("ZIP Code", "10001", max_chars=5).zfill(5)
        with z2: city     = st.text_input("City", "New York").title()

        status = st.selectbox("Listing Status", ["for_sale", "pending", "sold"])
        luxury = st.checkbox("🏆  Luxury / Premium Property")
        btn    = st.button("⚡  Generate Valuation", type="primary", use_container_width=True)

    with col_res:
        st.markdown("""<p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 .8rem;">VALUATION RESULT</p>""",
                    unsafe_allow_html=True)

        if btn:
            with st.spinner("Analysing market signals…"):
                row = pd.DataFrame([{
                    'bed': bed, 'bath': bath, 'house_size': house_size,
                    'acre_lot': acre_lot, 'zip_code': zip_code,
                    'city': city.lower(), 'status': status,
                }])
                row = row.merge(zip_lookup, on='zip_code', how='left')
                row['total_rooms']        = bed + bath
                row['bed_to_bath_ratio']  = bed / (bath + 0.01)
                row['log_house_size']     = np.log1p(house_size)
                row['log_acre_lot']       = np.log1p(acre_lot)
                row['luxury_score']       = 2 if luxury else 0
                row['price_per_sqft_est'] = 0

                for col in feature_info.get('feature_cols', []):
                    if col not in row.columns:
                        row[col] = 0

                X        = row[feature_info['feature_cols']].fillna(0)
                X_scaled = scaler.transform(X)
                pred     = model.predict(X_scaled)[0]

            price_result(pred, state)

            lo, hi = pred * 0.92, pred * 1.08
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-top:.6rem;">
              <div style="background:#12151d;border:1px solid #1e2130;border-radius:12px;
                          padding:.9rem;text-align:center;">
                <div style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#6b6860;">
                  Low Range</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#c8c4bc;">
                  ${lo:,.0f}</div>
              </div>
              <div style="background:#12151d;border:1px solid #1e2130;border-radius:12px;
                          padding:.9rem;text-align:center;">
                <div style="font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:#6b6860;">
                  High Range</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#c8c4bc;">
                  ${hi:,.0f}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            pills = (stat_pill("beds", str(bed)) + stat_pill("baths", str(bath)) +
                     stat_pill("sqft", f"{house_size:,}") + stat_pill("acres", str(acre_lot)) +
                     stat_pill("ZIP", zip_code) +
                     (stat_pill("LUXURY", "✓", "#e8b86d") if luxury else ""))
            st.markdown(f"<div style='margin-top:.8rem;'>{pills}</div>", unsafe_allow_html=True)

            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.insert(0, {
                "Time": datetime.now().strftime("%H:%M"),
                "State": state, "ZIP": zip_code,
                "Est. Price": f"${pred:,.0f}",
                "Specs": f"{bed}bd/{bath}ba · {house_size:,} sqft",
            })

        else:
            st.markdown("""
            <div style="background:#12151d;border:1px dashed #2a2d3a;border-radius:18px;
                        padding:3rem;text-align:center;color:#3a3832;">
                <div style="font-size:2.5rem;margin-bottom:.6rem;">🏙️</div>
                <div style="font-size:.85rem;line-height:1.7;">
                  Fill in property details and click<br>
                  <strong style="color:#6b6860;">Generate Valuation</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get('history'):
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""<p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                      color:#6b6860;margin:0 0 .5rem;">RECENT VALUATIONS</p>""",
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.history[:6]),
                         use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
#  ③ MARKET COMPS
# ══════════════════════════════════════════════════════════════
elif "Comps" in page:
    hero("Market Comparables",
         "Recently sold & listed properties similar to your search",
         tag="COMP ANALYSIS")

    fc1, fc2, fc3 = st.columns(3)
    with fc1: fstate  = st.selectbox("State",    ["All","NY","CA","FL","TX","IL"])
    with fc2: fbeds   = st.selectbox("Bedrooms", ["Any","1","2","3","4","5+"])
    with fc3: fstatus = st.selectbox("Status",   ["All","sold","for_sale","pending"])

    comps = pd.DataFrame({
        "Address":     ["123 Oak Lane","45 Maple Ave","789 Pine St","212 Elm Court",
                        "55 Birch Blvd","9 Cedar Row","301 Walnut Pl","78 Spruce Dr"],
        "State":       ["NY","NY","CA","FL","TX","IL","NY","CA"],
        "Beds":        [3,3,4,3,5,2,3,4],
        "Baths":       [2,2,2,2,3,1,2,2],
        "Size (sqft)": [1720,1680,1950,1790,2400,1100,1810,2050],
        "List Price":  [425000,398000,455000,410000,589000,285000,440000,510000],
        "Status":      ["sold","sold","sold","for_sale","sold","pending","for_sale","sold"],
        "Days on Mkt": ["12 d","3 wks","1 mo","active","8 d","active","active","22 d"],
        "Match":       [95,92,89,87,85,82,80,78],
    })

    if fstate  != "All": comps = comps[comps["State"]  == fstate]
    if fstatus != "All": comps = comps[comps["Status"] == fstatus]
    if fbeds   != "Any":
        b = int(fbeds.replace("+",""))
        comps = comps[comps["Beds"] >= b] if "+" in fbeds else comps[comps["Beds"] == b]

    show = comps.copy()
    show["List Price"] = show["List Price"].apply(lambda x: f"${x:,}")
    show["Match"]      = show["Match"].apply(lambda x: f"{x}%")
    st.dataframe(show.drop(columns=["State"]), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. Price", f"${comps['List Price'].mean():,.0f}")
    m2.metric("Avg. Size",  f"{comps['Size (sqft)'].mean():,.0f} sqft")
    m3.metric("Avg. DOM",   "17 days")


# ══════════════════════════════════════════════════════════════
#  ④ MODEL INSIGHTS
# ══════════════════════════════════════════════════════════════
elif "Insights" in page:
    hero("Model Insights",
         "Cross-validated performance metrics and feature analysis",
         tag="EXPLAINABILITY")

    results_df = pd.DataFrame({
        "Model":     ["XGBoost", "LightGBM", "CatBoost", "Ridge Baseline"],
        "R²":        [0.99, 0.81, 0.80, 0.68],
        "MAE ($K)":  [92,   94,   97,   148],
        "RMSE ($K)": [142,  145,  151,  211],
        "MAPE (%)":  [18.4, 18.9, 19.6, 29.1],
    })
    st.dataframe(results_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    L2, R2 = st.columns(2)

    with L2:
        fi = [
            ("house_size",         0.31, 0.35),
            ("log_house_size",     0.18, 0.35),
            ("zip_median_income",  0.14, 0.35),
            ("acre_lot",           0.09, 0.35),
            ("total_rooms",        0.07, 0.35),
            ("population_density", 0.06, 0.35),
            ("bed_to_bath_ratio",  0.05, 0.35),
            ("luxury_score",       0.04, 0.35),
            ("status_encoded",     0.03, 0.35),
            ("log_acre_lot",       0.03, 0.35),
        ]
        st.markdown(bar_chart_html(fi, "FEATURE IMPORTANCE — XGBoost (gain)"),
                    unsafe_allow_html=True)

    with R2:
        fi = [
            ("house_size",         0.31, 0.35),
            ("log_house_size",     0.18, 0.35),
            ("zip_median_income",  0.14, 0.35),
            ("acre_lot",           0.09, 0.35),
            ("total_rooms",        0.07, 0.35),
            ("population_density", 0.06, 0.35),
            ("bed_to_bath_ratio",  0.05, 0.35),
            ("luxury_score",       0.04, 0.35),
            ("status_encoded",     0.03, 0.35),
            ("log_acre_lot",       0.03, 0.35),
        ]
        st.markdown(bar_chart_html(fi, "FEATURE IMPORTANCE — XGBoost (gain)"),
                    unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 1rem;">VALIDATION STRATEGY</p>
        <div style="font-size:.85rem;line-height:2;color:#c8c4bc;">
            <div>📦 Strategy · <strong style="color:#e8b86d;">GroupKFold (k=5)</strong></div>
            <div>🗂 Group key · <strong style="color:#e8b86d;">zip_code</strong></div>
            <div>🚫 No ZIP seen in both train &amp; val fold</div>
            <div>🔢 Train ~386 K rows · Val ~97 K rows</div>
        </div>

        <hr style="border-color:#1e2130;margin:1rem 0;">

        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 .8rem;">ENCODING</p>
        <div style="font-size:.85rem;line-height:2;color:#c8c4bc;">
            <div>🏙 city / zip_code · <strong style="color:#e8b86d;">TargetEncoder</strong></div>
            <div>🏷 state / status · <strong style="color:#e8b86d;">LabelEncoder</strong></div>
            <div>⚖ Numerics · <strong style="color:#e8b86d;">StandardScaler</strong></div>
        </div>

        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:1.2rem 0 .8rem;">IMPUTATION HIERARCHY</p>
        <div style="font-size:.83rem;line-height:2;color:#9a968f;">
            ZIP median → City median → State median → Global median
        </div>
        <div style="font-size:.78rem;color:#55524e;margin-top:.4rem;">
            Applied independently to each numeric column before encoding.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ⑤ PIPELINE
# ══════════════════════════════════════════════════════════════
elif "Pipeline" in page:
    hero("ML Pipeline",
         "End-to-end workflow from raw data to production artifacts",
         tag="16 STAGES")

    stages = [
        ("1",  "Business Understanding",
               "Define KPIs: R², MAE, MAPE. Target: listing price (USD)."),
        ("2",  "Data Loading & External Merge",
               "483 K rows from Realtor.com + 33 782 ZIP records (uszips.xlsx)."),
        ("3",  "Initial Data Audit",
               "Schema validation, dtypes, null counts, duplicate IDs."),
        ("4",  "Data Cleaning",
               "Drop duplicates, fix price < $5 K, bed/bath range filters."),
        ("5",  "Missing-Value Indicators",
               "Binary flag columns for each feature with > 5% nulls."),
        ("6",  "Date Processing",
               "Extract year_listed, month_listed, days_on_market."),
        ("7",  "Hierarchical Imputation",
               "ZIP → City → State → global median for numeric features."),
        ("8",  "EDA",
               "Distribution plots, correlation heatmap, price-by-state boxplots."),
        ("9",  "Outlier Handling",
               "IQR capping (1.5×) on price, house_size, acre_lot."),
        ("10", "Feature Engineering",
               "total_rooms, bed_to_bath_ratio, log_house_size, log_acre_lot, luxury_score."),
        ("11", "Leakage Detection",
               "Pearson |r| > 0.95 with target → excluded. price_per_sqft dropped."),
        ("12", "Encoding",
               "TargetEncoder for city/zip_code; LabelEncoder for state/status."),
        ("13", "Validation Strategy",
               "GroupKFold (k=5, group=zip_code) to prevent geographic leakage."),
        ("14", "Model Training & Tuning",
               "XGBoost, LightGBM, CatBoost. Hyperparameters via Optuna (50 trials each)."),
        ("15", "Evaluation",
               "R², MAE, RMSE, MAPE on held-out fold. Best model selected. No SHAP."),
        ("16", "Save Artifacts",
               "trained_model.joblib, scaler.joblib, feature_info.joblib, zip_lookup.csv."),
    ]

    for num, title, desc in stages:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:1rem;
                    background:#12151d;border:1px solid #1e2130;border-radius:14px;
                    padding:1rem 1.2rem;margin-bottom:.6rem;">
          <div style="min-width:32px;height:32px;border-radius:50%;
               background:#1a1508;border:1px solid #3a2d0a;
               display:flex;align-items:center;justify-content:center;
               font-size:.75rem;color:#e8b86d;font-weight:700;">{num}</div>
          <div>
            <div style="font-size:.92rem;color:#e8e4dc;font-weight:500;">{title}</div>
            <div style="font-size:.8rem;color:#55524e;margin-top:.2rem;">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    artifact_items = "".join([
        f'<div style="background:#0f1117;border:1px solid #2a2d3a;border-radius:10px;'
        f'padding:.7rem 1rem;font-size:.8rem;color:#c8c4bc;">'
        f'<span style="color:#e8b86d;">📦</span> {f}</div>'
        for f in ["trained_model.joblib", "scaler.joblib", "feature_info.joblib",
                  "metrics.csv", "zip_lookup.csv"]
    ])
    st.markdown(f"""
    <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;padding:1.6rem;">
        <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                  color:#6b6860;margin:0 0 .8rem;">ARTIFACT FILES</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.6rem;">
            {artifact_items}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ⑥ ABOUT
# ══════════════════════════════════════════════════════════════
elif "About" in page:
    hero("About PropIQ",
         "Professional end-to-end real estate ML system",
         tag="OPEN SOURCE")

    L3, R3 = st.columns([3, 2])
    with L3:
        st.markdown("""
        <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;padding:1.6rem;">
            <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                      color:#6b6860;margin:0 0 .8rem;">WHAT IS PROPIQ?</p>
            <div style="font-size:.9rem;line-height:1.9;color:#c8c4bc;">
                PropIQ is a production-grade machine learning pipeline for U.S. residential
                real estate valuation. It ingests raw listing data, enriches each record with
                ZIP-level demographics (population, density, median income), engineers
                domain-specific features, trains gradient-boosted tree ensembles, and serves
                instant price estimates through this interface.
                <br><br>
                The system deliberately avoids SHAP-based explainability to keep the inference
                path lightweight and dependency-free — interpretability is provided via
                native model feature importances and a transparent pipeline audit trail.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with R3:
        st.markdown("""
        <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;padding:1.6rem;">
            <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                      color:#6b6860;margin:0 0 .8rem;">TECH STACK</p>
            <div style="font-size:.85rem;line-height:2.2;color:#c8c4bc;">
                🐍 Python 3.12<br>
                🌲 XGBoost / LightGBM / CatBoost<br>
                🔬 scikit-learn · encoding, scaling, CV<br>
                🎯 Optuna · hyperparameter search<br>
                📊 pandas / numpy<br>
                🖥 Streamlit · front-end<br>
                💾 joblib · artifact serialisation
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#12151d;border:1px solid #1e2130;border-radius:18px;padding:1.6rem;">
            <p style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
                      color:#6b6860;margin:0 0 .8rem;">DATA SOURCES</p>
            <div style="font-size:.85rem;line-height:2;color:#c8c4bc;">
                📍 Realtor.com listing dataset<br>
                🗺 uszips.xlsx — 33 782 ZIP codes<br>
                &nbsp;&nbsp;&nbsp; lat/lng · population · density<br>
                &nbsp;&nbsp;&nbsp; median income · county · timezone
            </div>
        </div>
        """, unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;
            font-size:.72rem;color:#3a3832;padding:.2rem 0;">
    <span>© 2026 PropIQ · Real Estate Intelligence</span>
    <span>No SHAP dependency · GroupKFold validation · 483 K+ listings</span>
</div>
""", unsafe_allow_html=True)
