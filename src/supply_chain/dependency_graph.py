import json
import networkx as nx

def build_graph():

    with open("sbom.json") as f:
        data = json.load(f)

    G = nx.DiGraph()

    for package in data["artifacts"]:
        name = package["name"]
        version = package["version"]

        G.add_node(name, version=version)

    print("Total packages:", len(G.nodes))

    return G

if __name__ == "__main__":
    graph = build_graph()