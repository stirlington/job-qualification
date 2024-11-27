import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(page_title="Recruitment Form", layout="wide")

# Title
st.title("Job Vacancy Requirements Form")
st.markdown("Please fill out the details for your job vacancy below.")

# Form
with st.form("job_vacancy_form"):
    # Basic Job Information
    st.subheader("Basic Job Information")
    job_title = st.text_input("Job Title*")
    department = st.text_input("Department")
    location = st.text_input("Location*")
    
    # Working Arrangements
    st.subheader("Working Arrangements")
    work_model = st.selectbox(
        "Working Model*",
        ["Office-based", "Hybrid", "Remote", "Flexible"]
    )
    if work_model == "Hybrid":
        office_days = st.number_input("Required Office Days per Week", min_value=1, max_value=5)
    
    # Compensation
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

# Handle form submission
if submitted:
    # Validation
    required_fields = [
        (job_title, "Job Title"),
        (location, "Location"),
        (required_skills, "Required Skills"),
        (success_factor_1, "1st Important Factor"),
        (success_factor_2, "2nd Important Factor"),
        (success_factor_3, "3rd Important Factor")
    ]
    
    missing_fields = [field[1] for field in required_fields if not field[0]]
    
    if missing_fields:
        st.error(f"Please fill out the following required fields: {', '.join(missing_fields)}")
    else:
        # Create data dictionary
        form_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            "Urgent": "Yes" if urgent else "No",
            "Additional Notes": additional_notes
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([form_data])
        
        # Save to Excel
        file_path = "job_vacancies.xlsx"
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_excel(file_path, index=False)
        else:
            df.to_excel(file_path, index=False)
        
        st.success("Form submitted successfully! The data has been saved.")

# Add some CSS styling
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            background-color: #0066cc;
            color: white;
        }
        .stButton>button:hover {
            background-color: #0052a3;
        }
    </style>
    """, unsafe_allow_html=True)
