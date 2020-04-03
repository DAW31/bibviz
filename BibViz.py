import plotly.graph_objects as go
import json
import networkx as nx
import matplotlib.pyplot as plt
from tinydb import TinyDB
with open("db.json", "r") as read_file:
    data=json.load(read_file)
G = nx.Graph()
try:
    current_number = 1
    while current_number <=100000000000:
        current_number = str(current_number)
        tconnections=str(data['connections'][current_number]['TitleID'])
        aconnections=str(data['connections'][current_number]['AuthorID'])
        title=(data['titles'][tconnections]['Title'])
        author=(data['authors'][aconnections]['Author'])
        print (title)
        G.add_node(title,color='red')
        G.add_node(author,color='green')
        G.add_edges_from([(author,title)])
        current_number = int(current_number)
        current_number += 1
except:
    KeyError
pos = nx.spring_layout(G, k=1.5, iterations=600)
for n, p in pos.items():
    color=nx.get_node_attributes(G,'color')
    G.nodes[n]['pos'] = p
    G.nodes[n]['color'] = color[n]

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=[],
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['marker']['color']+=tuple([G.nodes[node]['color']])
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['size']+=tuple([len(adjacencies[1])*8])
    print ("adj1",adjacencies)
    node_info = adjacencies[0],' Number of connections: ',str(len(adjacencies[1])),' Connections: ',adjacencies[1]
    node_trace['text']+=tuple([node_info])


fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Connections between Bibtex articles',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="No. of connections",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
fig.show()

nx.draw(
    G,
    with_labels=True
)
plt.show()