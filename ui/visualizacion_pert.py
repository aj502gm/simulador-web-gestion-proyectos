import networkx as nx
from pyvis.network import Network
import tempfile
import os
import re

MOCK_TASKS = {
    "A": {"duracion": 2, "deps": []},
    "B": {"duracion": 4, "deps": ["A"]},
    "C": {"duracion": 5, "deps": ["B"]},
    "D": {"duracion": 3, "deps": ["B"]},
    "E": {"duracion": 2, "deps": ["C", "D"]},
    "F": {"duracion": 3, "deps": ["E"]},
    "G": {"duracion": 1, "deps": ["F"]},
    "H": {"duracion": 5, "deps": ["D"]}
}

def render_pert_tasks(tasks: dict) -> tuple[str, list]:
    """
   GIVEN AN OBJECT OF TASKS, CREATES A PERT GRAPH AND SHOWS
   THE CRITICAL PATH.
    """
    # START GRAPH
    G = nx.DiGraph()
    # CREATE ALL NODES
    for tarea, data in tasks.items():
        G.add_node(
            tarea,
            duracion=data["duracion"],
            title=f"Tarea {tarea}<br>Duración: {data['duracion']} días"
        )
        for dep in data["deps"]:
            G.add_edge(dep, tarea)

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
