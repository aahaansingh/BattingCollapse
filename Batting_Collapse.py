import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utility.utilities import init_connection, run_query

supabase = init_connection()
st.write('## Welcome to the BattingCollapse Tool!')
st.write('For more about what this tool is and how it works, check out the about page!')
view = st.selectbox(
    "Select a display view for the statistics", 
    ("Plot", "Spreadsheet"))
start_date = st.selectbox(
    "First season to include in calculation", 
    ("2007/08", "2009", "2009/10", "2011", "2012", "2013", "2014", "2015", "2016", "2017",
    "2018", "2019", "2020/21", "2021", "2022", "2023", "2024"))
end_date = st.selectbox(
    "Most recent season to include in calculation", 
    ("2024", "2023", "2022", "2021", "2020/21", "2019", "2018", "2017", "2016", "2015",
    "2014", "2013", "2012", "2011", "2009/10", "2009", "2007/08"))
if view == "Spreadsheet" :
    stat = st.selectbox(
        "Select a statistic to display", 
        ("true_avg", "true_sr", "true_bowling_sr", "true_econ"))

    rows = run_query(supabase, stat, start_date, end_date)

    df_rows = pd.DataFrame.from_dict(rows.data)
    st.dataframe(df_rows)
else :
    role = st.selectbox(
        "Type of statistics to display", 
        ("Batting", "Bowling"))
    if role == "Batting" :
        runs_cutoff = st.slider(
             "The minimum number of runs required to be displayed on the plot",
             100, 3000, 1000
        )
        true_avg_rows = run_query(supabase, "true_avg", start_date, end_date)
        true_sr_rows = run_query(supabase, "true_sr", start_date, end_date)
        true_avg_df = pd.DataFrame.from_dict(true_avg_rows.data)
        true_sr_df = pd.DataFrame.from_dict(true_sr_rows.data)

        true_avg_df = true_avg_df.loc[np.where(true_avg_df["runs_scored"] >= runs_cutoff)]
        avg_sr_merged = true_avg_df.merge(true_sr_df)

        chart = px.scatter(
            avg_sr_merged,
            x="true_avg", 
            y="true_sr",
            hover_data=["player_name"],
            color="avg_position")
        st.plotly_chart(chart)
    else :
        balls_cutoff = st.slider(
             "The minimum number of balls delivered required to be displayed on the plot",
             100, 2400, 1000
        )
        true_econ_rows = run_query(supabase, "true_econ", start_date, end_date)
        true_bowling_sr_rows = run_query(supabase, "true_bowling_sr", start_date, end_date)
        true_econ_df = pd.DataFrame.from_dict(true_econ_rows.data)
        true_bowling_sr_df = pd.DataFrame.from_dict(true_bowling_sr_rows.data)

        true_econ_df = true_econ_df.loc[np.where(true_econ_df["balls_delivered"] >= balls_cutoff)]
        econ_sr_merged = true_econ_df.merge(true_bowling_sr_df)

        chart = px.scatter(
            econ_sr_merged,
            x="true_econ", 
            y="true_sr",
            hover_data=["player_name"])
        st.plotly_chart(chart)