from asyncio import tasks
import networkx as nx
from pyvis.network import Network
import tempfile, os, re
import streamlit as st
import math


def render_pert_tasks(tasks: any) -> tuple[str, list, list]:
    """
    GIVEN AN OBJECT OF TASKS, CREATES A PERT GRAPH AND SHOWS
    THE CRITICAL PATH, INCLUDING Inicio Proyecto AND Final del Proyecto NODES.
    """

    # START GRAPH
    G = nx.DiGraph()
    tasks_list = dict()

    for data in tasks["activities"]:
        costo_media_pert = (
            float(data["cost"]["optimistic"])
            + 4 * float(data["cost"]["most_likely"])
            + float(data["cost"]["pessimistic"])
        ) / 6

        duracion_media_pert = math.ceil(
            (
                float(data["duration"]["optimistic"])
                + 4 * float(data["duration"]["most_likely"])
                + float(data["duration"]["pessimistic"])
            )
            / 6
        )

        data["duration"]["media_pert"] = duracion_media_pert
        data["cost"]["media_pert"] = costo_media_pert

        G.add_node(
            data["id"],
            duracion=data["duration"]["media_pert"],
            title=f"Tarea {data['name']}<br>Duración: {data['duration']['media_pert']}",
        )
        tasks_list[data["id"]] = {
            "task": data["name"],
            "BAC": costo_media_pert,
            "duration": duracion_media_pert,
        }
        for dep in data.get("dependencies", []):
            G.add_edge(dep, data["id"])

    # START AND END TASKS
    G.add_node("Inicio del Proyecto", duracion=0, title="Inicio del proyecto")
    G.add_node("Final del Proyecto", duracion=0, title="Fin del proyecto")

    for node in tasks["activities"]:
        if not node.get("dependencies"):
            G.add_edge("Inicio del Proyecto", node["id"])

    for node in tasks["activities"]:
        node_id = node["id"]
        if G.out_degree(node_id) == 0:
            G.add_edge(node_id, "Final del Proyecto")

    # CRITICAL PATH
    paths = list(nx.all_simple_paths(G, "Inicio del Proyecto", "Final del Proyecto"))
    path_lengths = []
    for path in paths:
        length = sum(G.nodes[node]["duracion"] for node in path)
        path_lengths.append((path, length))

    longest_path = max(path_lengths, key=lambda x: x[1])[0]
    longest_path_edges = list(zip(longest_path, longest_path[1:]))

    net = Network(
        directed=True, height="300px", width="100%", bgcolor="#222", font_color="white"
    )

    net.set_options(
        """{
        "physics": {
            "enabled": true,
            "hierarchicalRepulsion": {
                "centralGravity": 0.0,
                "springLength": 100,
                "springConstant": 0.01,
                "nodeDistance": 120
            },
            "solver": "hierarchicalRepulsion"
        },
        "layout": {
            "hierarchical": {
                "enabled": true,
                "direction": "LR",
                "sortMethod": "directed",
                "levelSeparation": 200
            }
        }
    }"""
    )

    # TASK NODES
    for node in G.nodes(data=True):
        nid = node[0]
        title = node[1].get("title", nid)
        duration = node[1].get("duracion")  # Remove default 0

        if nid in longest_path:
            color = "#FF0000"  # Pure red
        else:
            color = "#97C2FC"  # Original blue

        # Only show duration if it exists
        label = (
            nid if duration is None else f"{nid}\n{duration if duration != 0 else ''}"
        )

        # Configure node shape and text alignment
        net.add_node(
            nid,
            label=label,
            title=title,
            color=color,
            borderWidth=3,
            physics=True,
            shape="box",
            font={"align": "center"},
            margin=10,
        )

    # SHOW ORDER AND DEPENDENCIES
    for edge in G.edges():
        if edge in longest_path_edges:
            net.add_edge(edge[0], edge[1], color="red", width=3, smooth=False)
        else:
            net.add_edge(edge[0], edge[1], color="#97C2FC", smooth=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        with open(tmp_file.name, "r", encoding="utf-8") as f:
            html_content = f.read()
    os.unlink(tmp_file.name)

    html_content = re.sub(
        r'<div id="mynetwork".*?>',
        '<div id="mynetwork" style="width:100vw; height:90vh;">',
        html_content,
    )

    return html_content, longest_path, tasks_list
