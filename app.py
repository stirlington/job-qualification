import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document
from github import Github
import base64

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

# Helper function: Save submission locally
def save_submission(data, filename):
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

# Helper function: Upload file to GitHub
def upload_to_github(file_path, repo_name, branch_name, github_token):
    """
    Uploads a file to a GitHub repository.

    Args:
        file_path (str): The local path of the file to upload.
        repo_name (str): The name of the repository (e.g., "username/repo").
        branch_name (str): The branch where the file will be uploaded.
        github_token (str): Your GitHub personal access token.

    Returns:
        str: URL of the uploaded file on GitHub.
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    # Read the file content
    with open(file_path, "rb") as file:
        content = file.read()
    
    content_base64 = base64.b64encode(content).decode("utf-8")
    github_file_path = f"submissions/{file_path.split('/')[-1]}"

    try:
        existing_file = repo.get_contents(github_file_path, ref=branch_name)
        repo.update_file(
            path=github_file_path,
            message=f"Update {file_path.split('/')[-1]}",
            content=content_base64,
            sha=existing_file.sha,
            branch=branch_name,
        )
    except:
        repo.create_file(
            path=github_file_path,
            message=f"Add {file_path.split('/')[-1]}",
            content=content_base64,
            branch=branch_name,
        )
    
    return f"https://github.com/{repo_name}/blob/{branch_name}/{github_file_path}"

# Initialize session state for form submission tracking
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

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

    # Qualifications and Requirements
    st.subheader("Qualifications and Requirements")
    
    experience_years = st.slider("Years of Experience Required", 0, 20, 3)
    
    education_level = st.selectbox(
        "Minimum Education Level",
        ["None Required", "High School", "Bachelor's Degree", "Master's Degree", "PhD"]
    )
    
    required_skills = st.text_area("Required Skills and Qualifications*")
    
    preferred_skills = st.text_area("Preferred Skills (Nice to Have)")

    # Interview Process
    st.subheader("Interview Process")
    
    interview_stages = st.multiselect(
        "Interview Stages*",
        ["Phone Screening", "HR Interview", "Technical Interview",
         "Task/Assignment", "Panel Interview", "Final Interview",
         "Presentation", "Assessment Center"]
    )
    
   interview_details...
