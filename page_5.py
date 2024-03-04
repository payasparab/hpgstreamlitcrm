
import streamlit as st
import pandas as pd
import os
from collections import Counter
import ast
import matplotlib.pyplot as plt
import base64


og_data = pd.read_csv('call_log.csv')


# Before your operation, set the chained_assignment to None
pd.options.mode.chained_assignment = None  # default='warn'


def run_page5():
    
    st.title('Referal Dashboard and Lead List Exporter')
    key_cols = [
        'company',
        'call_at',
        'contact_called',
        'phone_number_called',
        'contact_number',
        'contact_email', 
        'state_business_resources_previously_worked_with',
       'outside_organizations_previously_worked_with',
       'state_business_resources_suggested_but_not_connected',
       'outside_organizations_suggested_but_not_connected',
       'connect_with_state_business_resources',
       'connect_with_outside_organizations',
    ]  

    df = og_data[key_cols]
    df['call_at'] = pd.to_datetime(df['call_at'])

    # Function to safely evaluate strings as lists
    def safe_eval_list(val):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []

    # Identify columns to process (exclude 'company', 'call_at', 'contact_called')
    columns_to_process = df.columns[6:]

    # Initialize a DataFrame to store the counts for each string in each column
    string_counts = {col: Counter() for col in columns_to_process}

    # Count the frequency of each string in the specified columns
    for col in columns_to_process:
        df[col] = df[col].apply(safe_eval_list)
        for items in df[col]:
            string_counts[col].update(items)

    # Convert the counters to a DataFrame
    counts_df = pd.DataFrame.from_dict(string_counts, orient='index').fillna(0).T

    ### TOTAL IMPACT ###

    impact_series = counts_df.sum(axis=0)


    # Create a dictionary from the series for the funnel data
    funnel_dict = {'state_business_resources': [], 'outside_organizations': []}

    # Populate the funnel dictionary with the series data
    for key, value in impact_series.items():
        funnel_key = 'state_business_resources' if 'state_business_resources' in key else 'outside_organizations'
        funnel_dict[funnel_key].append((key, value))

    # Sort the funnel data by the count, reversed (largest at the top)
    for key in funnel_dict:
        funnel_dict[key].sort(key=lambda x: x[1], reverse=True)

    # Streamlit app layout
    st.header('1. Referrals Summary')

    # Using columns to layout the funnels side by side
    col1, col2 = st.columns(2)

    # Function to display funnel data as metrics
    def display_funnel_metrics(col, funnel_data, header):
        with col:
            st.header(header)
            for stage, value in funnel_data:
                stage_name = stage.replace('_', ' ').capitalize()
                st.metric(label=stage_name, value=f"{int(value)}")

    # Display the metrics for both funnels
    display_funnel_metrics(col1, funnel_dict['state_business_resources'], '1.1 State Resources')
    display_funnel_metrics(col2, funnel_dict['outside_organizations'], '1.2 Outside Organizations')


    st.header('2. Connected Businesses by Organization')
    # Using columns to layout the funnels side by side

    st.subheader('2.1 Connecting with Government Resources')
    col1_table = counts_df[['connect_with_state_business_resources']].sort_values(
        'connect_with_state_business_resources', 
        ascending=False
    )
    col1_table.columns = ['Connected Businesses']
    col1_table = col1_table[col1_table['Connected Businesses'] >0]
    st.dataframe(col1_table)

    st.subheader('2.2 Connecting with Outside Organizations')
    col2_table = counts_df[['connect_with_outside_organizations']].sort_values(
        'connect_with_outside_organizations', 
        ascending=False
    )
    col2_table.columns = ['Connected Businesses']
    col2_table = col2_table[col2_table['Connected Businesses'] >0]
    st.dataframe(col2_table)

    st.header('3. Export Business by Organizations')

    st.subheader('3.1 Export Call Data with Government Referrals')
    resource_select = list(col1_table.index.values)
    
    selected_state_source = st.selectbox(
        'Select the State Resource You Want To Track Referrals for', 
        resource_select
    )
    def check_source(row, source):
        return source in row.connect_with_state_business_resources
    
    if selected_state_source:
        export_state = df[df.apply(lambda x: check_source(x, selected_state_source), axis=1)]
        exportable_state = export_state[[
            'company', 'call_at', 'contact_called', 'phone_number_called', 'contact_number', 'contact_email'
        ]]
        st.dataframe(exportable_state)

    def to_csv_1(df):
        csv = df.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download Current State Business Referrals</a>'
        return href

    # Use st.markdown to display download link
    st.markdown(to_csv_1(exportable_state), unsafe_allow_html=True)

    st.subheader('3.2 Export Call Data with Outside Organization Referrals')
    resource_select_2 = list(col2_table.index.values)
    
    selected_state_source_2 = st.selectbox(
        'Select the Outside Organization You Want To Track Referrals for', 
        resource_select_2
    )
    #TODO: awful code LMAO, need to not duplicate, needs to be cleaned.
    def check_source_2(row, source):
        return source in row.connect_with_outside_organizations
    if selected_state_source_2:
        
        export_state = df[df.apply(lambda x: check_source_2(x, selected_state_source_2), axis=1)]
        exportable_org = export_state[[
            'company', 'call_at', 'contact_called', 'phone_number_called', 'contact_number', 'contact_email'
        ]]
        st.dataframe(exportable_org)
        def to_csv_2(df):
            csv = df.to_csv(index=True)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download Current Outside Organization Referrals</a>'
            return href

        # Use st.markdown to display download link
        st.markdown(to_csv_2(exportable_org), unsafe_allow_html=True)




        








