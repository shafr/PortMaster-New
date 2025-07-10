import os, json
from genson import SchemaBuilder
from jsonschema import validate, ValidationError
from termcolor import cprint

json_dir = "ports/"

allowed_genres = [
                                    "action",
                                    "adventure",
                                    "arcade",
                                    "card",
                                    "casino/card",
                                    "fps",
                                    "platformer",
                                    "puzzle",
                                    "racing",
                                    "rhythm",
                                    "rpg",
                                    "simulation",
                                    "sports",
                                    "shump",
                                    "strategy",
                                    "visual novel",
                                    "other"
                                ]

def validate_json_files(schema_version: int, schema_path: str):
    try:
        # Load the schema
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)

        errors_found = False

        for root, _, files in os.walk(json_dir):
            for filename in files:
                if filename != "port.json":
                    continue

                try:
                    with open(os.path.join(root, filename)) as f:
                        data = json.load(f)

                        if "version" not in data:
                            cprint(f"Error: 'version' key not found in {os.path.join(root, filename)}.", "red")
                            errors_found = True
                            continue

                        # if data["version"] != schema_version:
                        #     # cprint(f"Warning: Version mismatch in {filename}. Expected {schema_version}, found {data['version']}.", "yellow")
                        #     continue

                        try:
                            genre_value = data["attr"]["genres"]
                            if isinstance(genre_value, list):
                                invalid_genres = [g for g in genre_value if g not in allowed_genres]
                                if invalid_genres:
                                    cprint(f"Invalid genre(s) in {os.path.join(root, filename)}: {invalid_genres}", "red")
                                    errors_found = True
                            else:
                                if genre_value not in allowed_genres:
                                    cprint(f"Invalid genre '{genre_value}' in {os.path.join(root, filename)}", "red")
                                    errors_found = True

                            # validate(instance=data, schema=schema)
                            # cprint(f"{os.path.join(root, filename)} is valid.", "green")
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
        schema_path="schema/v4_schema.json"
    )
