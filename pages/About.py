import streamlit as st

st.write("## What is Batting Collapse?")
st.write('BattingCollapse is a tool that allows you to visualise and retrieve "True Stats" for player performance in the IPL.')
st.write("## So How Do These True Stats Work?")
st.write("These True Stats are based off of basic performance metrics like average and strike rate. They're smart because they're adjusted for the performance of other players in the same games. Essentially, these True Stats measure how well the player did compared to their peers.")
st.write("For example, a strike rate of 150 is far less impressive now than it would have been in the first season of the IPL. True Stats adjust for this by calculating the ratio of the player's strike rate to the average strike rate of a top 6 batsman over every match played by that player. That's why, despite Kohli having one of his quickest-scoring seasons in 2024, his true strike rate was around average.")
st.write("Both true average and true S/R are calculated relative to other top 6 batsmen, while true bowling S/R and true economy are calculated relative to every other bowler.")
st.write('The formula is (player_stat/peer_stat - 1) * 100, so a player with an average 1.2 times that of their peers would have a true average of 20, and an "average" player would have a true average of 0.')
st.write("## What do Phase Stats Do?")
st.write("Phase stats are the above metrics calculated over three phases: powerplay, middle overs, and death. This is important because it allows one to compare players in their specialized roles. For example, we likely care more about an opener's true average and strike rate in the powerplay than death, a batter's true batting stats in the powerplay is a far more useful metric than overall true batting stat.")
st.write("Furthermore, instead of using true average at the death, I have opted to use true runs per innings because death average is both an extremely noisy and extremely useless metric. Runs per innings at the death does end up significantly biasing finishers, so it's not a good metric if you want to understand the performance of players who take the game deep.")
st.write("## What Makes These Stats Useful?")
st.write("The nice thing about these stats is that they allow you to build a clearer overall picture of the player's abilities by adjusting for both conditions and era. There's definitely more advanced metrics out there, but these ones are useful enough without being opaque. That being said, I plan to add some more advanced metrics soon.")
st.write("## Credit")
st.write("The data used for these stats is available on [CricSheet](https://cricsheet.org/matches/) and was relationalized with [CricBase](https://github.com/aahaansingh/CricBase).")
st.write("I took the idea for these adjusted statistics from Jarrod Kimber's [Good Areas](https://www.goodareas.co/), although I'm not sure if they're implemented in the exact same way.")

