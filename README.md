# Streamlit CRM App App Overview
# By the Handy Point Group (www.handypointgroup.com)

## Overview
This Streamlit application is structured across multiple pages, each with a specific functionality. Here is a detailed breakdown of what each page does, along with the Streamlit components they use.

### `main_app.py`
The main entry point of the application. It sets up the page configuration and sidebar navigation to access various sections of the app.

#### Functionality:
- Initialize the app with a title.
- Set up sidebar navigation using radio buttons.
- Incorporate functions from other pages based on user navigation.
- Allow users to download a call log CSV file.
- Offer different data views and filters.

#### Streamlit Components:
- `st.set_page_config`
- `st.sidebar.radio`
- `st.title`
- `st.download_button`
- `st.selectbox`
- `st.multiselect`

### `page_2.py`
Handles mapping of geolocation data from CSV files and displays maps based on different filters.

#### Functionality:
- Read geocode and original data.
- Merge data to create maps for various call types.

#### Streamlit Components:
- `st.selectbox`
- `st.map`
- `st.subheader`

### `page_3.py`
Displays a sales team report by industry using bar charts for calls and sales.

#### Functionality:
- Generate bar charts to visualize call and sales data.

#### Streamlit Components:
- `st.pyplot`
- `st.columns`
- `st.metric`

### `page_4.py`
Allows interaction with call logs, including filtering and downloading of call data.

#### Functionality:
- Filter call logs by various criteria.
- Download filtered call logs as CSV.

#### Streamlit Components:
- `st.download_button`
- `st.selectbox`
- `st.dataframe`

### `page_5.py`
Provides a dashboard for referrals and exporting of lead lists.

#### Functionality:
- Count connections with resources.
- Display and export filtered call data.

#### Streamlit Components:
- `st.header`
- `st.subheader`
- `st.dataframe`
- Custom functions to handle data exporting.
- `st.columns`

## Notes
Each page uses specific Streamlit components to facilitate the creation of an interactive and user-friendly interface for data exploration. For more detailed information on the components and their usage, refer to the [Streamlit API Reference](https://docs.streamlit.io/library/api-reference).
