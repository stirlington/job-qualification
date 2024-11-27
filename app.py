def send_email(filename, data, sender_email):
    receiver_email = "info@stirlingqr.com"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Job Vacancy: {data['Job Title']}"

    body = "A new job vacancy has been submitted with the following details:\n\n"
    for key, value in data.items():
        if key != "Sender Email":
            body += f"{key}: {value}\n"
    msg.attach(MIMEText(body, 'plain'))

    with open(filename, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='docx')
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, st.session_state.email_password)
        server.send_message(msg)
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("Authentication failed. Please check your email or app-specific password.")
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
    return False
