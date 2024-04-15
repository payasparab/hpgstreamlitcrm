import streamlit as st
import pandas as pd
import base64
import os
from page_2 import run_page2
from page_3 import run_page3
from page_4 import run_page4
from page_5 import run_page5
import hmac
import re
from datetime import datetime
import base64
from io import BytesIO
import re
import streamlit as st
from credentials import sg_api_key
from email_validator import validate_email, EmailNotValidError
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# Main Streamlit app starts here

st.set_page_config(
        page_title="HPG CRM Demo",
        page_icon="hpg_logo.png",
        layout="wide",
    )


def check_email():
    """Asks the user for their name and email, and returns True if a valid email is entered."""

    # Function to call when the submit button is pressed
    def email_submitted():
        """Validates the email and sends a confirmation if valid."""
        try:
            # Validate email
            valid = validate_email(st.session_state["email_address"])
            email = valid.email  # Normalized form of email
            st.session_state["email_valid"] = True
            st.success("Email is valid. Access granted.")
            
            # Send lead email
            send_lead_email(name=st.session_state["name_submitted"], email=email)

        except EmailNotValidError as e:
            # Email is not valid
            st.session_state["email_valid"] = False
            st.error(f"Invalid email address: {e}")

    # Check if the email is already validated
    if st.session_state.get("email_valid"):
        return True

    # Input for name
    st.text_input("Name", key="name_submitted")

    # Input for email with a submit button
    st.text_input("Email Address", key="email_address")
    submit_button = st.button("Submit", on_click=email_submitted)

    # Error message if email is not valid
    if st.session_state.get("email_valid") == False:
        st.error("Please enter a valid email address.")

    # Only proceed if the email is valid
    return st.session_state.get("email_valid", False)




def send_lead_email(name, email):
    """Sends an email with the lead information using SendGrid."""
    sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
    from_email = Email("payas@handypointgroup.com")  # The email address it is sent from (update with your email).
    to_email = To("payas@handypointgroup.com")  # The destination email address.
    submit_time = datetime.now()
    subject = "New Lead from Streamlit App CRM Demo"
    content = Content("text/plain", f"Name: {name}\nEmail: {email}\nTime:{submit_time}")
    mail = Mail(from_email, to_email, subject, content)

    # Send the email.
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        st.error("Failed to send email.")
    else:
        st.success("Lead sent successfully!")


# Rest of the streamlit code
if check_email():
        # Navigation for App

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ['Summary Tables', 'Map', 'Cumulative Report', 'Contact Sheets', 'Connections Tracker'])

    og_data = pd.read_csv('call_log.csv')
    og_data['interview'] = og_data['call_disposition'].apply(
        lambda x: x == 'Connected - Interested'
    )

    # Title of the app
    st.title('Interactive Database for Business Development Managers')

    def run_app():
        # Function to download data as CSV
        # Convert DataFrame to CSV
        csv = og_data.to_csv(index=False)

        # Convert CSV to binary
        b_csv = csv.encode()

        # Create a BytesIO object
        b_io = BytesIO(b_csv)
        
        st.download_button(
            label="Download Full Sales Log",
            data=b_io,
            file_name='call_log.csv',
            mime="text/csv",
        )

        
        group_options = [
            'By County',
            'By Zip Code',
            'By NAICS Code (2 digit)', 
            'By NAICS Code (4 digit)', 
            'By Industry Tag', 
        ]

        st.subheader('Calls by Sorting')

        group_selected = st.selectbox(
            'What view do you want to see?', 
            options=group_options, 
            key='Grouping for Data'
        )

        st.subheader('Additional Filters')


        # Multi-select filter Zip Code
        filtered_df = og_data.copy()

        selected_zip = st.multiselect('Select Zip Code:', filtered_df['zip_code'].unique())
        if selected_zip:
            filtered_df = filtered_df[filtered_df['zip_code'].isin(selected_zip)]

        selected_county = st.multiselect('Select County:', filtered_df['business_county'].unique())
        if selected_county:
            filtered_df = filtered_df[filtered_df['business_county'].isin(selected_county)]

        selected_naics_2 = st.multiselect('Select NAICS 2 Digit:', filtered_df['naics_code_2_digit'].unique())
        if selected_naics_2:
            filtered_df = filtered_df[filtered_df['naics_code_2_digit'].isin(selected_naics_2)]


        selected_industry_tag = st.multiselect('Select Industry Tag:', filtered_df['industry_tag'].unique())
        if selected_industry_tag:
            filtered_df = filtered_df[filtered_df['industry_tag'].isin(selected_industry_tag)]


        data = filtered_df

        if group_selected == 'By County': 
            grouping = 'business_county'
        if group_selected == 'By Zip Code':
            grouping = 'zip_code'
        if group_selected == 'By NAICS Code (2 digit)':
            grouping = 'naics_code_2_digit'
        if group_selected == 'By NAICS Code (4 digit)':
            grouping = 'naics_code_4_digit'
        if group_selected == 'By Industry Tag':
            grouping = 'industry_tag'

        st.subheader('')
        calls = data.groupby([grouping, 'interview']).ID.count().unstack().sum(axis=1)
        interviews = data.query('interview == True').groupby(grouping).ID.count()

        data['hiring_bool'] = data['are_you_hiring'].apply(lambda x: x=='Yes')
        hiring = data.query('hiring_bool == True').groupby(grouping).ID.count()


        combined = pd.concat([calls, interviews, hiring], axis=1)
        combined.columns = ['Calls', 'Sales', 'High Value Sale']
        combined.index.name = group_selected
        if grouping == 'zip_code':
            combined.index = combined.index.astype('int').astype('str')
        combined = combined.sort_values('Sales', ascending=False)
        combined['Sales Conversion'] = combined['Sales'] / combined['Calls']
        combined['High Value % of Sales Conversion'] = combined['High Value Sale'] / combined['Sales']
        formatted_df = combined.style.format({
            'Calls' : '{:,.0f}', 
            'Sales' : '{:,.0f}', 
            'High Value Sale' : '{:,.0f}', 
            'Sales Conversion' : '{:.1%}',
            'High Value % of Sales Conversion': '{:.1%}'
        })


        st.dataframe(formatted_df)
        def to_csv_2(df):
            csv = df.to_csv(index=True)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download Current Summary Table</a>'
            return href

        # Use st.markdown to display download link
        st.markdown(to_csv_2(combined), unsafe_allow_html=True)


    # Clear the main page content before loading another page
    # This can be done using st.empty() or just by not calling other functions
    if selection == 'Summary Tables':
        run_app()
    elif selection == 'Map':
        run_page2()
    elif selection == 'Cumulative Report':
        run_page3()
    elif selection == 'Contact Sheets':
        run_page4()
    elif selection == 'Connections Tracker': 
        run_page5()

    # Need to do some testing on this branch

    pd.set_option('display.float_format', '{:.0f}'.format)
    
else:
    # Otherwise, ask for email
    st.write("Please enter your email to continue.")

# Data Load



