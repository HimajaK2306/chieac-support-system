import streamlit as st
import requests
import json
from datetime import datetime

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzYcAzLSO8IKh-fjarAj4RTJIt9ks_t1nQlm-RCBImdNsEUSCLEzbHoHf4TZJfSvtyuQQ/exec"

st.set_page_config(
    page_title="ChiEAC Student Support System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 ChiEAC Student Support Request System")
st.subheader("Chicago Education Advocacy Cooperative")
st.write("Welcome! Please fill out the form below to submit a support request.")

st.divider()

with st.form("support_request_form"):
    st.subheader("📋 Student Information")
    
    name = st.text_input("Full Name *")
    email = st.text_input("Email Address *")
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
    
    description = st.text_area("Please describe your situation *", height=150)
    
    submitted = st.form_submit_button("Submit Request")
    
    if submitted:
        if name and email and support_type != "Select..." and urgency != "Select..." and description:
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "neighborhood": neighborhood,
                "support_type": support_type,
                "urgency": urgency,
                "description": description
            }
            try:
                response = requests.post(GOOGLE_SCRIPT_URL, json=data)
                st.success("✅ Thank you! Your request has been submitted successfully. We will contact you soon.")
            except Exception as e:
                st.error("❌ Something went wrong. Please try again.")
        else:
            st.error("❌ Please fill in all required fields marked with *")