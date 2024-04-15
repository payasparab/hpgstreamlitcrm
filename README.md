main_app.py
This file serves as the main entry point for the Streamlit application. It initializes the app with a title, sets up navigation via the sidebar radio buttons, and includes functions from the other pages (page_2.py, page_3.py, etc.) to run based on user navigation. The page includes a section for downloading the call log CSV file and offers different views and filters for the data based on county, zip code, NAICS code, and industry tag.

Key Streamlit Components Used:

st.set_page_config to set up the app’s page configuration including the title and layout.
st.sidebar.radio for navigation between the different app sections.
st.title to display the app’s title.
st.download_button to provide a downloadable CSV file of the sales log.
st.selectbox and st.multiselect to allow users to filter data by various fields.
page_2.py
This page is designed for mapping geolocation data. It reads geocode information and original data from CSV files and merges them to create maps based on various filtering criteria like all calls, high-value calls, sales, and industry-specific calls.

Key Streamlit Components Used:

st.selectbox for selecting the type of map visualization.
st.map for displaying geographical data on a map.
st.subheader to display sub-headers for each map type.
page_3.py
The purpose of this page is to display a sales team report by industry. It generates bar charts to visualize calls completed and sales converted by industry.

Key Streamlit Components Used:

st.pyplot to display matplotlib plots within the Streamlit app.
st.columns to create a two-column layout for displaying metrics side by side.
st.metric to display key statistics.
page_4.py
This page allows users to interact with call logs. It provides functionality to filter call logs by county, industry, and call disposition, and to download the filtered call logs as a CSV file.

Key Streamlit Components Used:

st.download_button to download a portion of the call log as a CSV file.
st.selectbox to select specific filters for displaying the call logs.
st.dataframe to display data in a tabular format.
page_5.py
The final page provides a dashboard for referrals and lead list exporting. It processes data to count connections with state business resources and outside organizations, displays this data in a table format, and allows users to export filtered call data.

Key Streamlit Components Used:

st.header and st.subheader to organize content in a hierarchical manner.
st.dataframe for displaying data in a table format.
Custom functions to download specific subsets of data as CSV files.
st.columns for side-by-side layout of referral summaries.
These components are used to build an interactive, user-friendly interface for exploring call log data and are a part of Streamlit’s API to make building data applications easier. For more details on Streamlit components and their usage, you can refer to the Streamlit API Reference.
