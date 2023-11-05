import yagmail
import streamlit as st
import re
import json, tempfile
import mantis_vision.base_functions as bf


# read credentials from secrets:

config = {
    "email_address": st.secrets["gmail"]["email_address"],
    "google_client_id": st.secrets["gmail"]["google_client_id"],
    "google_client_secret": st.secrets["gmail"]["google_client_secret"],
    "google_refresh_token": st.secrets["gmail"]["google_refresh_token"],
}
creds = tempfile.NamedTemporaryFile(mode="w+")
json.dump(config, creds)
creds.flush()


def send_email(email: str, contents: str, attachment: str):
    if re.fullmatch(bf.regex, email) is None:
        st.write("Email not sent or invalid email address")
    else:
        try:
            yag = yagmail.SMTP(
                "mantis.from.image@gmail.com",
                # oauth2_file=".streamlit/credentials.json",
                oauth2_file=creds.name,
            )
            print(creds.name)
            yag.send(to=email, subject="test")
        except Exception as e:
            st.write(e)
    st.toast("Thank you for your feedback!")
