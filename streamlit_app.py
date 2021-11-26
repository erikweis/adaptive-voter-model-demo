from streamlit_force_graph_simulator import st_graph, ForceGraphSimulation
import streamlit as st

import networkx as nx
import random
from collections import Counter

st.title("Adaptive Voter Model")
# Render the h1 block, contained in a frame of size 200x200.

text = "".join("""
With the traditional voter model, a random node takes the state of one of its neighbors at each time step. With the adaptive voter model
nodes rewire an edge from a node with an opposite opinion, with probability p. Otherwise, nodes take the state of a neighbor, with probability 1-p.
""".split("\n"))

st.markdown(text)

def initialize_simulation():

    #initialize graph   
    G = nx.les_miserables_graph()
    for node in G.nodes:
        G.nodes[node]['color'] = random.choice(['red','blue'])

    #create simulation object
    return ForceGraphSimulation(G,link_attributes_to_track = ['color'])

def run_simulation(F):

    for _ in range(2000):

        #new event
        F.new_event()

        #choose node to act on
        node = random.choice(list(F.graph.nodes))

        #get neighbors
        neighbors = list(F.graph[node])

        #rewire or take a neighbor's state
        if random.random() < st.session_state.prob_rewire:

            #try to rewire a node with opposite opinion
            opp_neighbors = [n for n in neighbors if F.graph.nodes[n]['color'] != F.graph.nodes[node]['color'] ]
            if opp_neighbors:
                old_neighbor = random.choice(opp_neighbors)

                # choices = list(nx.ego_graph(G,node,radius=2,center=False).nodes)
                choices = list(F.graph.nodes)
                choices.remove(node)
                new_neighbor = random.choice(choices)
                F.add_edge(node,new_neighbor)
                F.remove_edge(node,old_neighbor)

        else:
            #take a neighbors state
            if neighbors:
                neighbor = random.choice(neighbors)
                neighbor_color = F.graph.nodes[neighbor]['color']
                F.set_node_attributes(node, color=neighbor_color)

        # #stopping function
        # colors = list(nx.get_node_attributes(F.graph,'color').values())
        # counts = Counter(colors)
        # print(counts)
        # max_prop = max(counts.values())/F.graph.number_of_nodes()
        # if max_prop > 0.9:
        #     stop = True

    return F

F = initialize_simulation()

if 'graph' not in st.session_state:
    st.session_state.graph = F.initial_graph_json
if 'events' not in st.session_state:
    st.session_state.events = F._events

def start_callback():

    F = initialize_simulation()
    F = run_simulation(F)
    st.session_state.graph = F.initial_graph_json
    st.session_state.events = F.events


def stop_callback():

    F = initialize_simulation()
    st.session_state.graph = F.initial_graph_json
    st.session_state.events = [[{'new_graph':F.initial_graph_json}]]


st.session_state.prob_rewire = st.sidebar.slider('Probability Rewire',key='rewire_slider',min_value=0.0,max_value=1.0,value=0.5,on_change=stop_callback)
st.session_state.cooldownTicks = st.sidebar.slider('Cooldown Ticks',key='cooldownTicks_slider',min_value =0,max_value=1000,value=100,on_change=stop_callback)
st.session_state.simulation_speed = st.sidebar.slider('Simulation Speed',key='speed_slider',min_value = 10,max_value=300,value=50,on_change=stop_callback)

graphprops = {
    'cooldownTicks':st.session_state.cooldownTicks,
    'height':600
}

w = st_graph(
    st.session_state.graph, 
    st.session_state.events, 
    st.session_state.simulation_speed, graphprops = graphprops,key="graph")

st.write(w)
st.sidebar.button('Run Simulation',key='start_button',on_click=start_callback)
st.sidebar.button('Stop Simulation',key='stop_button',on_click=stop_callback)

