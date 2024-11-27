import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
from docx import Document

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
    # Sanitize file name by replacing invalid characters with underscores
    safe_company_name = re.sub(r'[^\w\s-]', '_', data['Company Name'])
    safe_job_title = re.sub(r'[^\w\s-]', '_', data['Job Title'])
    filename = f"{safe_company_name}_{safe_job_title}.docx".replace(" ", "_")
    
    # Create Word document
    doc = Document()
    doc.add_heading('Job Vacancy Details', level=0)
    for key, value in data.items():
        p = doc.add_paragraph()
        p.add_run(f"{key}: ").bold = True
        p.add_run(str(value))
    
    # Save the document
    doc.save(filename)
    return filename

# Helper function: Save submission locally
def save_submission(data, filename):
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        os.makedirs(submissions_folder)

    # Ensure the file exists before renaming
    if os.path.exists(filename):
        new_file_path = os.path.join(submissions_folder, filename)
        os.rename(filename, new_file_path)
    else:
        raise FileNotFoundError(f"The file {filename} does not exist and cannot be moved.")

    # Save form data to a CSV file for record-keeping
    csv_file = os.path.join(submissions_folder, "submissions.csv")
    df = pd.DataFrame([data])
    
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, index=False)

# Form creation and submission handling
with st.form("job_vacancy_form"):
    st.subheader("Contact Information")
    company_name = st.text_input("Company Name*")
    job_title = st.text_input("Job Title*")
    
    st.subheader("Basic Job Information")
    location = st.text_input("Location*")
    
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
        form_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company Name": company_name,
            "Job Title": job_title,
            "Location": location,
        }

        # Create Word document locally
        try:
            doc_filename = create_word_document(form_data)
            save_submission(form_data, doc_filename)

            with open(os.path.join("submissions", doc_filename), 'rb') as file:
                st.download_button(
                    label="Download Job Vacancy Details",
                    data=file,
                    file_name=doc_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            st.success(f"Form submitted successfully! Your document has been saved.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
