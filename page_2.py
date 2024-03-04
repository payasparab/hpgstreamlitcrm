import streamlit as st
import pandas as pd
import os

# Create geocodes for mapping

og_data = pd.read_csv('call_log.csv')

def run_page2():
    # Add content for page 2 here
    geocode_data = pd.read_csv('geocodes.csv')
    joined_geocode_data = pd.concat([og_data, geocode_data], axis=1)
    clean_for_map = joined_geocode_data.query('State == "DE"') # Remove non DE mismatched
    clean_for_map.rename(
            columns={
                'Latitude' : 'lat',
                'Longitude' : 'lon'
            }, 
            inplace=True
        )
    map_type = st.selectbox(
        'Select the type of mapping', 
        ['All Calls', 'By High Value', 'Sales', 'Calls by Industry']
    )
    
    if map_type == 'All Calls':
        st.subheader('All Calls')
        st.map(
            clean_for_map,
        )

    if map_type == 'By High Value':
        st.subheader('High Value Sales')
        st.map(
            clean_for_map.query(
                'are_you_hiring =="Yes"'
            )
        )

    if map_type == 'Sales':
        st.subheader('Sales')
        st.map(
            clean_for_map.query(
                'call_disposition =="Connected - Interested"'
            )
        )


    if map_type == 'Calls by Industry':
        st.subheader('By Industry')
        industries = list(clean_for_map.industry_tag.unique())
        industry_selected = st.selectbox(
            'Select the industry you want to visualize',
            options=industries
        )
        st.map(
            clean_for_map.query(
                'industry_tag =="{}"'.format(industry_selected)
            )
        )



    

