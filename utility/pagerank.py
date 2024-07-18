from supabase import Client
import pandas as pd
import numpy as np
import streamlit as st
import networkx as nx

@st.cache_data(ttl=600)
def yearly_results(_connection: Client, season: str):
    return pd.DataFrame.from_dict(
        _connection.table("match").select("start_date, match_number, batting_first, chasing, winner, target_runs, chasing_score, target_balls, chasing_balls").eq("season", season).execute().data)

@st.cache_data(ttl=600)
def basic_team_rank(_connection: Client, season: str) :
    results = yearly_results(_connection, season)

    batting_first_winner = results.iloc[np.where(results["batting_first"] == results["winner"])][["batting_first", "chasing"]]
    chasing_winner = results.iloc[np.where(results["chasing"] == results["winner"])][["chasing", "batting_first"]]
    batting_first_winner = batting_first_winner.rename(columns={"batting_first":"winner", "chasing":"loser"})
    chasing_winner = chasing_winner.rename(columns={"chasing":"winner", "batting_first":"loser"})

    adj_list = pd.concat([batting_first_winner, chasing_winner]).values.tolist()
    team_graph = nx.MultiDiGraph(adj_list)
    adj_mtx = nx.adjacency_matrix(team_graph).toarray()
    idx_map = list(team_graph.nodes)
    markov_mtx = np.nan_to_num(adj_mtx/adj_mtx.sum(axis=0,keepdims=1), nan=1/len(idx_map))

    alpha = .85
    google_mtx = alpha*markov_mtx + (1-alpha)/markov_mtx.shape[0]*np.ones(markov_mtx.shape)
    pi = np.full((len(idx_map)), 1/len(idx_map))
    while True :
        pi_new = google_mtx@pi
        if max_diff(pi_new, pi) < 0.0001 :
            break
        pi = pi_new

    results = pd.DataFrame(data=pi, index=idx_map, columns=["rating"]).sort_values(by=["rating"], ascending=False)
    return results

@st.cache_data(ttl=600)
def weighted_team_rank_hist(_connection: Client, season: str) :
    results = yearly_results(_connection, season)
    results = results.sort_values(by=["start_date"], ignore_index=True)
    starting_match = 10 # Can't start from match 1 because not every team will have played
    ranking_hist = pd.DataFrame()
    while starting_match <= len(results) :
        results_trunc = results.head(starting_match)
        ranking = pagerank_score(results_trunc)
        starting_match += 1
        ranking_hist = pd.concat([ranking_hist, ranking], axis=0, ignore_index=True)
    ranking_hist.index = ranking_hist.index + 10
    ranking_hist["Match Number"] = ranking_hist.index
    ranking_hist_long=pd.melt(ranking_hist, id_vars=['Match Number'], value_vars=ranking_hist.columns, var_name="Team", value_name="Rating")
    return ranking_hist_long

@st.cache_data(ttl=600)
def pagerank_score(results:pd.DataFrame) :
    batting_first_winner = results.iloc[np.where(results["batting_first"] == results["winner"])][["batting_first", "chasing", "target_runs", "chasing_score"]]
    chasing_winner = results.iloc[np.where(results["chasing"] == results["winner"])][["chasing", "batting_first", "target_balls", "chasing_balls"]]
    
    batting_first_winner["margin"] = 1+(batting_first_winner["target_runs"]-batting_first_winner["chasing_score"])/batting_first_winner["chasing_score"]
    chasing_winner["margin"] = 1+(chasing_winner["target_balls"]-chasing_winner["chasing_balls"])/chasing_winner["chasing_balls"]
    batting_first_winner["margin"].clip(upper=1.2, inplace=True)
    chasing_winner["margin"].clip(upper=1.2, inplace=True)
    
    batting_first_winner = batting_first_winner.drop(columns=["target_runs", "chasing_score"])
    chasing_winner = chasing_winner.drop(columns=["target_balls", "chasing_balls"])
    batting_first_winner = batting_first_winner.rename(columns={"batting_first":"winner", "chasing":"loser"})
    chasing_winner = chasing_winner.rename(columns={"chasing":"winner", "batting_first":"loser"})
    
    winner_df = pd.concat([batting_first_winner, chasing_winner]).sort_index(ascending=False)
    recent_clip = 40
    if len(winner_df) > recent_clip :
        winner_df.loc[winner_df.tail(len(winner_df)-recent_clip).index, "margin"] = winner_df.loc[winner_df.tail(len(winner_df)-recent_clip).index, "margin"]/2

    adj_list_w = winner_df.values.tolist()

    for edge in adj_list_w :
        weight = edge.pop(2)
        weight_dict = {"weight" : weight}
        edge.append(weight_dict)
    team_graph_w = nx.MultiDiGraph(adj_list_w)
    idx_map = list(team_graph_w.nodes)
    adj_mtx_w = nx.adjacency_matrix(team_graph_w).toarray()

    markov_mtx_w = np.nan_to_num(adj_mtx_w/adj_mtx_w.sum(axis=0,keepdims=1), nan=1/len(idx_map)) # deal w/sinks
    alpha = 0.85
    google_mtx_w = alpha*markov_mtx_w + (1-alpha)/markov_mtx_w.shape[0]*np.ones(markov_mtx_w.shape)
    pi_w = np.full((len(idx_map)), 1/len(idx_map))
    while True :
        pi_new_w = google_mtx_w@pi_w
        if max_diff(pi_new_w, pi_w) < 0.0001 :
            break
        pi_w = pi_new_w
    
    markov_mtx_l = np.nan_to_num(adj_mtx_w.T/adj_mtx_w.T.sum(axis=0,keepdims=1), nan=1/len(idx_map))
    google_mtx_l = alpha*markov_mtx_l + (1-alpha)/markov_mtx_l.shape[0]*np.ones(markov_mtx_l.shape)
    pi_l = np.full((len(idx_map)), 1/len(idx_map))
    while True :
        pi_new_l = google_mtx_l@pi_l
        if max_diff(pi_new_l, pi_l) < 0.0001 :
            break
        pi_l = pi_new_l
    
    pi = pi_w-pi_l
    ranking = pd.DataFrame(data=pi.reshape((1,len(idx_map))), columns=idx_map)
    return ranking

def max_diff(a:np.ndarray, b:np.ndarray) :
    c = np.abs(a-b)
    return c.max()

