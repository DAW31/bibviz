import plotly.graph_objects as go
import json
import networkx as nx
with open("db.json", "r") as read_file:
    data=json.load(read_file)
G = nx.Graph()
max_number=(len(data['connections']))
try:
    current_number = 1
    while current_number <= max_number:
        current_number = str(current_number)
        tconnections=str(data['connections'][current_number]['TitleID'])
        aconnections=str(data['connections'][current_number]['AuthorID'])
        title=(data['titles'][tconnections]['Title'])
        author=(data['authors'][aconnections]['Author'])
        G.add_node(title,color='red')
        G.add_node(author,color='blue')
        G.add_edges_from([(author,title)])
        current_number = int(current_number)
        current_number += 1
except:
    KeyError
pos = nx.spring_layout(G, dim=2, k=None, pos=None, fixed=None, iterations=50, weight='weight', scale=1.0)
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
        color=[],
        size=[],
))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['marker']['color']+=tuple([G.nodes[node]['color']])
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['size']+=tuple([len(adjacencies[1])*8])
    node_text.append('<b>'+str(adjacencies[0])+'</b><i><br>Number of connections: '+str(len(adjacencies[1]))+"<br>Connections: "+str(adjacencies[1]).replace("{","").replace("}", "").replace(":","").replace("'",""))
    
node_trace.text = node_text


fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Connections between Bibtex articles',
                titlefont=dict(size=20),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=5,l=5,r=5,t=5),
                annotations=[ dict(
                    text="No. of connections",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
fig.show()
