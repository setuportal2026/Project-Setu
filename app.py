"""
Project SETU — MMHAPU Patna AI Helpdesk
Main Streamlit entrypoint. Multi-page, futuristic UI with per-page neon themes.
"""

import streamlit as st
from modules import guard, router, academics, scrapper

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project SETU ",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  LOAD HF TOKEN (safe — works even if not set)
# ─────────────────────────────────────────────────────────────
try:
    guard.HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    guard.HF_TOKEN = None

# ─────────────────────────────────────────────────────────────
#  PER-PAGE THEMES  (accent, glow, gradient)
# ─────────────────────────────────────────────────────────────
THEMES = {
    "Home": {
        "accent": "#7DF9FF",
        "gradient": "linear-gradient(135deg, #0f2027, #203a43, #2c5364)",
        "glow": "0 0 25px rgba(125,249,255,0.45)",
    },
    "Guard Layer": {
        "accent": "#00FFA3",
        "gradient": "linear-gradient(135deg, #0f2027, #134e4a, #0f2027)",
        "glow": "0 0 25px rgba(0,255,163,0.45)",
    },
    "KRC Locator": {
        "accent": "#C77DFF",
        "gradient": "linear-gradient(135deg, #1a0033, #3c096c, #1a0033)",
        "glow": "0 0 25px rgba(199,125,255,0.45)",
    },
    "Academics": {
        "accent": "#FFD166",
        "gradient": "linear-gradient(135deg, #1b1b2f, #2b2b52, #1b1b2f)",
        "glow": "0 0 25px rgba(255,209,102,0.45)",
    },
    "Notifications": {
        "accent": "#FF6B6B",
        "gradient": "linear-gradient(135deg, #1a0e0e, #3a1c1c, #1a0e0e)",
        "glow": "0 0 25px rgba(255,107,107,0.45)",
    },
}

# ─────────────────────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<h2 style='letter-spacing:2px;'>🛰️ SETU</h2>"
    "<p style='opacity:0.6;font-size:13px;margin-top:-10px;'>University Project</p>",
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Navigate",
    list(THEMES.keys()),
    label_visibility="collapsed",
)
theme = THEMES[page]

# ─────────────────────────────────────────────────────────────
#  GLOBAL + DYNAMIC CSS INJECTION
# ─────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {{
        font-family: 'Poppins', sans-serif;
    }}

    .stApp {{
        background: {theme['gradient']};
        background-attachment: fixed;
        transition: background 0.6s ease;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(10, 10, 20, 0.85);
        border-right: 1px solid {theme['accent']}55;
    }}

    h1, h2, h3 {{
        font-family: 'Orbitron', sans-serif !important;
        color: {theme['accent']} !important;
        text-shadow: {theme['glow']};
    }}

    .setu-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid {theme['accent']}44;
        border-radius: 16px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: {theme['glow']};
    }}

    .stButton>button {{
        background: transparent;
        border: 1.5px solid {theme['accent']};
        color: {theme['accent']};
        border-radius: 10px;
        padding: 8px 22px;
        font-weight: 600;
        transition: all 0.25s ease;
    }}
    .stButton>button:hover {{
        background: {theme['accent']};
        color: #0a0a14;
        box-shadow: {theme['glow']};
    }}

    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {{
        background: rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid {theme['accent']}55 !important;
    }}

    .metric-glow {{
        font-family: 'Orbitron', sans-serif;
        font-size: 34px;
        color: {theme['accent']};
        text-shadow: {theme['glow']};
    }}

    hr {{
        border-color: {theme['accent']}33;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────────────────────
if page == "Home":
    st.markdown("<h1>PROJECT SETU</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='opacity:0.75;font-size:16px;'>"
        "AI Helpdesk for student ",
        
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    cols = st.columns(4)
    labels = ["Guard Layer", "KRC Locator", "Academics", "Notifications"]
    descs = [
        "Fraud-safe document guidance",
        "Find your nearest KRC instantly",
        "Percentage calc + syllabus",
        "Latest university notices",
    ]
    for c, l, d in zip(cols, labels, descs):
        with c:
            st.markdown(
                f"<div class='setu-card'><b>{l}</b><br>"
                f"<span style='opacity:0.7;font-size:13px;'>{d}</span></div>",
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────────────────────
#  PAGE: GUARD LAYER
# ─────────────────────────────────────────────────────────────
elif page == "Guard Layer":
    st.markdown("<h1>🛡️ Guard Layer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='setu-card'>Puchho document (Migration, TC, Marksheet, Degree) "
        "kaise apply karein — hum fraud-prone queries automatically flag karte hain.</div>",
        unsafe_allow_html=True,
    )

    query = st.text_input("Apna sawaal likhein", placeholder="e.g. Migration certificate kaise milega?")
    district = st.text_input("Apna district (nearest KRC ke liye, optional)")

    if st.button("Check"):
        if query.strip():
            result = guard.guard_and_guide(query, student_district=district or None)
            if result["status"] == "warning":
                st.error(result["message"])
            elif result["status"] == "guidance":
                st.markdown(f"<div class='setu-card'><b>📄 {result['document'].title()}</b></div>", unsafe_allow_html=True)
                st.markdown(f"**Online Process:**\n\n{result['online_process']}")
                st.markdown(f"**Offline Process:**\n\n{result['offline_process']}")
                if result["nearest_krc"]:
                    st.markdown("**Nearest KRC:**")
                    st.markdown(result["nearest_krc"])
            else:
                st.warning(result["message"])
        else:
            st.warning("Pehle apna sawaal likhein.")

# ─────────────────────────────────────────────────────────────
#  PAGE: KRC LOCATOR
# ─────────────────────────────────────────────────────────────
elif page == "KRC Locator":
    st.markdown("<h1>📍 KRC Locator</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["By Code", "By Name", "By District"])
    data = router.load_krc_data()

    with tab1:
        code = st.text_input("3-digit KRC code")
        if st.button("Find KRC"):
            info = router.get_krc_by_code(code, data)
            if info:
                st.markdown(f"<div class='setu-card'>{router.format_krc_card(code, info)}</div>", unsafe_allow_html=True)
            else:
                st.error("Code nahi mila.")

    with tab2:
        name_q = st.text_input("Institution ka naam")
        if name_q:
            for r in router.search_krc_by_name(name_q, data)[:10]:
                st.markdown(f"<div class='setu-card'>{router.format_krc_card(r['krc_code'], r)}</div>", unsafe_allow_html=True)

    with tab3:
        districts = router.list_all_districts(data)
        chosen = st.selectbox("District chuno", districts)
        if chosen:
            for r in router.search_krc_by_district(chosen, data)[:10]:
                st.markdown(f"<div class='setu-card'>{router.format_krc_card(r['krc_code'], r)}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  PAGE: ACADEMICS
# ─────────────────────────────────────────────────────────────
elif page == "Academics":
    st.markdown("<h1>📊 Academics</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Percentage Calculator", "Syllabus"])
    with tab1:
        academics.cgpa_calculator_tab()
    with tab2:
        academics.syllabus_tab()

# ─────────────────────────────────────────────────────────────
#  PAGE: NOTIFICATIONS
# ─────────────────────────────────────────────────────────────
elif page == "Notifications":
    st.markdown("<h1>📢 Notifications</h1>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Latest"):
        notices = scrapper.get_notifications(force_refresh=True)
    else:
        notices = scrapper.get_notifications()

    if notices:
        for n in notices:
            st.markdown(
                f"<div class='setu-card'><a href='{n['link']}' style='color:{theme['accent']};text-decoration:none;' target='_blank'>"
                f"📄 {n['title']}</a></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Abhi koi notification cache me nahi hai — Refresh dabao.")