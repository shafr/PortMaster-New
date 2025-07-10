import os, json
from genson import SchemaBuilder
from termcolor import cprint

json_dir = "ports/"

def json_schema_from_file(schema_version: int, output_schema_path: str):
    try:
        builder = SchemaBuilder()
        builder.add_schema({})

        for root, _, files in os.walk(json_dir):
            for filename in files:
                if filename != "port.json":
                    continue

                try:
                    with open(os.path.join(root, filename)) as f:
                        data = json.load(f)

                        if "version" not in data:
                            cprint("Error: 'version' key not found in JSON data.", "red")
                            continue

                        if data["version"] != schema_version:
                            # cprint(f"Warning: Version mismatch in {filename}. Expected {schema_version}, found {data['version']}.", "yellow")
                            continue

                        cprint(f"Adding {root} to schema", "green")
                        builder.add_object(data)
                except Exception as e:
                    cprint(f"Error processing {filename} in {root}: {e}", "red")
                    continue


        schema = builder.to_schema()

        with open(output_schema_path, "w") as schema_file:
            json.dump(schema, schema_file, indent=2)


        print(f"JSON schema successfully generated and saved to '{output_schema_path}'.")
    except IOError as e:
        print(f"I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    json_schema_from_file(
        schema_version=4,
        output_schema_path="schema/v4_schema.json"
    )
