import subprocess
import json

def generate_sbom():
    print("Generating SBOM...")

    command = "syft dir:. -o json > sbom.json"
    subprocess.run(command, shell=True)

    print("SBOM saved as sbom.json")

if __name__ == "__main__":
    generate_sbom()