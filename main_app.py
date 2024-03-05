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


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Username"
    )

    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

st.set_page_config(
        page_title="HPG CRM Demo",
        page_icon="hpg_logo.png",
        layout="wide",
    )

# Data Load

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

