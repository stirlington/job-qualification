import streamlit as st
import pandas as pd
from datetime import datetime
import os
from docx import Document

# Page configuration
st.set_page_config(page_title="Job Vacancy Form", layout="wide")

# Helper functions
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
    submissions_folder = "submissions"
    if not os.path.exists(submissions_folder):
        os.makedirs(submissions_folder)

    new_file_path = os.path.join(submissions_folder, filename)
    os.rename(filename, new_file_path)

    csv_file = os.path.join(submissions_folder, "submissions.csv")
    df = pd.DataFrame([data])
    
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, index=False)

def validate_login(email, password):
    """Validate admin login credentials."""
    return email == "info@stirlingqr.com" and password == "JobQualifications"

# Get query parameters to determine which page to display
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["client"])[0]  # Default to "client" page

# ------------------- Client Page -------------------
if page == "client":
    st.title("Job Vacancy Requirements Form")
    st.markdown("Please fill out this form with job vacancy details.")

    with st.form("job_vacancy_form"):
        sender_email = st.text_input("Your Email Address*")
        job_title = st.text_input("Job Title*")
        location = st.text_input("Location*")
        required_skills = st.text_area("Required Skills*")
        success_factor_1 = st.text_input("1st Important Factor*")
        success_factor_2 = st.text_input("2nd Important Factor*")
        success_factor_3 = st.text_input("3rd Important Factor*")
        
        submitted = st.form_submit_button("Submit Job Vacancy")

    if submitted:
        if not all([sender_email, job_title, location, required_skills, success_factor_1, success_factor_2, success_factor_3]):
            st.error("All required fields must be filled.")
        else:
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

            doc_filename = create_word_document(form_data)
            save_submission(form_data, doc_filename)

            st.success("Form submitted successfully! A new job vacancy has been recorded.")

            with open(f"submissions/{doc_filename}", 'rb') as file:
                st.download_button(
                    label="Download Job Vacancy Details",
                    data=file,
                    file_name=doc_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# ------------------- Admin Page -------------------
elif page == "admin":
    st.title("Admin Dashboard")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.form("login_form"):
            admin_email = st.text_input("Admin Email")
            admin_password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        if login_button:
            if validate_login(admin_email, admin_password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.experimental_set_query_params(page="admin")  # Reload as admin page
                st.experimental_rerun()
            else:
                st.error("Invalid email or password.")
    else:
        submissions_folder = "submissions"
        
        if not os.path.exists(submissions_folder):
            st.error("No submissions found.")
        else:
            csv_file = os.path.join(submissions_folder, "submissions.csv")
            
            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
                st.write("### Submitted Forms:")
                st.dataframe(df)

                for _, row in df.iterrows():
                    word_doc_name = f"job_vacancy_{row['Submission Date'].replace(':', '').replace('-', '').replace(' ', '_')}.docx"
                    word_doc_path = os.path.join(submissions_folder, word_doc_name)
                    
                    if os.path.exists(word_doc_path):
                        with open(word_doc_path, 'rb') as file:
                            st.download_button(
                                label=f"Download {row['Job Title']} Details",
                                data=file,
                                file_name=word_doc_name,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
            else:
                st.error("No CSV records found.")

        if st.button("Logout"):
            del st.session_state.logged_in
            st.experimental_set_query_params(page="client")  # Redirect to client page
            st.experimental_rerun()
