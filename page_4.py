import streamlit as st
import pandas as pd
import os
import base64
from io import BytesIO


og_data = pd.read_csv('call_log.csv')


def run_page4():
    
    st.title('Interactive Call Logs')
    # Function to download data as CSV
    def to_csv(df):
        csv = df.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download CSV File</a>'
        return href

    # Use st.markdown to display download link

    # Convert DataFrame to CSV
    csv = og_data.to_csv(index=False)

    # Convert CSV to binary
    b_csv = csv.encode()

    # Create a BytesIO object
    b_io = BytesIO(b_csv)
    
    st.download_button(
        label="Download Full Call Log",
        data=b_io,
        file_name='call_log.csv',
        mime="text/csv",
    )

    df = og_data.copy()
    county = st.selectbox('Select County', ['All'] + sorted(df['business_county'].fillna('None').unique()))
    industry = st.selectbox('Select Industry', ['All'] + sorted(df['industry_tag'].fillna('None').unique()))
    call_dispo = st.selectbox('Select Call Disposition', ['All'] + sorted(df['call_disposition'].fillna('None').unique()))


    filtered_df = df

    if county != 'All':
        filtered_df = filtered_df[filtered_df['business_county'] == county]


    if industry != 'All':
        filtered_df = filtered_df[filtered_df['industry_tag'] == industry]

    if call_dispo != 'All':
        filtered_df = filtered_df[filtered_df['call_disposition'] == call_dispo]


    display_cols = [
         'contact_called',
        'contact_number', 'contact_email', 'company', 'naics_code_2_digit', 
        'call_disposition', 
         'call_at',
    ]

    display_df = filtered_df[display_cols]
    display_df.columns = [
        'Contact Called',
        'Contact Number', 'Contact Email', 
        'Company', 'NAICS', 
        'Call Disposition', 
         'Call Date/Time'
    ]
    

    st.dataframe(display_df)










