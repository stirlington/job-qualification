import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document
import requests

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

# Helper function: Upload file to SharePoint
def upload_to_sharepoint(file_path, file_name):
    sharepoint_site = "https://davidsongray.sharepoint.com"
    site_relative_url = "/sites/StirlingQR"
    folder_relative_url = "/sites/StirlingQR/Shared Documents/General"

    # SharePoint credentials (use environment variables for security)
    username = "your-sharepoint-chris@stirlingqr.com"  # Replace with your SharePoint email
    password = "your-sharepoint-Measure897!"          # Replace with your SharePoint password

    # Authenticate using requests library
    auth_url = f"{sharepoint_site}/_forms/default.aspx?wa=wsignin1.0"
    session = requests.Session()
    session.auth = (username, password)

    # Upload file to SharePoint
    with open(file_path, "rb") as file_content:
        upload_url = f"{sharepoint_site}/_api/web/getfolderbyserverrelativeurl('{folder_relative_url}')/files/add(overwrite=true, url='{file_name}')"
        headers = {"Accept": "application/json;odata=verbose"}
        response = session.post(upload_url, headers=headers, data=file_content)

        if response.status_code == 200:
            return f"{sharepoint_site}{folder_relative_url}/{file_name}"  # Return the URL of the uploaded file
        else:
            raise Exception(f"Failed to upload file: {response.text}")

# Form creation and submission handling
with st.form("job_vacancy_form"):
    # Contact Information
    st.subheader("Contact Information")
    company_name = st.text_input("Company Name*")
    job_title = st.text_input("Job Title*")
    
    # Additional fields (truncated for brevity)
    location = st.text_input("Location*")
    required_skills = st.text_area("Required Skills*")

    # Submit button
    submitted = st.form_submit_button("Submit Job Vacancy")

if submitted:
    required_fields = [
        (company_name, "Company Name"),
        (job_title, "Job Title"),
        (location, "Location"),
        (required_skills, "Required Skills"),
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
            "Location": location,
            "Required Skills": required_skills,
        }

        # Create Word document locally
        doc_filename = create_word_document(form_data)

        try:
            # Upload document to SharePoint
            uploaded_file_url = upload_to_sharepoint(doc_filename, os.path.basename(doc_filename))
            st.success(f"File uploaded successfully to SharePoint: {uploaded_file_url}")

            # Notify admin about the new upload (optional)
            st.info(f"A new job vacancy has been submitted: {uploaded_file_url}")

            # Clean up local file after upload (optional)
            os.remove(doc_filename)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
