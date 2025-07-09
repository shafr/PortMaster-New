import json
import sys
from jsonschema import validate, ValidationError
import os
import pandas as pd

def load_data(file_path):
    with open(file_path) as f:
        return json.load(f)

def get_schema_for_version(version):
    schema_map = {
        1: "schema/v1_schema.json",
        2: "schema/v2_schema.json",
        3: "schema/v3_schema.json",
        4: "schema/v4_schema.json"
    }

    schema_path = schema_map.get(version)
    if not schema_path:
        raise ValueError(f"No schema defined for version {version}")
    
    with open(schema_path) as f:
        return json.load(f)

def main():
    results = []

    ports_dir = "ports"
    for root, dirs, files in os.walk(ports_dir):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                try:
                    data = load_data(json_path)
                except Exception as e:
                    results.append({
                        "file": json_path,
                        "version": None,
                        "status": "error",
                        "message": f"Failed to load JSON: {e}"
                    })
                    continue

                version = data.get("version")
                if version is None:
                    results.append({
                        "file": json_path,
                        "version": None,
                        "status": "error",
                        "message": "Missing 'version' key"
                    })
                    continue

                try:
                    schema = get_schema_for_version(version)
                except ValueError as ve:
                    results.append({
                        "file": json_path,
                        "version": version,
                        "status": "error",
                        "message": str(ve)
                    })
                    continue

                try:
                    validate(instance=data, schema=schema)
                    results.append({
                        "file": json_path,
                        "version": version,
                        "status": "valid",
                        "message": ""
                    })
                except ValidationError as e:
                    results.append({
                        "file": json_path,
                        "version": version,
                        "status": "invalid",
                        "message": e.message
                    })

    df = pd.DataFrame(results)
    df.to_csv("validation_results.csv", index=False)
    print("Validation results saved to validation_results.csv")

if __name__ == "__main__":
    main()