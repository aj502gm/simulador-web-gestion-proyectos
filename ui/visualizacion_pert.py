import networkx as nx
from pyvis.network import Network
import tempfile
import os
import re

def render_pert_tasks(tasks: any) -> tuple[str, list]:
    """
   GIVEN AN OBJECT OF TASKS, CREATES A PERT GRAPH AND SHOWS
   THE CRITICAL PATH.
    """
    # START GRAPH
    G = nx.DiGraph()
    # CREATE ALL NODES
    for data in tasks['activities']:
        G.add_node(
            data['id'],
            duracion=data['duration']["most_likely"],
            title=f"Tarea {data["name"]}<br>Duración: {data["duration"]["most_likely"]} días"
        )
        for dep in data["dependencies"]:
            G.add_edge(dep, data['id'])

    # CRITICAL PATH
    longest_path = nx.dag_longest_path(G, weight='duracion')
    longest_path_edges = list(zip(longest_path, longest_path[1:]))

    net = Network(
        directed=True,
        height="300px",
        width="100%",
        bgcolor="#222",
        font_color="white"
    )
    pos = None

    # STYLE NODES AND HIGHLIGHT CRITICAL PATH
    for node in G.nodes(data=True):
        nid = node[0]
        title = node[1]["title"]
        color = "red" if nid in longest_path else "#97C2FC"
        net.add_node(
            nid,
            label=nid,
            title=title,
            color=color,
            borderWidth=3
        )

    # SHOW ORDER AND DEPENDENCIES
    for edge in G.edges():
        if edge in longest_path_edges:
            net.add_edge(edge[0], edge[1], color="red", width=3)
        else:
            net.add_edge(edge[0], edge[1])

    net.repulsion()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, "r", encoding="utf-8") as f:
            html_content = f.read()
    os.unlink(tmp_file.name)

    html_content = re.sub(
        r'<div id="mynetwork".*?>',
        '<div id="mynetwork" style="width:100vw; height:90vh;">',
        html_content
    )

    return html_content, longest_path
