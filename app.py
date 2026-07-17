import streamlit as st
import requests
import pandas as pd
import json

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxf04M03vEURVBzo1JatzAhAvny4-bJVBRgSHYA014KPA6eOql8wGWa0b8TiaB5nrJ9iQ/exec"
SHEET_ID = "1h85m2f6UmE9NPOcHrQnU2_n7GWyL1ZTLhyvbJuUrl94"
REQUESTS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Requests"

st.set_page_config(
    page_title="ChiEAC Support Portal",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background-color: #ffffff; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding-top: 0rem !important; max-width: 100% !important; }

.navbar {
    background: #ffffff;
    border-bottom: 1px solid #e8e8e8;
    padding: 16px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.navbar-brand { font-size: 1.5em; font-weight: 900; color: #1a1a1a; }
.navbar-brand span { color: #2d6a4f; }
.navbar-right { display: flex; gap: 12px; align-items: center; }

.hero-section {
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 60%, #f0fdf4 100%);
    padding: 90px 80px;
    text-align: center;
    border-bottom: 1px solid #e8e8e8;
}
.hero-badge {
    display: inline-block;
    background: #dcfce7;
    color: #2d6a4f;
    padding: 6px 18px;
    border-radius: 100px;
    font-size: 0.85em;
    font-weight: 600;
    margin-bottom: 28px;
    letter-spacing: 0.5px;
}
.hero-title {
    font-size: 3.8em;
    font-weight: 900;
    color: #1a1a1a;
    line-height: 1.1;
    margin-bottom: 20px;
    letter-spacing: -1.5px;
}
.hero-title span { color: #2d6a4f; }
.hero-tagline {
    font-size: 1.1em;
    color: #2d6a4f;
    font-style: italic;
    margin-bottom: 16px;
    font-weight: 500;
}
.hero-subtitle {
    font-size: 1.1em;
    color: #666;
    line-height: 1.8;
    max-width: 640px;
    margin: 0 auto 48px auto;
}

.stats-row {
    display: flex;
    justify-content: center;
    gap: 48px;
    padding: 48px 80px;
    background: #ffffff;
    border-bottom: 1px solid #f0f0f0;
}
.stat-item { text-align: center; }
.stat-number { font-size: 3em; font-weight: 900; color: #2d6a4f; line-height: 1; }
.stat-divider { width: 1px; background: #e8e8e8; }
.stat-label { font-size: 0.85em; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 6px; }

.section { padding: 80px 80px; }
.section-alt { background: #fafafa; }
.section-dark { background: #1a1a1a; }

.section-badge {
    display: inline-block;
    background: #dcfce7;
    color: #2d6a4f;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.8em;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}
.section-badge-dark {
    display: inline-block;
    background: #1e3a2e;
    color: #4ade80;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.8em;
    font-weight: 600;
    margin-bottom: 16px;
}
.section-title { font-size: 2.2em; font-weight: 800; color: #1a1a1a; margin-bottom: 16px; line-height: 1.2; }
.section-title-white { font-size: 2.2em; font-weight: 800; color: #ffffff; margin-bottom: 16px; }
.section-text { color: #666; font-size: 1em; line-height: 1.8; margin-bottom: 24px; }
.section-text-white { color: #aaaaaa; font-size: 1em; line-height: 1.8; }

.program-card {
    background: white;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 8px 24px rgba(0,0,0,0.04);
    border: 1px solid #f0f0f0;
    border-top: 4px solid #2d6a4f;
    height: 100%;
}
.program-title { font-size: 1.3em; font-weight: 800; color: #1a1a1a; margin-bottom: 12px; }
.program-text { color: #666; font-size: 0.95em; line-height: 1.7; }

.gift-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #f0f0f0;
    margin-bottom: 16px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.gift-icon { font-size: 1.8em; flex-shrink: 0; }
.gift-amount { font-size: 1.1em; font-weight: 700; color: #2d6a4f; margin-bottom: 4px; }
.gift-desc { color: #666; font-size: 0.88em; line-height: 1.6; }

.tags-section {
    padding: 40px 80px;
    background: white;
    text-align: center;
    border-top: 1px solid #f0f0f0;
    border-bottom: 1px solid #f0f0f0;
}
.tags-label { color: #888; font-size: 0.85em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px; }
.support-tag {
    display: inline-block;
    background: #f8f8f8;
    color: #444;
    padding: 8px 16px;
    border-radius: 100px;
    font-size: 0.88em;
    font-weight: 500;
    margin: 4px;
    border: 1px solid #eeeeee;
}

.volunteer-section {
    background: #f0fdf4;
    padding: 60px 80px;
    text-align: center;
    border-top: 1px solid #dcfce7;
}

.footer-section {
    background: #111111;
    padding: 40px 80px;
    text-align: center;
}
.footer-text { color: #555; font-size: 0.85em; line-height: 2; }
.footer-link { color: #4ade80; text-decoration: none; }

.login-page {
    min-height: 100vh;
    background: #fafafa;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
}
.login-card {
    background: white;
    border-radius: 20px;
    padding: 48px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border: 1px solid #f0f0f0;
    max-width: 440px;
    width: 100%;
}
.login-icon {
    width: 64px;
    height: 64px;
    background: #dcfce7;
    border-radius: 16px;
    font-size: 1.8em;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px auto;
    text-align: center;
    line-height: 64px;
}
.login-title { font-size: 1.6em; font-weight: 800; color: #1a1a1a; text-align: center; margin-bottom: 6px; }
.login-sub { color: #888; text-align: center; font-size: 0.9em; margin-bottom: 32px; }

.dashboard-header {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d6a4f 100%);
    padding: 32px 40px;
    margin-bottom: 0;
}
.dashboard-title { color: white; font-size: 1.8em; font-weight: 800; margin-bottom: 4px; }
.dashboard-sub { color: #a8d5b5; font-size: 0.9em; }

.emergency-banner {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: white;
    padding: 20px 32px;
    text-align: center;
    margin-bottom: 0;
}
.emergency-title { font-size: 1.05em; font-weight: 700; margin-bottom: 4px; }
.emergency-sub { font-size: 0.85em; opacity: 0.85; }

.sidebar-profile {
    background: linear-gradient(135deg, #1a1a1a, #2d6a4f);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 16px;
}
.sidebar-name { color: white; font-weight: 700; font-size: 1em; margin-top: 8px; }
.sidebar-role { color: #a8d5b5; font-size: 0.8em; }

.stTextInput > div > div > input {
    border-radius: 8px !important;
    border: 1.5px solid #e8e8e8 !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2d6a4f !important;
    box-shadow: 0 0 0 3px rgba(45,106,79,0.1) !important;
}
.stSelectbox > div > div { border-radius: 8px !important; }
.stTextArea > div > div > textarea { border-radius: 8px !important; }
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: #2d6a4f !important;
    border: none !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1e4d38 !important;
    transform: translateY(-1px) !important;
}
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
        res = requests.post(SCRIPT_URL, json=payload, timeout=15)
        return res.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ══════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":

    # Navbar
    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown("""
        <div style="padding: 16px 0;">
            <span style="font-size:1.5em; font-weight:900; color:#1a1a1a;">Chi<span style="color:#2d6a4f;">EAC</span></span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Log In", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with c2:
            if st.button("Sign Up", use_container_width=True, type="primary"):
                st.session_state.page = "signup"
                st.rerun()

    st.markdown("<hr style='margin:0; border-color:#e8e8e8;'>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✦ Serving Chicago Since 2020</div>
        <div class="hero-title">
            Education is the<br>
            <span>Path Forward</span>
        </div>
        <div class="hero-tagline">con cariño — with love and care</div>
        <div class="hero-subtitle">
            Chicago Education Advocacy Cooperative (ChiEAC) serves the needs
            of Chicago students and families. We champion educational equity
            and social justice — fighting alongside Black and Latino students
            and families seeking practical pathways to upward social mobility.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1,2,0.5,2,0.5,2,1])
    with col2:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">1,600+</div>
            <div class="stat-label">Students Served</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">2020</div>
            <div class="stat-label">Year Founded</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div class="stat-item">
            <div class="stat-number">K–12+</div>
            <div class="stat-label">Education Levels</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#f0f0f0; margin:0;'>", unsafe_allow_html=True)

    # Programs
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div class="section-badge">Our Programs</div>
        <div class="section-title">ELEVATE<br>& IMPACT</div>
        <div class="section-text">
            ChiEAC was founded in January 2020 with the vision of providing
            practical pathways to upward social mobility. We have since expanded
            to include K-12 and Adult Education serving over 1,600 students
            and counting.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="program-card">
                <div style="font-size:2em; margin-bottom:16px;">🚀</div>
                <div class="program-title">ELEVATE</div>
                <div class="program-text">
                    We create custom professional opportunities for rising scholars.
                    Mentorship, tutoring, and culturally grounded college and
                    career guidance for every student we serve.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="program-card">
                <div style="font-size:2em; margin-bottom:16px;">🤝</div>
                <div class="program-title">IMPACT</div>
                <div class="program-text">
                    We serve as first-responder advocates to students and families
                    in need — from food and rent assistance to mental health
                    resources and legal help.
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Support tags
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

    # Donations
    st.markdown("<div class='section section-alt'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-badge">Support Our Mission</div>
    <div class="section-title">Make a Real Difference<br>in Chicago Communities</div>
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
        <div class="gift-card">
            <div class="gift-icon">📱</div>
            <div>
                <div class="gift-amount">$65 gives a lifeline</div>
                <div class="gift-desc">Provides a newly arrived migrant family with a phone, unlimited data, and hotspot access for one month.</div>
            </div>
        </div>
        <div class="gift-card">
            <div class="gift-icon">🚍</div>
            <div>
                <div class="gift-amount">$25 opens a door</div>
                <div class="gift-desc">Covers public transit for students and parents to get to school, legal appointments, or medical care.</div>
            </div>
        </div>
        <div class="gift-card">
            <div class="gift-icon">📚</div>
            <div>
                <div class="gift-amount">$100 empowers a student</div>
                <div class="gift-desc">Supports a young person in our ELEVATE Program with mentorship, tutoring, and college guidance.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="gift-card">
            <div class="gift-icon">💼</div>
            <div>
                <div class="gift-amount">$150 prepares a future</div>
                <div class="gift-desc">Funds career readiness training through our IMPACT Program including resume support and job coaching.</div>
            </div>
        </div>
        <div class="gift-card">
            <div class="gift-icon">🧠</div>
            <div>
                <div class="gift-amount">$200 brings healing</div>
                <div class="gift-desc">Supports trauma-informed mental health sessions for families who have endured displacement or poverty.</div>
            </div>
        </div>
        <div class="gift-card">
            <div class="gift-icon">⚖️</div>
            <div>
                <div class="gift-amount">$500 provides hope</div>
                <div class="gift-desc">Helps grow our volunteer legal clinic where families receive guidance on asylum cases and work permits.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💚 Donate to ChiEAC Community Impact Fund", use_container_width=True, type="primary"):
        st.markdown('<meta http-equiv="refresh" content="0;url=https://www.zeffy.com/en-US/fundraising/chieac-social-impact-project">', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Volunteer
    st.markdown("""
    <div class="volunteer-section">
        <div class="section-badge">Get Involved</div>
        <div class="section-title" style="text-align:center;">Volunteer With Us</div>
        <div class="section-text" style="text-align:center; max-width:600px; margin: 0 auto 24px auto;">
            We rely on volunteers to help us provide these vital services.
            Whether you have time to mentor or assist at events, your involvement
            helps us empower students to achieve their goals.
            Join us in fostering educational equity today.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🤝 Volunteer With ChiEAC", use_container_width=False):
        st.markdown('<meta http-equiv="refresh" content="0;url=https://www.volunteermatch.org/search/org1194340.jsp">', unsafe_allow_html=True)

    # Mission dark section
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

    # Footer
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
        st.markdown("""
        <div style="padding: 16px 0;">
            <span style="font-size:1.5em; font-weight:900; color:#1a1a1a;">Chi<span style="color:#2d6a4f;">EAC</span></span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Log In", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        with c2:
            if st.button("← Home", use_container_width=True):
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

        st.markdown("""
        <div style='text-align:center; margin-top:16px; color:#888; font-size:0.88em;'>
            Already have an account?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Log In Instead", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
elif st.session_state.page == "login":

    col1, col2, col3 = st.columns([3, 4, 3])
    with col1:
        st.markdown("""
        <div style="padding: 16px 0;">
            <span style="font-size:1.5em; font-weight:900; color:#1a1a1a;">Chi<span style="color:#2d6a4f;">EAC</span></span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Home", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()
        with c2:
            if st.button("Sign Up", use_container_width=True, type="primary"):
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

        st.markdown("""
        <div style='text-align:center; margin-top:16px; color:#888; font-size:0.88em;'>
            Don't have an account yet?
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create an Account", use_container_width=True):
            st.session_state.page = "signup"
            st.rerun()

        st.markdown("""
        <div style='text-align:center; margin-top:12px; color:#999; font-size:0.82em;'>
            Need help? Contact us at
            <a href="mailto:benjamin@chieac.org" style="color:#2d6a4f;">benjamin@chieac.org</a>
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    st.markdown(f"""
    <div class="dashboard-header">
        <div class="dashboard-title">Welcome, {st.session_state.name} 👋</div>
        <div class="dashboard-sub">ChiEAC Student Support Portal — We are here to help</div>
    </div>
    """, unsafe_allow_html=True)

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
                        st.success("✅ Your request has been submitted! A ChiEAC team member will reach out soon.")
                        st.balloons()
                    else:
                        st.error("Something went wrong. Please try again or call 773-599-0267")
                else:
                    st.error("Please fill in all required fields!")

    elif st.session_state.student_tab == "history":
        st.markdown("### 📋 My Past Requests")
        try:
            df = pd.read_csv(REQUESTS_URL)
            df.columns = ["Timestamp", "Username", "Name", "Email", "Phone",
                         "Neighborhood", "Support Type", "Urgency", "Description", "Status"]
            my_requests = df[df["Username"] == st.session_state.user]
            if len(my_requests) > 0:
                st.dataframe(my_requests[["Timestamp", "Support Type", "Urgency", "Status", "Description"]],
                           use_container_width=True)
            else:
                st.info("You have not submitted any requests yet.")
        except:
            st.info("Request history coming soon! Contact benjamin@chieac.org for updates.")

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
                st.metric("🟡 Medium", len(df[df["Urgency"] == "Medium - Need help this month"]))

            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                urgency_filter = st.selectbox("Filter by Urgency",
                    ["All", "Critical - Need help today", "High - Need help this week",
                     "Medium - Need help this month", "Low - Planning ahead"])
            with col2:
                type_filter = st.selectbox("Filter by Type",
                    ["All", "Food", "Rent", "Transportation", "Technology",
                     "School Supplies", "Mental Health", "Housing", "Legal Help",
                     "Career Readiness", "EMERGENCY", "Other"])

            filtered = df.copy()
            if urgency_filter != "All":
                filtered = filtered[filtered["Urgency"] == urgency_filter]
            if type_filter != "All":
                filtered = filtered[filtered["Support Type"] == type_filter]

            st.markdown(f"**Showing {len(filtered)} of {len(df)} requests**")
            st.dataframe(filtered, use_container_width=True, height=420)

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