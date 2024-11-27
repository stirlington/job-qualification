import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re

# Page configuration
st.set_page_config(page_title="Recruitment Form", layout="wide")

# Display logo
try:
    logo_path = "logo.png"
    st.image(logo_path, width=200)
except Exception as e:
    st.error("Logo not found. Please ensure 'logo.png' is in the same directory as the script.")

# Title
st.title("Job Vacancy Requirements Form")
st.markdown("Please fill out the details for your job vacancy below.")

def is_valid_email(email):
    """Check if email address is valid"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def create_word_document(data):
    """Generate a Word document with job vacancy details."""
    doc = Document()
    doc.add_heading('Job Vacancy Details', level=0)
    for key, value in data.items():
        if key not in ["Submission Date", "Sender Email"]:
            p = doc.add_paragraph()
            p.add_run(f"{key}: ").bold = True
            p.add_run(str(value))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_vacancy_{timestamp}.docx"
    doc.save(filename)
    return filename

def send_email(filename, data, sender_email):
    """Send an email with job vacancy details attached."""
    receiver_email = "info@stirlingqr.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Job Vacancy: {data['Job Title']}"

    # Email body
    body = "A new job vacancy has been submitted with the following details:\n\n"
    for key, value in data.items():
        if key != "Sender Email":
            body += f"{key}: {value}\n"
    msg.attach(MIMEText(body, 'plain'))

    # Attach Word document
    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='docx')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

    # Send email via SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, st.session_state.email_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Form creation and submission handling
with st.form("job_vacancy_form"):
    # Contact Information
    st.subheader("Contact Information")
    sender_email = st.text_input("Your Email Address*")

    # Basic Job Information
    st.subheader("Basic Job Information")
    job_title = st.text_input("Job Title*")
    department = st.text_input("Department")
    location = st.text_input("Location*")

    # Working Arrangements
    st.subheader("Working Arrangements")
    work_model = st.selectbox(
        "Working Model*", ["Office-based", "Hybrid", "Remote", "Flexible"]
    )
    
    if work_model == "Hybrid":
        office_days = st.number_input("Required Office Days per Week", min_value=1, max_value=5)

    # Compensation Package
    st.subheader("Compensation Package")
    
    col1, col2 = st.columns(2)
    
    with col1:
        salary_min = st.number_input("Minimum Salary (£)*", min_value=0)
    
    with col2:
        salary_max = st.number_input("Maximum Salary (£)*", min_value=0)
    
    benefits = st.multiselect(
        "Benefits Package",
        ["Health Insurance", "Dental Insurance", "Life Insurance", "Pension",
         "Annual Bonus", "Share Options", "Professional Development Budget",
         "Gym Membership", "Private Healthcare", "Mental Health Support"]
    )
    
    bonus_scheme = st.text_area("Bonus Structure Details (if applicable)")

# Qualifications and Requirements Section (truncated for brevity)

# Key Success Factors Section (truncated for brevity)

# Additional Information Section (truncated for brevity)

# Submit button handling logic (truncated for brevity)
