import streamlit as st
import plotly.express as px
from utility.utilities import init_connection
from utility.pagerank import weighted_team_rank_hist
import warnings
import pandas as pd

supabase = init_connection()
st.write('## Team Ratings')
st.write('For more information on the somewhat arbitrary methodology behind these ratings, hang tight because there\'s an explanation coming!')
season = st.selectbox(
    "Which season do you want to see ratings for?", 
    ("2024", "2023", "2022", "2021", "2020/21", "2019", "2018", "2017", "2016", "2015",
    "2014", "2013", "2012", "2011", "2009/10", "2009", "2007/08"))
warnings.filterwarnings("ignore", message="invalid value encountered in divide")
ranking = weighted_team_rank_hist(supabase, season)
chart = px.line(data_frame=ranking, x="Match Number", y="Rating", color="Team")
st.plotly_chart(chart)

