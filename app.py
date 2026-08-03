from email_helper import send_notification_email, send_emergency_email
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyvkedZBy_iCpuuL0zVXPaVTaMqxBv-MNDR537kUnL5tqgksdiTjRWL-Lx2GV7kjUE09Q/exec"
SHEET_ID = "1h85m2f6UmE9NPOcHrQnU2_n7GWyL1ZTLhyvbJuUrl94"
REQUESTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Requests"

st.set_page_config(
    page_title="ChiEAC Support Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"

)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
@media screen and (max-width: 768px) {
    .block-container { padding: 0 !important; }
}
.stApp { background-color: #ffffff; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
section[data-testid="stSidebar"] > div {padding-top: 0rem;}
button[data-testid="baseButton-header"] {display: block !important; visibility: visible !important;}
[data-testid="collapsedControl"] {display: block !important; visibility: visible !important;}
.block-container { padding-top: 0rem !important; max-width: 100% !important; }
.hero-section { background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 60%, #f0fdf4 100%); padding: 90px 80px; text-align: center; border-bottom: 1px solid #e8e8e8; }
.hero-badge { display: inline-block; background: #dcfce7; color: #2d6a4f; padding: 6px 18px; border-radius: 100px; font-size: 0.85em; font-weight: 600; margin-bottom: 28px; letter-spacing: 0.5px; }
.hero-title { font-size: clamp(1.5em, 4vw, 3.8em); font-weight: 900; color: #1a1a1a; line-height: 1.1; margin-bottom: 20px; letter-spacing: -1.5px; }
@media (max-width: 768px) {
    .hero-section { padding: 40px 20px !important; }
    .section { padding: 40px 20px !important; }
    .tags-section { padding: 24px 20px !important; }
    .volunteer-section { padding: 40px 20px !important; }
    .footer-section { padding: 24px 20px !important; }
    .stat-number { font-size: 2em !important; }
    .section-title { font-size: 1.6em !important; white-space: normal !important; }
    .gift-card { flex-direction: column !important; }
    .program-card { margin-bottom: 16px !important; }
}
.hero-title span { color: #2d6a4f; }
.hero-tagline { font-size: 1.1em; color: #2d6a4f; font-style: italic; margin-bottom: 16px; font-weight: 500; }
.hero-subtitle { font-size: 1.1em; color: #666; line-height: 1.8; max-width: 640px; margin: 0 auto 48px auto; }
.stat-item { text-align: center; }
.stat-number { font-size: 3em; font-weight: 900; color: #2d6a4f; line-height: 1; }
.stat-label { font-size: 0.85em; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 6px; }
.section { padding: 80px 80px; }
.section-alt { background: #fafafa; }
.section-dark { background: #1a1a1a; }
.section-badge { display: inline-block; background: #dcfce7; color: #2d6a4f; padding: 4px 14px; border-radius: 100px; font-size: 0.8em; font-weight: 600; margin-bottom: 16px; }
.section-badge-dark { display: inline-block; background: #1e3a2e; color: #4ade80; padding: 4px 14px; border-radius: 100px; font-size: 0.8em; font-weight: 600; margin-bottom: 16px; }
.section-title { font-size: 2.2em; font-weight: 800; color: #1a1a1a; margin-bottom: 16px; line-height: 1; white-space: nowrap; }
.section-title-white { font-size: 2.2em; font-weight: 800; color: #ffffff; margin-bottom: 16px; }
.section-text { color: #666; font-size: 1em; line-height: 1.8; margin-bottom: 24px; }
.section-text-white { color: #aaaaaa; font-size: 1em; line-height: 1.8; }
.program-card { background: white; border-radius: 16px; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; border-top: 4px solid #2d6a4f; height: 100%; }
.program-title { font-size: 1.3em; font-weight: 800; color: #1a1a1a; margin-bottom: 12px; }
.program-text { color: #666; font-size: 0.95em; line-height: 1.7; }
.gift-card { background: white; border-radius: 12px; padding: 24px; border: 1px solid #f0f0f0; margin-bottom: 16px; display: flex; gap: 16px; align-items: flex-start; }
.gift-icon { font-size: 1.8em; flex-shrink: 0; }
.gift-amount { font-size: 1.1em; font-weight: 700; color: #2d6a4f; margin-bottom: 4px; }
.gift-desc { color: #666; font-size: 0.88em; line-height: 1.6; }
.tags-section { padding: 40px 80px; background: white; text-align: center; border-top: 1px solid #f0f0f0; border-bottom: 1px solid #f0f0f0; }
.tags-label { color: #888; font-size: 0.85em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px; }
.support-tag { display: inline-block; background: #f8f8f8; color: #444; padding: 8px 16px; border-radius: 100px; font-size: 0.88em; font-weight: 500; margin: 4px; border: 1px solid #eeeeee; }
.volunteer-section { background: #f0fdf4; padding: 60px 80px; text-align: center; border-top: 1px solid #dcfce7; }
.footer-section { background: #111111; padding: 40px 80px; text-align: center; }
.footer-text { color: #555; font-size: 0.85em; line-height: 2; }
.footer-link { color: #4ade80; text-decoration: none; }
.dashboard-header { background: linear-gradient(135deg, #1a1a1a 0%, #2d6a4f 100%); padding: 32px 40px; margin-bottom: 0; }
.dashboard-title { color: white; font-size: 1.8em; font-weight: 800; margin-bottom: 4px; }
.dashboard-sub { color: #a8d5b5; font-size: 0.9em; }
.emergency-banner { background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; padding: 20px 32px; text-align: center; margin-bottom: 0; }
.emergency-title { font-size: 1.05em; font-weight: 700; margin-bottom: 4px; }
.emergency-sub { font-size: 0.85em; opacity: 0.85; }
.sidebar-profile { background: linear-gradient(135deg, #1a1a1a, #2d6a4f); padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 16px; }
.sidebar-name { color: white; font-weight: 700; font-size: 1em; margin-top: 8px; }
.sidebar-role { color: #a8d5b5; font-size: 0.8em; }
.stTextInput > div > div > input { border-radius: 8px !important; border: 1.5px solid #e8e8e8 !important; padding: 12px 16px !important; }
.stTextInput > div > div > input:focus { border-color: #2d6a4f !important; box-shadow: 0 0 0 3px rgba(45,106,79,0.1) !important; }
.stSelectbox > div > div { border-radius: 8px !important; }
.stTextArea > div > div > textarea { border-radius: 8px !important; }
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; transition: all 0.2s !important; background: #2d6a4f !important; color: white !important; border: none !important; }
.stButton > button[kind="primary"] { background: #2d6a4f !important; border: none !important; color: white !important; }
.stButton > button[kind="primary"]:hover { background: #1e4d38 !important; transform: translateY(-1px) !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
if "name" not in st.session_state:
    st.session_state.name = None
if "email" not in st.session_state:
    st.session_state.email = None
if "student_tab" not in st.session_state:
    st.session_state.student_tab = "submit"
if "staff_tab" not in st.session_state:
    st.session_state.staff_tab = "all"

def logout():
    for key in ["user", "role", "name", "email"]:
        st.session_state[key] = None
    st.session_state.page = "landing"
    st.session_state.student_tab = "submit"
    st.session_state.staff_tab = "all"

def call_api(payload):
    try:
        res = requests.get(
            SCRIPT_URL,
            params=payload,
            timeout=30,
            allow_redirects=True
        )
        text = res.text.strip()
        if not text:
            return {"status": "error", "message": "Empty response"}
        return json.loads(text)
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"JSON error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_status_color(status):
    if status == "Pending":
        return "🟡"
    elif status == "In Progress":
        return "🔵"
    elif status == "Resolved":
        return "✅"
    return "⚪"

# ══════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":

    col_logo, col_space, col_btns = st.columns([3, 0.1, 4])
    with col_logo:
        st.markdown('<img src="https://images.squarespace-cdn.com/content/v1/5e20c115d763a90de6f29cae/b3f5e6ff-7104-4b29-aa4d-ecb59ef49f3a/New+Logo.png?format=1500w" style="height:75px; object-fit:contain; margin-top:8px;">', unsafe_allow_html=True)
    with col_btns:
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            st.markdown('<a href="https://www.zeffy.com/en-US/donation-form/behind-the-introduction-international-student-support-fundraiser" target="_blank"><button style="background:#2d6a4f; color:white; padding:9px 12px; border:none; border-radius:8px; font-size:0.85em; font-weight:600; cursor:pointer; width:100%;">Donate</button></a>', unsafe_allow_html=True)
        with b2:
            st.markdown('<a href="https://www.volunteermatch.org/search/org1194340.jsp" target="_blank"><button style="background:#2d6a4f; color:white; padding:9px 12px; border:none; border-radius:8px; font-size:0.85em; font-weight:600; cursor:pointer; width:100%;">Volunteer</button></a>', unsafe_allow_html=True)
        with b3:
            if st.button("Get Help", use_container_width=True, key="nb_help"):
                st.session_state.page = "signup"
                st.rerun()
        with b4:
            if st.button("Log In", use_container_width=True, key="nb_login"):
                st.session_state.page = "login"
                st.rerun()
        with b5:
            if st.button("Sign Up", use_container_width=True, key="nb_signup"):
                st.session_state.page = "signup"
                st.rerun()
    st.markdown("<hr style='margin:0; border-color:#e8e8e8;'>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✦ Serving Chicago Since 2020</div>
        <div class="hero-title">Education is the<br><span>Path Forward</span></div>
        <div class="hero-tagline">con cariño — with love and care</div>
        <div class="hero-subtitle">
            Chicago Education Advocacy Cooperative (ChiEAC) serves the needs
            of Chicago students and families. We champion educational equity
            and social justice — fighting alongside Black and Latino students
            and families seeking practical pathways to upward social mobility.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,2,0.5,2,0.5,2,1])
    with col2:
        st.markdown('<div class="stat-item"><div class="stat-number">1,600+</div><div class="stat-label">Students Served</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-item"><div class="stat-number">2020</div><div class="stat-label">Year Founded</div></div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="stat-item"><div class="stat-number">K–12+</div><div class="stat-label">Education Levels</div></div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#f0f0f0; margin:0;'>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div class="section-badge">Our Programs</div>
        <div class="section-title">ELEVATE & IMPACT</div>
        <div class="section-text">
            ChiEAC was founded in January 2020 with the vision of providing
            practical pathways to upward social mobility. We have since expanded
            to include K-12 and Adult Education serving over 1,600 students and counting.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="program-card">
                <div style="font-size:2em; margin-bottom:16px;">🚀</div>
                <div class="program-title">ELEVATE</div>
                <div class="program-text">We create custom professional opportunities for rising scholars. Mentorship, tutoring, and culturally grounded college and career guidance for every student we serve.</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="program-card">
                <div style="font-size:2em; margin-bottom:16px;">🤝</div>
                <div class="program-title">IMPACT</div>
                <div class="program-text">We serve as first-responder advocates to students and families in need — from food and rent assistance to mental health resources and legal help.</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="tags-section">
        <div class="tags-label">We help with</div>
        <span class="support-tag">🍎 Food</span>
        <span class="support-tag">🏠 Rent</span>
        <span class="support-tag">🚍 Transportation</span>
        <span class="support-tag">💻 Technology</span>
        <span class="support-tag">📚 School Supplies</span>
        <span class="support-tag">🧠 Mental Health</span>
        <span class="support-tag">⚖️ Legal Help</span>
        <span class="support-tag">💼 Career Readiness</span>
        <span class="support-tag">🏡 Housing</span>
        <span class="support-tag">🏥 Healthcare</span>
    </div>
    """, unsafe_allow_html=True)

    
    st.markdown("""
    <div style="background:#fafafa; padding:40px 80px;">
    <div class="section-title">Make a Real Difference in Chicago Communities</div>
    <div class="section-text">
        We started ChiEAC using the retirement savings of Dr. Drury and have been
        sustained using contributions from our community. We have NEVER relied on
        grants to provide our services. When you give to the ChiEAC Community
        Impact Fund, you are changing lives.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="gift-card"><div class="gift-icon">📱</div><div><div class="gift-amount">$65 gives a lifeline</div><div class="gift-desc">Provides a newly arrived migrant family with a phone, unlimited data, and hotspot access for one month.</div></div></div>
        <div class="gift-card"><div class="gift-icon">🚍</div><div><div class="gift-amount">$25 opens a door</div><div class="gift-desc">Covers public transit for students and parents to get to school, legal appointments, or medical care.</div></div></div>
        <div class="gift-card"><div class="gift-icon">📚</div><div><div class="gift-amount">$100 empowers a student</div><div class="gift-desc">Supports a young person in our ELEVATE Program with mentorship, tutoring, and college guidance.</div></div></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="gift-card"><div class="gift-icon">💼</div><div><div class="gift-amount">$150 prepares a future</div><div class="gift-desc">Funds career readiness training through our IMPACT Program including resume support and job coaching.</div></div></div>
        <div class="gift-card"><div class="gift-icon">🧠</div><div><div class="gift-amount">$200 brings healing</div><div class="gift-desc">Supports trauma-informed mental health sessions for families who have endured displacement or poverty.</div></div></div>
        <div class="gift-card"><div class="gift-icon">⚖️</div><div><div class="gift-amount">$500 provides hope</div><div class="gift-desc">Helps grow our volunteer legal clinic where families receive guidance on asylum cases and work permits.</div></div></div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<a href="https://www.zeffy.com/en-US/donation-form/behind-the-introduction-international-student-support-fundraiser" target="_blank"><button style="background:#2d6a4f; color:white; padding:14px 32px; border:none; border-radius:8px; font-size:1em; font-weight:600; cursor:pointer; width:100%;">Support ChiEAC Students — Donate Now</button></a>', unsafe_allow_html=True)
    

    st.markdown('<div style="padding: 60px 80px; background: white; text-align:center;"><div class="section-badge">Our Impact</div><div class="section-title" style="text-align:center; margin-bottom:8px;">See Our Work in Action</div><div style="color:#666; margin-bottom:32px;">Real stories from our students and community</div>', unsafe_allow_html=True)

    
    if "video_page" not in st.session_state:
        st.session_state.video_page = 0

    all_videos = [
        "https://www.instagram.com/reel/DVv4x0-DQmI/embed/",
        "https://www.instagram.com/reel/DZXwWIixciX/embed/",
        "https://www.instagram.com/reel/DbbQbdVR3f_/embed/",
        "https://www.instagram.com/reel/DbdidkqxaKM/embed/",
        "https://www.instagram.com/reel/DbTCXfYxs51/embed/",
        "https://www.instagram.com/reel/Da0Pfr-x3aL/embed/",
        "https://www.instagram.com/reel/DarNRwouNsW/embed/",
        "https://www.instagram.com/reel/DaOdTgHhzzU/embed/",
        "https://www.instagram.com/reel/DZ7ucoqRg9y/embed/",
        "https://www.instagram.com/reel/DZBbgxtB1ii/embed/",
    ]

    start = st.session_state.video_page * 3
    current_videos = all_videos[start:start+3]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, video_url in enumerate(current_videos):
        with cols[i]:
            st.markdown(f'<div style="overflow:hidden; height:480px; border-radius:12px;"><iframe src="{video_url}" width="100%" height="800" frameborder="0" scrolling="no" allowtransparency="true" allow="encrypted-media" style="border:none; margin-top:-130px;"></iframe></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns([2, 1, 2])
    with nav2:
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("◀ Prev", disabled=st.session_state.video_page == 0, key="vid_prev"):
                st.session_state.video_page -= 1
                st.rerun()
        with col_next:
            if st.button("Next ▶", disabled=start + 3 >= len(all_videos), key="vid_next"):
                st.session_state.video_page += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True) 

    st.markdown("""
    <div class="volunteer-section">
        <div class="section-badge">Get Involved</div>
        <div class="section-title" style="text-align:center;">Volunteer With Us</div>
        <div class="section-text" style="text-align:center; max-width:600px; margin: 0 auto 24px auto;">
            We rely on volunteers to help us provide these vital services.
            Whether you have time to mentor or assist at events, your involvement
            helps us empower students to achieve their goals.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<a href="https://www.volunteermatch.org/search/org1194340.jsp" target="_blank"><button style="background:#2d6a4f; color:white; padding:14px 32px; border:none; border-radius:8px; font-size:1em; font-weight:600; cursor:pointer; width:100%;">Volunteer With ChiEAC</button></a>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section section-dark">
        <div style="text-align:center;">
            <div class="section-badge-dark">Why ChiEAC</div>
            <div class="section-title-white">We do more with less<br>because we care more</div>
            <div class="section-text-white" style="max-width:680px; margin: 0 auto;">
                Since 2020, ChiEAC has served over 500 families stretching every dollar
                through volunteer power, partnerships, and deep trust in the community.
                We listen more, care more, and show up where others do not.
                Together, we can build a Chicago where every family has a fair chance.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-section">
        <div class="footer-text">
            <strong style="color:#ffffff;">Chicago Education Advocacy Cooperative (ChiEAC)</strong><br>
            EIN: 84-4211875 &nbsp;|&nbsp;
            <a href="mailto:benjamin@chieac.org" class="footer-link">benjamin@chieac.org</a> &nbsp;|&nbsp;
            773-599-0267<br><br>
            <a href="https://chieac.org/s/FormAG990ILCharitableOrganizationAnnualReport.pdf" class="footer-link">2024 Taxes</a> &nbsp;|&nbsp;
            <a href="https://chieac.org/s/CHIEAC-2023-IL-990-T.pdf" class="footer-link">2023 Taxes</a> &nbsp;|&nbsp;
            <a href="https://chieac.org/s/form-8879.pdf" class="footer-link">2022 Taxes</a> &nbsp;|&nbsp;
            <a href="https://chieac.org/s/form-8879-TE.pdf" class="footer-link">2021 Taxes</a><br><br>
            © 2026 ChiEAC — Serving Chicago communities con cariño since 2020
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIGNUP PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "signup":

    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown('<div style="padding: 8px 0;"><img src="https://images.squarespace-cdn.com/content/v1/5e20c115d763a90de6f29cae/b3f5e6ff-7104-4b29-aa4d-ecb59ef49f3a/New+Logo.png?format=1500w" style="height:50px; object-fit:contain;"></div>', unsafe_allow_html=True)
    with col3:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Log In", use_container_width=True, key="signup_login"):
                st.session_state.page = "login"
                st.rerun()
        with c2:
            if st.button("← Home", use_container_width=True, key="signup_home"):
                st.session_state.page = "landing"
                st.rerun()

    st.markdown("<hr style='margin:0; border-color:#e8e8e8;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:2.5em;">🎓</div>
            <div style="font-size:1.8em; font-weight:800; color:#1a1a1a; margin-bottom:8px;">Create Your Account</div>
            <div style="color:#888; font-size:0.92em;">Join ChiEAC and get the support you need</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("signup_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                full_name = st.text_input("Full Name *", placeholder="Your full name")
                email = st.text_input("Email Address *", placeholder="your@email.com")
                password = st.text_input("Password *", type="password", placeholder="Create a password")
                address = st.text_input("Address *", placeholder="Street address, City, State, ZIP")
            with col_b:
                username = st.text_input("Username *", placeholder="Choose a username")
                phone = st.text_input("Phone Number *", placeholder="(xxx) xxx-xxxx")
                confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Repeat your password")
                dob = st.date_input("Date of Birth *")

            gender = st.selectbox("Gender *", ["Select...", "Female", "Male", "Non-binary", "Prefer not to say", "Other"])
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Create Account →", use_container_width=True, type="primary")

            if submitted:
                if not all([full_name, username, email, phone, password, confirm_password, address]):
                    st.error("Please fill in all required fields!")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters!")
                elif gender == "Select...":
                    st.error("Please select your gender!")
                else:
                    result = call_api({
                        "action": "register",
                        "name": full_name,
                        "phone": phone,
                        "email": email,
                        "password": password,
                        "address": address,
                        "dob": str(dob),
                        "gender": gender,
                        "username": username
                    })
                    if result.get("status") == "success":
                        st.success("✅ Account created successfully! Please log in.")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('message', 'Something went wrong. Please try again.')}")

        st.markdown('<div style="text-align:center; margin-top:16px; color:#888; font-size:0.88em;">Already have an account?</div>', unsafe_allow_html=True)
        if st.button("Log In Instead", use_container_width=True, key="signup_to_login"):
            st.session_state.page = "login"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "login":

    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown('<div style="padding: 16px 0;"><span style="font-size:1.5em; font-weight:900; color:#1a1a1a;">Chi<span style="color:#2d6a4f;">EAC</span></span></div>', unsafe_allow_html=True)
    with col3:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Home", use_container_width=True, key="login_home"):
                st.session_state.page = "landing"
                st.rerun()
        with c2:
            if st.button("Sign Up", use_container_width=True, type="primary", key="login_signup"):
                st.session_state.page = "signup"
                st.rerun()

    st.markdown("<hr style='margin:0; border-color:#e8e8e8;'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:2.5em;">👋</div>
            <div style="font-size:1.8em; font-weight:800; color:#1a1a1a; margin-bottom:8px;">Welcome Back</div>
            <div style="color:#888; font-size:0.92em;">Sign in to your ChiEAC account</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                if username and password:
                    result = call_api({
                        "action": "login",
                        "username": username,
                        "password": password
                    })
                    if result.get("status") == "success":
                        st.session_state.user = username
                        st.session_state.role = result.get("role")
                        st.session_state.name = result.get("name")
                        st.session_state.email = result.get("email")
                        if result.get("role") == "staff":
                            st.session_state.page = "staff_dashboard"
                        else:
                            st.session_state.page = "student_dashboard"
                        st.rerun()
                    else:
                        st.error("❌ Incorrect username or password. Please try again.")
                else:
                    st.error("Please enter your username and password!")

        st.markdown('<div style="text-align:center; margin-top:16px; color:#888; font-size:0.88em;">Don\'t have an account yet?</div>', unsafe_allow_html=True)
        if st.button("Create an Account", use_container_width=True, key="login_to_signup"):
            st.session_state.page = "signup"
            st.rerun()

        st.markdown('<div style="text-align:center; margin-top:12px; color:#999; font-size:0.82em;">Need help? Contact us at <a href="mailto:benjamin@chieac.org" style="color:#2d6a4f;">benjamin@chieac.org</a></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# STUDENT DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "student_dashboard":

    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()

    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-profile">
            <div style="font-size:2em;">🎓</div>
            <div class="sidebar-name">{st.session_state.name}</div>
            <div class="sidebar-role">Student</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Menu**")
        if st.button("📝 Submit Request", use_container_width=True):
            st.session_state.student_tab = "submit"
        if st.button("📋 My Requests", use_container_width=True):
            st.session_state.student_tab = "history"
        if st.button("👤 My Profile", use_container_width=True):
            st.session_state.student_tab = "profile"
        if st.button("📚 Resources", use_container_width=True):
            st.session_state.student_tab = "resources"
        if st.button("📞 Contact ChiEAC", use_container_width=True):
            st.session_state.student_tab = "contact"
        if st.button("❓ FAQ", use_container_width=True):
            st.session_state.student_tab = "faq"
        if st.button("📈 My Progress", use_container_width=True):
            st.session_state.student_tab = "progress"
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

        st.rerun()
    

    st.markdown("""
    <div class="emergency-banner">
        <div class="emergency-title">🚨 Need Immediate Help?</div>
        <div class="emergency-sub">Click the button below if you are in an emergency situation</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚨 EMERGENCY — I Need Help RIGHT NOW!", use_container_width=True, type="primary"):
        result = call_api({
            "action": "submit_request",
            "username": st.session_state.user,
            "name": st.session_state.name,
            "email": st.session_state.email,
            "phone": "",
            "neighborhood": "",
            "support_type": "EMERGENCY",
            "urgency": "Critical - Need help today",
            "description": f"EMERGENCY REQUEST from {st.session_state.name} — Needs immediate assistance!"
        })
        send_emergency_email(st.session_state.name, st.session_state.email)
        st.error("🚨 Emergency alert sent! ChiEAC staff will contact you immediately. If urgent call 773-599-0267")

    st.markdown("---")

    if st.session_state.student_tab == "submit":
        st.markdown("### 📝 Submit a Support Request")
        st.markdown("Tell us how we can help. We respond as quickly as possible.")
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("student_request_form"):
            col1, col2 = st.columns(2)
            with col1:
                name_input = st.text_input("Full Name *", value=st.session_state.name)
                email_input = st.text_input("Email *", value=st.session_state.email)
            with col2:
                phone = st.text_input("Phone Number", placeholder="(xxx) xxx-xxxx")
                neighborhood = st.text_input("Neighborhood / ZIP Code *", placeholder="e.g. Pilsen, 60608")

            col1, col2 = st.columns(2)
            with col1:
                support_type = st.selectbox("Type of Support *",
                    ["Select...", "Food", "Rent", "Transportation", "Technology",
                     "School Supplies", "Mental Health", "Housing", "Legal Help",
                     "Career Readiness", "Other"])
            with col2:
                urgency = st.selectbox("How urgent is this? *",
                    ["Select...", "Critical - Need help today",
                     "High - Need help this week",
                     "Medium - Need help this month",
                     "Low - Planning ahead"])

            description = st.text_area("Describe your situation *", height=160,
                placeholder="Please describe what you need help with. The more details you share the better we can support you.")

            submitted = st.form_submit_button("Submit Request →", use_container_width=True, type="primary")

            if submitted:
                if name_input and email_input and support_type != "Select..." and urgency != "Select..." and description and neighborhood:
                    result = call_api({
                        "action": "submit_request",
                        "username": st.session_state.user,
                        "name": name_input,
                        "email": email_input,
                        "phone": phone,
                        "neighborhood": neighborhood,
                        "support_type": support_type,
                        "urgency": urgency,
                        "description": description
                    })
                    if result.get("status") == "success":
                        send_notification_email(
                            student_name=name_input,
                            support_type=support_type,
                            urgency=urgency,
                            description=description,
                            neighborhood=neighborhood,
                            phone=phone,
                            email=email_input
                        )
                        st.success("✅ Your request has been submitted! A ChiEAC team member will reach out soon.")
                        st.balloons()
                    else:
                        st.error("Something went wrong. Please try again or call 773-599-0267")
                else:
                    st.error("Please fill in all required fields!")

    elif st.session_state.student_tab == "history":
        st.markdown("### 📋 My Past Requests")
        st.markdown("Track the status of your support requests below.")
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]
            my_requests = df[df["Email"] == st.session_state.email]
            if len(my_requests) > 0:
                for _, row in my_requests.iterrows():
                    status_icon = get_status_color(row["Status"])
                    with st.expander(f"{status_icon} {row['Support Type']} — {row['Urgency']} | {row['Status']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Submitted:** {row['Timestamp']}")
                            st.markdown(f"**Support Type:** {row['Support Type']}")
                            st.markdown(f"**Urgency:** {row['Urgency']}")
                        with col2:
                            st.markdown(f"**Status:** {status_icon} {row['Status']}")
                            if row['Status'] == "Pending":
                                st.markdown("*Your request is being reviewed by ChiEAC staff.*")
                            elif row['Status'] == "In Progress":
                                st.markdown("*ChiEAC staff are actively working on your request!*")
                            elif row['Status'] == "Resolved":
                                st.markdown("*Your request has been resolved!*")
                        st.markdown(f"**Description:** {row['Description']}")
            else:
                st.info("You have not submitted any requests yet.")
        except Exception as e:
            st.info("Request history coming soon! Contact benjamin@chieac.org for updates.")
    elif st.session_state.student_tab == "profile":
        st.markdown("### 👤 My Profile")
        st.markdown("Your personal information on file with ChiEAC.")
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Users"
            df = pd.read_csv(USERS_URL)
            df.columns = ["Name", "Phone", "Email", "Password", "Address", "DOB", "Gender", "Username", "Role"]
            user_data = df[df["Username"] == st.session_state.user]
            if len(user_data) > 0:
                row = user_data.iloc[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Full Name:** {row['Name']}")
                    st.markdown(f"**Email:** {row['Email']}")
                    st.markdown(f"**Phone:** {row['Phone']}")
                    st.markdown(f"**Gender:** {row['Gender']}")
                with col2:
                    st.markdown(f"**Username:** {row['Username']}")
                    st.markdown(f"**Date of Birth:** {row['DOB']}")
                    st.markdown(f"**Address:** {row['Address']}")
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("To update your information please contact benjamin@chieac.org or call 773-599-0267")
        except Exception as e:
            st.info("Profile loading. Contact benjamin@chieac.org for help.")

    elif st.session_state.student_tab == "resources":
        st.markdown("### 📚 Chicago Community Resources")
        st.markdown("Helpful resources for students and families in Chicago.")
        st.markdown("<br>", unsafe_allow_html=True)

        resources = [
            ("🍎 Food Resources", [
                ("Greater Chicago Food Depository", "773-247-3663", "chicagosfoodbank.org"),
                ("Chicago Community Kitchens", "312-563-9400", "chicagocommunity.org"),
                ("SNAP Benefits", "800-843-6154", "dhs.state.il.us"),
            ]),
            ("🏠 Housing Resources", [
                ("Chicago Housing Authority", "312-742-8500", "thecha.org"),
                ("Interfaith Housing Center", "847-823-1100", "interfaithhousing.org"),
                ("Emergency Housing Hotline", "312-744-5000", "cityofchicago.org"),
            ]),
            ("🧠 Mental Health Resources", [
                ("NAMI Chicago", "833-626-4244", "namichicago.org"),
                ("Chicago Behavioral Hospital", "800-890-1423", "chicagobehavioral.org"),
                ("Crisis Text Line", "Text HOME to 741741", "crisistextline.org"),
            ]),
            ("⚖️ Legal Resources", [
                ("Legal Aid Chicago", "312-341-1070", "legalaidchicago.org"),
                ("Chicago Legal Clinic", "773-731-1762", "clclaw.org"),
                ("Illinois Legal Aid Online", "800-252-8966", "illinoislegalaid.org"),
            ]),
            ("💼 Career Resources", [
                ("Chicago Cook Workforce Partnership", "312-603-0200", "workforceboard.org"),
                ("City Colleges of Chicago", "773-COLLEGE", "ccc.edu"),
                ("Illinois WorkNet", "888-367-4382", "illinoisworknet.com"),
            ]),
        ]

        for category, items in resources:
            st.markdown(f"#### {category}")
            for name, phone, website in items:
                st.markdown(f"""
                <div style="background:white; border-radius:8px; padding:16px; margin-bottom:8px; border:1px solid #f0f0f0;">
                    <strong style="color:#1a1a1a;">{name}</strong><br>
                    <span style="color:#666; font-size:0.9em;">📞 {phone} &nbsp;|&nbsp; 🌐 {website}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

    elif st.session_state.student_tab == "contact":
        st.markdown("### 📞 Contact ChiEAC")
        st.markdown("We are here to help. Reach out to us anytime!")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background:white; border-radius:12px; padding:24px; border:1px solid #f0f0f0; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <h4 style="color:#2d6a4f; margin-bottom:16px;">Get In Touch</h4>
                <p>📞 <strong>Phone:</strong> 773-599-0267</p>
                <p>📧 <strong>Email:</strong> benjamin@chieac.org</p>
                <p>📍 <strong>Address:</strong> 1156 E 61st St, Chicago, IL 60637</p>
                <p>🌐 <strong>Website:</strong> chieac.org</p>
                <p>📸 <strong>Instagram:</strong> @wearechieac</p>
                <p>▶️ <strong>YouTube:</strong> @chicagoeducated</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:white; border-radius:12px; padding:24px; border:1px solid #f0f0f0; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <h4 style="color:#2d6a4f; margin-bottom:16px;">Office Hours</h4>
                <p>Monday to Friday</p>
                <p>9:00 AM to 5:00 PM CST</p>
                <br>
                <p style="color:#666; font-size:0.9em;">For emergencies outside office hours please use the Emergency button on your dashboard or call 911.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#f0fdf4; border-radius:12px; padding:24px; border:1px solid #dcfce7; text-align:center;">
            <h4 style="color:#2d6a4f;">Follow Us</h4>
            <p style="color:#666;">Stay updated with ChiEAC news and events</p>
            <a href="https://www.instagram.com/wearechieac/" target="_blank" style="margin:8px; display:inline-block;">
                <button style="background:#2d6a4f; color:white; padding:10px 20px; border:none; border-radius:6px; font-weight:600; cursor:pointer;">Instagram</button>
            </a>
            <a href="https://www.youtube.com/@chicagoeducated" target="_blank" style="margin:8px; display:inline-block;">
                <button style="background:#2d6a4f; color:white; padding:10px 20px; border:none; border-radius:6px; font-weight:600; cursor:pointer;">YouTube</button>
            </a>
            <a href="https://www.linkedin.com/company/chieac" target="_blank" style="margin:8px; display:inline-block;">
                <button style="background:#2d6a4f; color:white; padding:10px 20px; border:none; border-radius:6px; font-weight:600; cursor:pointer;">LinkedIn</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.student_tab == "faq":
        st.markdown("### ❓ Frequently Asked Questions")
        st.markdown("<br>", unsafe_allow_html=True)

        faqs = [
            ("How long does it take to process my request?",
             "Our team typically responds within 24 to 48 hours. For critical requests we respond as soon as possible."),
            ("What programs does ChiEAC offer?",
             "ChiEAC offers two core programs. ELEVATE creates custom professional opportunities for rising scholars including mentorship and college guidance. IMPACT serves as first-responder advocates for students and families in need providing direct support for food, rent, transportation and more."),
            ("How do I update my personal information?",
             "Please contact us at benjamin@chieac.org or call 773-599-0267 and our team will update your information."),
            ("Can I submit multiple support requests?",
             "Yes you can submit as many requests as you need. Each request is tracked separately and our team will respond to each one."),
            ("Is my information kept confidential?",
             "Yes. All personal information you provide is kept strictly confidential and is only used to provide you with the support you need."),
            ("What should I do in an emergency?",
             "Click the red EMERGENCY button on your dashboard immediately. Our staff will be alerted right away. For life threatening emergencies please call 911."),
            ("How can I volunteer with ChiEAC?",
             "We love volunteers! Visit volunteermatch.org/search/org1194340.jsp to see current volunteer opportunities with ChiEAC."),
            ("How can I donate to ChiEAC?",
             "You can donate at zeffy.com/en-US/donation-form/behind-the-introduction-international-student-support-fundraiser. Every dollar helps us serve more students and families."),
        ]

        for question, answer in faqs:
            with st.expander(f"❓ {question}"):
                st.markdown(f"{answer}")

    elif st.session_state.student_tab == "progress":
        st.markdown("### 📈 My Progress")
        st.markdown("Track your journey with ChiEAC.")
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]
            my_requests = df[df["Email"] == st.session_state.email]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Requests", len(my_requests))
            with col2:
                resolved = len(my_requests[my_requests["Status"] == "Resolved"])
                st.metric("✅ Resolved", resolved)
            with col3:
                pending = len(my_requests[my_requests["Status"] == "Pending"])
                st.metric("🟡 Pending", pending)

            st.markdown("<br>", unsafe_allow_html=True)

            if len(my_requests) > 0:
                st.markdown("#### Your Request History")
                for _, row in my_requests.iterrows():
                    status_icon = get_status_color(row["Status"])
                    st.markdown(f"""
                    <div style="background:white; border-radius:8px; padding:16px; margin-bottom:8px; border:1px solid #f0f0f0; border-left:4px solid #2d6a4f;">
                        <strong>{row['Support Type']}</strong> &nbsp;|&nbsp;
                        <span style="color:#666; font-size:0.9em;">{row['Urgency']}</span> &nbsp;|&nbsp;
                        {status_icon} <span style="font-size:0.9em;">{row['Status']}</span> &nbsp;|&nbsp;
                        <span style="color:#888; font-size:0.85em;">{row['Timestamp']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("You have not submitted any requests yet. Submit your first request to start tracking your progress!")

        except Exception as e:
            st.info("Progress tracking coming soon!")
# ══════════════════════════════════════════════════════════════
# STAFF DASHBOARD
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "staff_dashboard":

    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()

    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-profile">
            <div style="font-size:2em;">👩‍💼</div>
            <div class="sidebar-name">{st.session_state.name}</div>
            <div class="sidebar-role">Staff Member</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Menu**")
        if st.button("📊 All Requests", use_container_width=True):
            st.session_state.staff_tab = "all"
        if st.button("🚨 Emergencies", use_container_width=True):
            st.session_state.staff_tab = "emergency"
        if st.button("👥 All Students", use_container_width=True):
            st.session_state.staff_tab = "students"
        if st.button("📝 Submit for Student", use_container_width=True):
            st.session_state.staff_tab = "submit"
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.staff_tab = "analytics"
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">Staff Dashboard 📊</div>
        <div class="dashboard-sub">Real time student support request management</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.staff_tab == "all":
        st.markdown("### 📊 All Student Requests")
        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]

            emergency_count = len(df[df["Support Type"] == "EMERGENCY"])
            if emergency_count > 0:
                st.error(f"🚨 {emergency_count} EMERGENCY REQUEST(S) NEED IMMEDIATE ATTENTION!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Requests", len(df))
            with col2:
                st.metric("🔴 Critical", len(df[df["Urgency"] == "Critical - Need help today"]))
            with col3:
                st.metric("🟠 High", len(df[df["Urgency"] == "High - Need help this week"]))
            with col4:
                st.metric("🟡 Pending", len(df[df["Status"] == "Pending"]))

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                urgency_filter = st.selectbox("Filter by Urgency",
                    ["All", "Critical - Need help today", "High - Need help this week",
                     "Medium - Need help this month", "Low - Planning ahead"])
            with col2:
                type_filter = st.selectbox("Filter by Type",
                    ["All", "Food", "Rent", "Transportation", "Technology",
                     "School Supplies", "Mental Health", "Housing", "Legal Help",
                     "Career Readiness", "EMERGENCY", "Other"])
            with col3:
                status_filter = st.selectbox("Filter by Status",
                    ["All", "Pending", "In Progress", "Resolved"])

            filtered = df.copy()
            if urgency_filter != "All":
                filtered = filtered[filtered["Urgency"] == urgency_filter]
            if type_filter != "All":
                filtered = filtered[filtered["Support Type"] == type_filter]
            if status_filter != "All":
                filtered = filtered[filtered["Status"] == status_filter]

            st.markdown(f"**Showing {len(filtered)} of {len(df)} requests**")
            st.markdown("<br>", unsafe_allow_html=True)

            for idx, row in filtered.iterrows():
                status_icon = get_status_color(row["Status"])
                with st.expander(f"{status_icon} {row['Name']} — {row['Support Type']} | {row['Urgency']} | {row['Status']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Name:** {row['Name']}")
                        st.markdown(f"**Email:** {row['Email']}")
                        st.markdown(f"**Phone:** {row['Phone'] if row['Phone'] else 'Not provided'}")
                        st.markdown(f"**Neighborhood:** {row['Neighborhood'] if row['Neighborhood'] else 'Not provided'}")
                    with col2:
                        st.markdown(f"**Support Type:** {row['Support Type']}")
                        st.markdown(f"**Urgency:** {row['Urgency']}")
                        st.markdown(f"**Submitted:** {row['Timestamp']}")
                        st.markdown(f"**Current Status:** {status_icon} {row['Status']}")

                    st.markdown(f"**Description:** {row['Description']}")
                    st.markdown("---")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Pending", "In Progress", "Resolved"],
                            index=["Pending", "In Progress", "Resolved"].index(row["Status"]) if row["Status"] in ["Pending", "In Progress", "Resolved"] else 0,
                            key=f"status_{idx}"
                        )
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("Update →", key=f"btn_{idx}", type="primary"):
                            result = call_api({
                                "action": "update_status",
                                "name": row["Name"],
                                "email": row["Email"],
                                "new_status": new_status
                            })
                            if result.get("status") == "success":
                                st.success(f"✅ Status updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error(f"Could not update: {result.get('message', 'Please try again')}")

        except Exception as e:
            st.error(f"Error loading requests: {e}")

    elif st.session_state.staff_tab == "emergency":
        st.markdown("### 🚨 Emergency Requests")
        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]
            emergency_df = df[df["Support Type"] == "EMERGENCY"]
            if len(emergency_df) > 0:
                st.error(f"🚨 {len(emergency_df)} students need immediate help!")
                st.dataframe(emergency_df, use_container_width=True)
            else:
                st.success("✅ No emergency requests at this time!")
        except Exception as e:
            st.error(f"Error: {e}")

    elif st.session_state.staff_tab == "students":
        st.markdown("### 👥 All Registered Students")
        try:
            USERS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Users"
            df = pd.read_csv(USERS_URL)
            df.columns = ["Name", "Phone", "Email", "Password", "Address", "DOB", "Gender", "Username", "Role"]
            students = df[df["Role"] == "student"][["Name", "Email", "Phone", "Address", "DOB", "Gender", "Username"]]
            st.metric("Total Registered Students", len(students))
            st.dataframe(students, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading students: {e}")

    elif st.session_state.staff_tab == "analytics":
        st.markdown("### 📈 Analytics Dashboard")
        st.markdown("Visual insights into student support requests")
        st.markdown("<br>", unsafe_allow_html=True)

        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Requests", len(df))
            with col2:
                st.metric("✅ Resolved", len(df[df["Status"] == "Resolved"]))
            with col3:
                st.metric("🔵 In Progress", len(df[df["Status"] == "In Progress"]))
            with col4:
                st.metric("🟡 Pending", len(df[df["Status"] == "Pending"]))

            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Support Type Breakdown")
                support_counts = df["Support Type"].value_counts().reset_index()
                support_counts.columns = ["Support Type", "Count"]
                fig1 = px.bar(support_counts, x="Count", y="Support Type", orientation="h",
                    color="Count", color_continuous_scale=["#dcfce7", "#2d6a4f"],
                    title="Requests by Support Type")
                fig1.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                    showlegend=False, coloraxis_showscale=False, height=350)
                st.plotly_chart(fig1, use_container_width=True)

            with col2:
                st.markdown("#### Request Status Overview")
                status_counts = df["Status"].value_counts().reset_index()
                status_counts.columns = ["Status", "Count"]
                fig2 = px.pie(status_counts, values="Count", names="Status",
                    color_discrete_map={"Pending": "#f59e0b", "In Progress": "#3b82f6", "Resolved": "#2d6a4f"},
                    title="Request Status Distribution")
                fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=350)
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Urgency Level Breakdown")
                urgency_counts = df["Urgency"].value_counts().reset_index()
                urgency_counts.columns = ["Urgency", "Count"]
                fig3 = px.bar(urgency_counts, x="Urgency", y="Count", color="Count",
                    color_continuous_scale=["#dcfce7", "#2d6a4f"], title="Requests by Urgency Level")
                fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                    showlegend=False, coloraxis_showscale=False, height=350)
                st.plotly_chart(fig3, use_container_width=True)

            with col2:
                st.markdown("#### Top Neighborhoods Needing Help")
                neighborhood_counts = df["Neighborhood"].value_counts().head(10).reset_index()
                neighborhood_counts.columns = ["Neighborhood", "Count"]
                fig4 = px.bar(neighborhood_counts, x="Count", y="Neighborhood", orientation="h",
                    color="Count", color_continuous_scale=["#dcfce7", "#2d6a4f"],
                    title="Top 10 Neighborhoods by Requests")
                fig4.update_layout(plot_bgcolor="white", paper_bgcolor="white",
                    showlegend=False, coloraxis_showscale=False, height=350)
                st.plotly_chart(fig4, use_container_width=True)

        except Exception as e:
            st.error(f"Error loading analytics: {e}")

    elif st.session_state.staff_tab == "submit":
        st.markdown("### 📝 Submit Request on Behalf of a Student")
        with st.form("staff_submit_form"):
            col1, col2 = st.columns(2)
            with col1:
                name_input = st.text_input("Student Full Name *")
                email_input = st.text_input("Student Email *")
            with col2:
                phone = st.text_input("Phone Number")
                neighborhood = st.text_input("Neighborhood / ZIP Code")

            col1, col2 = st.columns(2)
            with col1:
                support_type = st.selectbox("Type of Support *",
                    ["Select...", "Food", "Rent", "Transportation", "Technology",
                     "School Supplies", "Mental Health", "Housing", "Legal Help",
                     "Career Readiness", "Other"])
            with col2:
                urgency = st.selectbox("Urgency Level *",
                    ["Select...", "Critical - Need help today",
                     "High - Need help this week",
                     "Medium - Need help this month",
                     "Low - Planning ahead"])

            description = st.text_area("Description *", height=150)
            submitted = st.form_submit_button("Submit Request →", use_container_width=True, type="primary")

            if submitted:
                if name_input and email_input and support_type != "Select..." and urgency != "Select..." and description:
                    result = call_api({
                        "action": "submit_request",
                        "username": "staff",
                        "name": name_input,
                        "email": email_input,
                        "phone": phone,
                        "neighborhood": neighborhood,
                        "support_type": support_type,
                        "urgency": urgency,
                        "description": description
                    })
                    if result.get("status") == "success":
                        st.success("✅ Request submitted successfully!")
                    else:
                        st.error("Something went wrong. Please try again.")
                else:
                    st.error("Please fill in all required fields!")