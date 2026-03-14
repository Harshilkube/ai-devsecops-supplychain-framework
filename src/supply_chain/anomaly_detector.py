import numpy as np
from sklearn.ensemble import IsolationForest

def train_model():

    # fake training data
    normal_data = np.random.rand(100, 5)

    model = IsolationForest(contamination=0.05)
    model.fit(normal_data)

    return model


def detect_anomaly(model):

    new_data = np.random.rand(1, 5)

    prediction = model.predict(new_data)

    if prediction == -1:
        print("⚠️ Suspicious dependency detected!")
        return True
    else:
        print("Dependencies look safe")
        return False


if __name__ == "__main__":

    model = train_model()

    detect_anomaly(model)