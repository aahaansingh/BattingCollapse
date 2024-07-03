import streamlit as st

st.write("## What is Batting Collapse?")
st.write('BattingCollapse is a tool that allows you to visualise and retrieve "Smart Stats" for player performance in the IPL.')
st.write("## So How Do These Smart Stats Work?")
st.write("These Smart Stats are based off of basic performance metrics like average and strike rate. They're smart because they're adjusted for the performance of other players in the same games. Essentially, these Smart Stats measure how well the player did compared to their peers.")
st.write("For example, a strike rate of 150 is far less impressive now than it would have been in the first season of the IPL. Smart Stats adjust for this by calculating the ratio of the player's strike rate to the average strike rate of a top 6 batsman over every match played by that player. That's why, despite Kohli having one of his quickest-scoring seasons in 2024, his true strike rate was around average.")
st.write("Both true average and true S/R are calculated relative to other top 6 batsmen, while true bowling S/R and true economy are calculated relative to every other bowler.")
st.write('The formula is (player_stat/peer_stat - 1) * 100, so a player with an average 1.2 times that of their peers would have a true average of 20, and an "average" player would have a true average of 0.')
st.write("## What Makes These Stats Useful?")
st.write("The nice thing about these stats is that they allow you to build a clearer overall picture of the player's abilities by adjusting for both conditions and era. There's definitely more advanced metrics out there, but these ones are useful enough without being opaque. That being said, I plan to add some more advanced metrics soon.")
st.write("## Credit")
st.write("The data used for these stats is available on [CricSheet](https://cricsheet.org/matches/) and was relationalized with [CricBase](https://github.com/aahaansingh/CricBase).")
st.write("I took the idea for these adjusted statistics from Jarrod Kimber's [Good Areas](https://www.goodareas.co/), although I'm not sure if they're implemented in the exact same way.")

