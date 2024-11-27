if submitted:
    # Check for missing fields
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
        # Collect form data
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

        # Save submission locally
        doc_filename = create_word_document(form_data)
        save_submission(form_data, doc_filename)

        # Track new submission in session state
        if 'new_submissions' not in st.session_state:
            st.session_state['new_submissions'] = []
        
        st.session_state['new_submissions'].append(form_data)

        st.success("Form submitted successfully!")
        st.sidebar.header("New Submissions")

if 'new_submissions' in st.session_state and st.session_state['new_submissions']:
    st.sidebar.write(f"🔔 You have {len(st.session_state['new_submissions'])} new submission(s).")
    
    if st.sidebar.button("View Submissions"):
        st.write("### New Submissions")
        
        for idx, submission in enumerate(st.session_state['new_submissions']):
            st.write(f"#### Submission {idx + 1}")
            for key, value in submission.items():
                st.write(f"**{key}:** {value}")
        
        # Clear notifications after viewing
        if st.button("Mark as Read"):
            st.session_state['new_submissions'] = []
else:
    st.sidebar.write("No new submissions.")
