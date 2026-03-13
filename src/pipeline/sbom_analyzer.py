"""
SBOM Analyzer - Parses Syft JSON output to extract software components.
"""
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class SBOMAnalyzer:
    def __init__(self, sbom_path: str):
        self.sbom_path = sbom_path

    def parse_syft_json(self) -> List[Dict[str, Any]]:
        """Reads the Syft JSON file and extracts the package details."""
        try:
            with open(self.sbom_path, 'r') as f:
                data = json.load(f)
            
            components = []
            # Syft stores packages under the 'artifacts' key
            for item in data.get('artifacts', []):
                component = {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "version": item.get("version"),
                    "type": item.get("type")
                }
                components.append(component)
                
            logger.info(f"Successfully parsed {len(components)} components from SBOM.")
            return components
            
        except FileNotFoundError:
            logger.error(f"SBOM file not found at {self.sbom_path}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from {self.sbom_path}")
            return []