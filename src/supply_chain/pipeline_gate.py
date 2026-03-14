from anomaly_detector import train_model, detect_anomaly

def security_gate():

    model = train_model()

    result = detect_anomaly(model)

    if result:
        print("❌ Build blocked due to supply chain risk")
        exit(1)
    else:
        print("✅ Build allowed")


if __name__ == "__main__":
    security_gate()