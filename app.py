import streamlit as st
import requests
import yaml
import pandas as pd
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Load config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzYcAzLSO8IKh-fjarAj4RTJIt9ks_t1nQlm-RCBImdNsEUSCLEzbHoHf4TZJfSvtyuQQ/exec"
SHEET_ID = "1h85m2f6UmE9NPOcHrQnU2_n7GWyL1ZTLhyvbJuUrl94"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(
    page_title="ChiEAC Student Support System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 ChiEAC Student Support System")
st.subheader("Chicago Education Advocacy Cooperative")
st.divider()

# Login
try:
    authenticator.login()
    name = st.session_state.get("name")
    authentication_status = st.session_state.get("authentication_status")
    username = st.session_state.get("username")
except Exception as e:
    st.error(f"Login error: {e}")
    name = None
    authentication_status = None
    username = None

if authentication_status == False:
    st.error("Username or password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")

elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Welcome {name}!")

    # Check if staff or student
    role = config['credentials']['usernames'][username].get('role', 'student')

    if role == 'staff':
        st.sidebar.title("Staff Menu")
        page = st.sidebar.selectbox("Navigate", ["View All Requests", "Student Request Form"])
    else:
        page = "Student Request Form"

    if page == "Student Request Form":
        st.title("Submit a Support Request")
        st.write("Please fill out the form below.")
        st.divider()

        with st.form("support_request_form"):
            st.subheader("📋 Student Information")
            name_input = st.text_input("Full Name *")
            email_input = st.text_input("Email Address *")
            phone = st.text_input("Phone Number")
            neighborhood = st.text_input("Neighborhood / ZIP Code *")

            st.subheader("🆘 Support Request Details")
            support_type = st.selectbox(
                "Type of Support Needed *",
                ["Select...", "Food", "Rent", "Transportation",
                 "Technology", "School Supplies", "Mental Health",
                 "Housing", "Other"]
            )
            urgency = st.selectbox(
                "Urgency Level *",
                ["Select...", "Critical - Need help today",
                 "High - Need help this week",
                 "Medium - Need help this month",
                 "Low - Planning ahead"]
            )
            description = st.text_area(
                "Please describe your situation *",
                height=150
            )
            submitted = st.form_submit_button("Submit Request")

            if submitted:
                if name_input and email_input and support_type != "Select..." and urgency != "Select..." and description:
                    data = {
                        "name": name_input,
                        "email": email_input,
                        "phone": phone,
                        "neighborhood": neighborhood,
                        "support_type": support_type,
                        "urgency": urgency,
                        "description": description
                    }
                    try:
                        response = requests.post(GOOGLE_SCRIPT_URL, json=data)
                        st.success("✅ Thank you! Your request has been submitted successfully!")
                    except Exception as e:
                        st.error("❌ Something went wrong. Please try again.")
                else:
                    st.error("❌ Please fill in all required fields marked with *")

    elif page == "View All Requests":
        st.title("📊 Staff Dashboard")
        st.subheader("All Student Support Requests")
        st.divider()

        try:
            df = pd.read_csv(SHEET_URL)
            df.columns = ["Timestamp", "Name", "Email", "Phone", "Neighborhood", "Support Type", "Urgency", "Description"]

            st.metric("Total Requests", len(df))

            col1, col2, col3 = st.columns(3)
            with col1:
                critical = len(df[df["Urgency"] == "Critical - Need help today"])
                st.metric("🔴 Critical", critical)
            with col2:
                high = len(df[df["Urgency"] == "High - Need help this week"])
                st.metric("🟠 High", high)
            with col3:
                medium = len(df[df["Urgency"] == "Medium - Need help this month"])
                st.metric("🟡 Medium", medium)

            st.divider()

            urgency_filter = st.selectbox(
                "Filter by Urgency",
                ["All", "Critical - Need help today",
                 "High - Need help this week",
                 "Medium - Need help this month",
                 "Low - Planning ahead"]
            )

            support_filter = st.selectbox(
                "Filter by Support Type",
                ["All", "Food", "Rent", "Transportation",
                 "Technology", "School Supplies", "Mental Health",
                 "Housing", "Other"]
            )

            filtered_df = df.copy()
            if urgency_filter != "All":
                filtered_df = filtered_df[filtered_df["Urgency"] == urgency_filter]
            if support_filter != "All":
                filtered_df = filtered_df[filtered_df["Support Type"] == support_filter]

            st.dataframe(filtered_df, use_container_width=True)

        except Exception as e:
            st.error(f"Error loading data: {e}")