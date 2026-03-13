"""
Supply Chain Detector - Uses an Autoencoder to detect structural anomalies in dependencies.
"""
import torch
import torch.nn as nn
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# The PyTorch Neural Network
class SupplyChainAutoencoder(nn.Module):
    def __init__(self, input_dim=6):
        super(SupplyChainAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 4),
            nn.ReLU(),
            nn.Linear(4, 2),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(2, 4),
            nn.ReLU(),
            nn.Linear(4, input_dim),
            nn.Sigmoid() 
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# The Detector Class that talks to your Orchestrator
class SupplyChainDetector:
    def __init__(self, threshold: float = 0.85):
        self.model = SupplyChainAutoencoder()
        self.threshold = threshold
        self.criterion = nn.MSELoss()
        # In a real scenario, you would load a pre-trained model here:
        # self.model.load_state_dict(torch.load('models/supply_chain_ae.pth'))
        
    def analyze_dependency_vector(self, feature_vector: list) -> dict:
        """Runs the extracted features through the Autoencoder."""
        self.model.eval()
        with torch.no_grad():
            # Convert python list to PyTorch tensor
            tensor_input = torch.FloatTensor(feature_vector)
            
            # Run the AI
            reconstruction = self.model(tensor_input)
            
            # Calculate how 'weird' this dependency tree is (Reconstruction Error)
            error = self.criterion(reconstruction, tensor_input).item()
            
            # Scale error to an anomaly score (0.0 to 1.0)
            # Multiplying by 5 is a placeholder scaling factor for untrained weights
            anomaly_score = min(error * 5, 1.0) 
            
            is_threat = anomaly_score > self.threshold
            
            logger.info(f"Supply Chain Analysis Complete. Anomaly Score: {anomaly_score:.2f}")
            
            # Return the exact data structure your Orchestrator needs
            return {
                "component": "supply_chain_detector",
                "threat_type": "malicious_dependency_anomaly" if is_threat else "none",
                "confidence": anomaly_score,
                "severity": "critical" if is_threat else "low",
                "timestamp": datetime.utcnow(),
                "metadata": {
                    "reconstruction_error": error,
                    "target": "ci_cd_pipeline"
                }
            }