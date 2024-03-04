import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta


## Grab latest month ##

# Get the current date
current_date = datetime.now()
# Calculate the first day of the current month
first_day_of_current_month = current_date.replace(day=1)
# Subtract one day from the first day of the current month to get the last day of the previous month
last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
# Now we have the year and month for the latest complete month
latest_complete_month = last_day_of_previous_month.strftime("%Y-%m")
# To get just the month as a number
latest_complete_month_number = last_day_of_previous_month.month
# To get the name of the month
latest_complete_month_name = last_day_of_previous_month.strftime("%B")


og_data = pd.read_csv('call_log.csv')
og_data['interview'] = og_data['call_disposition'].apply(
    lambda x: x == 'Connected - Interested'
)
og_data['call_at'] = pd.to_datetime(og_data['call_at'])

call_data = og_data.copy()

# Set the month and year you want to filter by
month = latest_complete_month_number  # for March
year = 2023  # for the year 2023

# Filter the DataFrame
filtered_df = call_data.copy()


def run_page3():
    
    # Function to plot a bar chart
    def plot_bar_chart(df, title, color):
        fig, ax = plt.subplots()
        df = df.sort_values('ID', ascending=True)
        ax.barh(df.index, df['ID'], color=color)
        plt.title(title)
        for i, v in enumerate(df['ID']):
            ax.text(v + 3, i, str(v), color='black', va='center')
        return fig

        # Set up the Streamlit page
    st.title('Sales Team Report, by Industry')
    st.header('HPG Client BD Team')

    # Overview section
    col1, col2 = st.columns(2)
    col1.metric("Calls Completed", filtered_df.interview.count())
    col2.metric("Sales Converted", filtered_df.interview.sum())

    calls_made = filtered_df.copy()
    interviews = filtered_df[filtered_df.interview]

    with col1: 
        # Plot calls completed
        st.subheader('Calls Completed')
        call_df = calls_made.groupby('industry_tag').ID.count().to_frame()
        calls_chart = plot_bar_chart(call_df, 'Calls Completed', 'blue')
        st.pyplot(calls_chart)

    # Plot interviews completed
    with col2:
        st.subheader('Sales Converted')
        interview_df = interviews.groupby('industry_tag').ID.count().to_frame()
        interviews_chart = plot_bar_chart(interview_df, 'Sales Converted', 'red')
        st.pyplot(interviews_chart)









