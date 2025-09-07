import networkx as nx
from pyvis.network import Network
import tempfile, os, re
import streamlit as st

def render_pert_tasks(tasks: any) -> tuple[str, list, list]:
    """
    GIVEN AN OBJECT OF TASKS, CREATES A PERT GRAPH AND SHOWS
    THE CRITICAL PATH, INCLUDING Inicio Proyecto AND Final del Proyecto NODES.
    """

    # START GRAPH
    G = nx.DiGraph()
    tasks_list = dict()

    for data in tasks['activities']:
        costo_media_pert = (float(data['cost']['optimistic']) + 4*float(data['cost']['most_likely']) + float(data['cost']['pessimistic'])) / 6

        duracion_media_pert = (float(data['duration']['optimistic']) + 4*float(data['duration']['most_likely']) + float(data['duration']['pessimistic'])) / 6

        data['duration']['media_pert'] = duracion_media_pert
        data['cost']['media_pert'] = costo_media_pert

        G.add_node(
            data['id'],
            duracion=data['duration']["media_pert"],
            title=f"Tarea {data['name']}<br>Duración: {data['duration']['media_pert']} días"
        )
        tasks_list[data['id']] = {
            'task': data['name'],
            'BAC': costo_media_pert
        }
        for dep in data.get("dependencies", []):
            G.add_edge(dep, data['id'])

    # START AND END TASKS
    G.add_node("Inicio Proyecto", duracion=0, title="Inicio del proyecto")
    G.add_node("Final del Proyecto", duracion=0, title="Fin del proyecto")

    for node in tasks['activities']:
        if not node.get("dependencies"):
            G.add_edge("Inicio Proyecto", node['id'])

    for node in tasks['activities']:
        node_id = node['id']
        if G.out_degree(node_id) == 0:
            G.add_edge(node_id, "Final del Proyecto")

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

    # TASK NODES
    for node in G.nodes(data=True):
        nid = node[0]
        title = node[1]["title"]
        color = "red" if nid in longest_path else "#97C2FC"
        if nid == "Inicio Proyecto" or nid == "Final del Proyecto":
            color = "red"
        net.add_node(nid, label=nid, title=title, color=color, borderWidth=3)

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

    return html_content, longest_path, tasks_list
