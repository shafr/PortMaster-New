import os, json
from genson import SchemaBuilder
from jsonschema import validate, ValidationError
from termcolor import cprint
import re

json_dir = "ports/"

def validate_json_files(schema_version: int, schema_old: str, schema_new: str):
    try:
        # Load the schema
        with open(schema_old) as schema_file:
            schema_old_json = json.load(schema_file)

        with open(schema_new) as schema_file:
            schema_new_json = json.load(schema_file)

        errors_found = False

        for root, _, files in os.walk(json_dir):
            for filename in files:
                if filename != "port.json":
                    continue

                try:
                    with open(os.path.join(root, filename)) as f:
                        data = json.load(f)
                        data_as_text = json.dumps(data, indent=2)

                        if "version" not in data:
                            cprint(f"Error: 'version' key not found in {os.path.join(root, filename)}.", "red")
                            errors_found = True
                            continue

                        if data["version"] != schema_version:
                            # cprint(f"Warning: Version mismatch in {filename}. Expected {schema_version}, found {data['version']}.", "yellow")
                            continue

                        try:
                            if "availability" not in data["attr"]:
                                cprint(f"Error: 'availability' key not found in {os.path.join(root, filename)}.", "red")
                                errors_found = True
                                continue

                            continue

                            # print(data["attr"]["availability"])


                            # Uncomment the following lines if you want to filter out files based on platform keys

                            # if not "steam" in data_as_text or "gog" in data_as_text or "epic" in data_as_text:
                            #    continue

                            # if "purchase" in data_as_text or "buy" in data_as_text:
                            #     cprint(f"Warning: 'purchase' key found in {os.path.join(root, filename)}. This key is deprecated.", "yellow")

                            # print(f"Validating {os.path.join(root, filename)}")

                            # Convert data from schema v2 to v4
                            # Example: migrate "steam" field to new structure if needed
                            # converted_data = data.copy()

                            # # Example conversion: move "steam" to "platforms.steam"
                            # if "steam" in converted_data:
                            #     if "platforms" not in converted_data:
                            #         converted_data["platforms"] = {}
                            #     converted_data["platforms"]["steam"] = converted_data.pop("steam")

                            # # Update version
                            # converted_data["version"] = 4

                            # # Validate against new schema
                            # validate(instance=converted_data, schema=schema_new_json)


                        except ValidationError as ve:
                            cprint(f"Validation error in {os.path.join(root, filename)}: {ve.message}\n", "red")
                            errors_found = True
                except Exception as e:
                    cprint(f"Error processing {filename} in {root}: {e}", "red")
                    errors_found = True
                    continue

        if errors_found:
            print("Some files failed validation.")
        else:
            print("All files validated successfully.")
    except IOError as e:
        print(f"I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    validate_json_files(
        schema_version=4,
        schema_old="schema/v2_schema.json",
        schema_new="schema/v4_schema.json"
    )
