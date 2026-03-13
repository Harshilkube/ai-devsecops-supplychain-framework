"""
Graph Builder - Constructs a dependency graph from SBOM components and extracts AI features.
"""
import networkx as nx
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SBOMGraphBuilder:
    def __init__(self, components: list):
        self.components = components
        self.graph = nx.DiGraph()

    def build_graph(self) -> nx.DiGraph:
        """Builds a directed graph of dependencies."""
        for comp in self.components:
            # Add nodes for each component
            self.graph.add_node(comp['id'], name=comp['name'], version=comp['version'])
            
        # Note: In a full implementation, you would parse the 'relationships' block
        # from the Syft JSON to add edges between nodes. For the thesis baseline,
        # we treat them as standalone nodes if relationships are missing.
        logger.info(f"Built dependency graph with {self.graph.number_of_nodes()} nodes.")
        return self.graph

    def extract_features(self) -> np.ndarray:
        """
        Extracts the 6-value feature vector for the Autoencoder:
        [dependency_count, avg_depth, version_delta, license_risk, maintainer_change, new_dep_ratio]
        """
        dependency_count = self.graph.number_of_nodes()
        
        # Calculate average depth (fallback to 1.0 if no edges exist yet)
        try:
            root_nodes = [n for n, d in self.graph.in_degree() if d == 0]
            if root_nodes and self.graph.number_of_edges() > 0:
                paths = nx.shortest_path_length(self.graph, source=root_nodes[0])
                avg_depth = sum(paths.values()) / len(paths)
            else:
                avg_depth = 1.0
        except Exception:
            avg_depth = 1.0

        # These are calculated placeholders for your thesis. 
        # As you gather dataset metrics, you will populate these dynamically.
        version_delta = 0.0          # e.g., jump from v1 to v5
        license_risk_score = 0.5     # e.g., 0.0 for MIT, 1.0 for unknown
        maintainer_change_flag = 0.0 # 1.0 if maintainer changed
        new_dependency_ratio = 0.1   # percentage of entirely new packages

        features = [
            float(dependency_count),
            float(avg_depth),
            float(version_delta),
            float(license_risk_score),
            float(maintainer_change_flag),
            float(new_dependency_ratio)
        ]
        
        return np.array(features)