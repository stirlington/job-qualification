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
    
    interview_details = st.text_area("Additional Interview Process Details")

    # Key Success Factors
    st.subheader("Top 3 Most Important Factors")
    
    success_factor_1 = st.text_input("1st Most Important Factor*")
    
    success_factor_2 = st.text_input("2nd Most Important Factor*")
    
    success_factor_3 = st.text_input("3rd Most Important Factor*")

    # Additional Information
    st.subheader("Additional Information")
    
    start_date = st.date_input("Expected Start Date")
    
    urgent = st.checkbox("This is an urgent requirement")
    
    additional_notes = st.text_area("Any Additional Information or Special Requirements")

    # Submit button
    submitted = st.form_submit_button("Submit Job Vacancy")

if submitted:
    
    required_fields = [
        (company_name, "Company Name"),
        (job_title, "Job Title"),
        (location, "Location"),
        (required_skills, "Required Skills"),
        (success_factor_1, "1st Important Factor"),
        (success_factor_2, "2nd Important Factor"),
        (success_factor_3, "3rd Important Factor"),
     ]
    
    missing_fields = [field[1] for field in required_fields if not field[0]]
    
    if missing_fields:
        st.error(f"Please fill out the following required fields: {', '.join(missing_fields)}")
        
    else:
        form_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company Name": company_name,
            "Job Title": job_title,
            "Department": department,
            "Location": location,
            "Working Model": work_model,
            "Salary Range": f"£{salary_min:,} - £{salary_max:,}",
            "Benefits": ", ".join(benefits),
            "Bonus Structure": bonus_scheme,
            "Required Experience": f"{experience_years} years",
            "Education Level": education_level,
            "Required Skills": required_skills,
            "Preferred Skills": preferred_skills,
            "Interview Stages": ", ".join(interview_stages),
            "Interview Details": interview_details,
            "Top Factor 1": success_factor_1,
            "Top Factor 2": success_factor_2,
            "Top Factor 3": success_factor_3,
            "Start Date": start_date.strftime("%Y-%m-%d"),
            "Urgent": urgent,
            "Additional Notes": additional_notes,
        }

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
