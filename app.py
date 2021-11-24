from networkx.generators.social import les_miserables_graph
import streamlit.components.v1 as components  # Import Streamlit

# Render the h1 block, contained in a frame of size 200x200.
#components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)

# Import the wrapper function from your package
from streamlit_force_graph_simulator import st_graph, ForceGraphSimulation
import streamlit as st

import json
import networkx as nx
from networkx.readwrite import json_graph
import time
import random

st.title("Adaptive Voter Model")

# Store and display the return value of your custom component
# label = st.sidebar.text_input('Label', 'Hello world')
# min_value, max_value = st.sidebar.slider("Range slider", 0, 100, (0, 50))

# v = st_custom_slider(label=label, min_value=min_value, max_value=max_value,key="slider")
# st.write(v)

#initialize graph
G = nx.les_miserables_graph()
for node in G.nodes:
    G.nodes[node]['color'] = random.choice(['red','blue'])

F = ForceGraphSimulation(G,link_attributes_to_track = ['color'])


data = json_graph.node_link_data(G)


for _ in range(500):
    F.new_event()
    node = random.choice(list(F.graph.nodes))
    neighbors = list(F.graph[node])
    node_color = F.graph.nodes[node]['color']
    if random.random() < 0.1:
        if neighbors:
            neighbor = random.choice(neighbors)
            neighbor_color = F.graph.nodes[neighbor]['color']
            F.set_node_attributes(node, color=neighbor_color)

    else:
        opp_neighbors = [n for n in neighbors if F.graph.nodes[n]['color'] != F.graph.nodes[node]['color'] ]
        if opp_neighbors:
            old_neighbor = random.choice(opp_neighbors)

            # choices = list(nx.ego_graph(G,node,radius=2,center=False).nodes)
            choices = list(F.graph.nodes)
            choices.remove(node)
            new_neighbor = random.choice(choices)
            F.add_edge(node,new_neighbor)
            F.remove_edge(node,old_neighbor)

events = F._events


# if 'graph_data' not in st.session_state:
#     st.session_state.initial_data = data 

# w = st_graph(data = st.session_state.graph_data,key="graph")
# st.write(w)



w = st_graph(data,events, key="graph")
st.write(w)

# def color_callback():

#     st.session_state.initial_data = json_graph.node_link_data(G)


# st.sidebar.button('Run Simulation',key='button',on_click=color_callback)



# st.write(st_graph(data=data,key="graph"))