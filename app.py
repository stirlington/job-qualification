import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document
import re

# Page configuration
st.set_page_config(page_title="Job Vacancy Form", layout="wide")

# Display logo
try:
    st.image("logo.png", width=200)
except FileNotFoundError:
    st.error("Logo not found. Please ensure 'logo.png' is in the same directory.")

# Title
st.title("Job Vacancy Requirements Form")
st.markdown("Please fill out this form with job vacancy details.")

# Helper functions
def is_valid_email(email):
    """Validate email address format."""
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
    filename = f"job_vacancy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    doc.save(filename)
    return filename

def save_submission(data, filename):
    """Save form data and Word document locally."""
    # Create a submissions folder if it doesn't exist
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        os.makedirs(submissions_folder)

    # Save Word document in the submissions folder
    new_file_path = os.path.join(submissions_folder, filename)
    os.rename(filename, new_file_path)

    # Save form data to a CSV file for record-keeping
    csv_file = os.path.join(submissions_folder, "submissions.csv")
    df = pd.DataFrame([data])
    
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, index=False)

# Form creation
with st.form("job_vacancy_form"):
    sender_email = st.text_input("Your Email Address*")
    job_title = st.text_input("Job Title*")
    location = st.text_input("Location*")
    required_skills = st.text_area("Required Skills*")
    success_factor_1 = st.text_input("1st Important Factor*")
    success_factor_2 = st.text_input("2nd Important Factor*")
    success_factor_3 = st.text_input("3rd Important Factor*")
    
    submitted = st.form_submit_button("Submit Job Vacancy")

# Handle form submission
if submitted:
    if not all([sender_email, job_title, location, required_skills, success_factor_1, success_factor_2, success_factor_3]):
        st.error("All required fields must be filled.")
    elif not is_valid_email(sender_email):
        st.error("Invalid email address.")
    else:
        # Collect form data
        form_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Sender Email": sender_email,
            "Job Title": job_title,
            "Location": location,
            "Required Skills": required_skills,
            "Top Factor 1": success_factor_1,
            "Top Factor 2": success_factor_2,
            "Top Factor 3": success_factor_3,
        }

        # Create Word document and save submission locally
        doc_filename = create_word_document(form_data)
        save_submission(form_data, doc_filename)

        # Notify admin (you) that a new submission has been made
        st.success(f"Form submitted successfully! A new job vacancy has been recorded.")

        # Provide download button for Word document to the client
        with open(f"submissions/{doc_filename}", 'rb') as file:
            st.download_button(
                label="Download Job Vacancy Details",
                data=file,
                file_name=doc_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# Admin Dashboard (for you to view submissions)
st.sidebar.header("Admin Dashboard")
if st.sidebar.button("View Submissions"):
    submissions_folder = "submissions"
    
    # Check if there are any submissions saved
    if not os.path.exists(submissions_folder):
        st.sidebar.error("No submissions found.")
    else:
        csv_file = os.path.join(submissions_folder, "submissions.csv")
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            st.sidebar.write("### Submitted Forms:")
            st.sidebar.dataframe(df)
            
            # Provide links to download individual Word documents
            for _, row in df.iterrows():
                word_doc_name = f"job_vacancy_{row['Submission Date'].replace(':', '').replace('-', '').replace(' ', '_')}.docx"
                word_doc_path = os.path.join(submissions_folder, word_doc_name)
                
                if os.path.exists(word_doc_path):
                    with open(word_doc_path, 'rb') as file:
                        st.sidebar.download_button(
                            label=f"Download {row['Job Title']} Details",
                            data=file,
                            file_name=word_doc_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
        else:
            st.sidebar.error("No CSV records found.")
