import streamlit as st
import plotly.express as px
from utility.utilities import init_connection, run_query

supabase = init_connection()
st.write('## Phase by Phase Stats')
st.write('These follow the same methodology as the original true stats (except for runs per innings at the death, as death average is not a useful measure).')
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
phase = st.selectbox(
    "Select a phase of the innings to analyze", 
    ("Powerplay (1-6)", "Middle Overs (7-15)", "Death Overs(16-20)"))
if view == "Spreadsheet" :
    if phase == "Powerplay (1-6)" :
        stat = st.selectbox(
            "Select a statistic to display", 
            ("true_avg", "true_sr", "true_bowling_sr", "true_econ"))
        fn_name = "pp_" + stat
    elif phase == "Middle Overs (7-15)" :
        stat = st.selectbox(
            "Select a statistic to display", 
            ("true_avg", "true_sr", "true_bowling_sr", "true_econ"))
        fn_name = "mo_" + stat
    else :
        stat = st.selectbox(
            "Select a statistic to display", 
            ("true_rpi", "true_sr", "true_bowling_sr", "true_econ"))
        fn_name = "death_" + stat
    df = run_query(supabase, fn_name, start_date, end_date)
    st.dataframe(df)
else :
    role = st.selectbox(
            "Type of statistics to display", 
            ("Batting", "Bowling"))
    num_cutoff = st.slider(
             "The number of players to display",
             5, 100, 15)
    label = st.checkbox("Show names")
    if role == "Batting" :
        true_avg_fn = ""
        true_sr_fn = ""
        avg_metric = "true_avg"
        if phase == "Powerplay (1-6)" :
            true_avg_fn = "pp_true_avg"
            true_sr_fn = "pp_true_sr"
        elif phase == "Middle Overs (7-15)" :
            true_avg_fn = "mo_true_avg"
            true_sr_fn = "mo_true_sr"
        else :
            true_avg_fn = "death_true_rpi"
            true_sr_fn = "death_true_sr"
            avg_metric = "true_rpi"
        true_avg_df = run_query(supabase, true_avg_fn, start_date, end_date)
        true_sr_df = run_query(supabase, true_sr_fn, start_date, end_date)
        
        true_avg_df = true_avg_df.sort_values(by=["runs_scored"], ascending=False).head(num_cutoff)
        avg_sr_merged = true_avg_df.merge(true_sr_df)

        if not label :
            chart = px.scatter(
                avg_sr_merged,
                x=avg_metric,
                y="true_sr",
                hover_data=["name"],
                color="avg_position")
        else :
            chart = px.scatter(
                avg_sr_merged,
                x=avg_metric,
                y="true_sr",
                text="name",
                color="avg_position")
        st.plotly_chart(chart)
    else :
        true_econ_fn = "true_econ"
        true_bowling_sr_fn = "true_bowling_sr"
        if phase == "Powerplay (1-6)" :
            true_econ_fn = "pp_" + true_econ_fn
            true_bowling_sr_fn = "pp_" + true_bowling_sr_fn
        elif phase == "Middle Overs (7-15)" :
            true_econ_fn = "mo_" + true_econ_fn
            true_bowling_sr_fn = "mo_" + true_bowling_sr_fn
        else :
            true_econ_fn = "death_" + true_econ_fn
            true_bowling_sr_fn = "death_" + true_bowling_sr_fn
        
        true_econ_df = run_query(supabase, true_econ_fn, start_date, end_date)
        true_bowling_sr_df = run_query(supabase, true_bowling_sr_fn, start_date, end_date)

        true_econ_df = true_econ_df.sort_values(by=["balls_delivered"], ascending=False).head(num_cutoff)
        econ_sr_merged = true_econ_df.merge(true_bowling_sr_df)

        if not label :
            chart = px.scatter(
                econ_sr_merged,
                x="true_econ",
                y="true_sr",
                hover_data=["name"])
        else :
            chart = px.scatter(
                econ_sr_merged,
                x="true_econ",
                y="true_sr",
                text="name")
        st.plotly_chart(chart)