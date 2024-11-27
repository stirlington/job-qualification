import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Page configuration
st.set_page_config(page_title="Job Vacancy Requirements Form", layout="wide")

# Display logo
try:
    st.image("logo.png", width=200)
except FileNotFoundError:
    st.error("Logo not found. Please ensure 'logo.png' is in the same directory.")

# Title
st.title("Job Vacancy Requirements Form")
st.markdown("Please fill out this form with job vacancy details.")

# Helper function: Create Word document
def create_word_document(data):
    doc = Document()
    doc.add_heading('Job Vacancy Details', level=0)
    for key, value in data.items():
        p = doc.add_paragraph()
        p.add_run(f"{key}: ").bold = True
        p.add_run(str(value))
    filename = f"{data['Company Name']}_{data['Job Title']}.docx".replace(" ", "_")
    doc.save(filename)
    return filename

# Helper function: Send email via Outlook SMTP
def send_email_via_outlook(filename, data):
    sender_email = "chris.stirling@stirlingqr.com"  # Your Outlook email address
    sender_password = "Measure897!"  # Your Outlook password (ensure this is secure!)
    receiver_email = "chris.stirling@stirlingqr.com"  # Email where you want to receive the submission

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Job Vacancy Submission: {data['Job Title']}"

    # Email body content
    body = "A new job vacancy has been submitted with the following details:\n\n"
    for key, value in data.items():
        body += f"{key}: {value}\n"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the Word document
    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='docx')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

    # Send the email using Outlook's SMTP server
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)  # Outlook SMTP server and port
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in to your account
        server.send_message(msg)  # Send the email
        server.quit()  # Close the connection
        return True  # Return success status if no errors occur

    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Form creation and submission handling
with st.form("job_vacancy_form"):
    # Contact Information
    st.subheader("Contact Information")
    company_name = st.text_input("Company Name*")
    job_title = st.text_input("Job Title*")
    
    # Basic Job Information
    st.subheader("Basic Job Information")
    department = st.text_input("Department")
    location = st.text_input("Location*")

    # Working Arrangements Section (truncated for brevity)
    
    # Submit button
    submitted = st.form_submit_button("Submit Job Vacancy")

if submitted:
    
    required_fields = [
        (company_name, "Company Name"),
        (job_title, "Job Title"),
        (location, "Location"),
     ]
    
    missing_fields = [field[1] for field in required_fields if not field[0]]
    
    if missing_fields:
        st.error(f"Please fill out the following required fields: {', '.join(missing_fields)}")
        
    else:
        # Collect form data
        form_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company Name": company_name,
            "Job Title": job_title,
            "Department": department,
            "Location": location,
            # Additional fields truncated for brevity...
        }

        # Create Word document locally
        doc_filename = create_word_document(form_data)

        try:
            # Send email via Outlook SMTP with the Word document attached
            if send_email_via_outlook(doc_filename, form_data):
                st.success(f"Form submitted successfully! An email has been sent to {receiver_email}")

            # Clean up local file after sending (optional)
            os.remove(doc_filename)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
