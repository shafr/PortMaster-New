import os, json
from genson import SchemaBuilder
from jsonschema import validate, ValidationError
from termcolor import cprint
import re

json_dir = "ports/"

regex_map = {
    "itch": r"https://.*\.itch\.io/[^ \n\"']*",
    "epic": r"https://store\.epicgames\.com/[^ \n\"']*",
    "steam": r"https://store\.steampowered\.com/app/[^ \n\"']*"
}

def extract_store_link(store_regex, inst, inst_md):
    match = re.search(regex_map[store_regex], inst)
    if not match:
        match = re.search(regex_map[store_regex], inst_md)
    return match.group(0) if match else ""

def validate_json_files(path_to_validate, schema_path: str):
    try:
        # Load the schema
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)

        with open(path_to_validate) as f:
            data = json.load(f)
            data_as_text = json.dumps(data, indent=2)


            data["attr"]["min_glibc"] = ""
            runtime = data["attr"]["runtime"]
            data["attr"]["runtime"] = [ runtime ]

            stores = []
            availability =


            if "itch.io" in data["attr"]["inst"] or "itch.io" in data["attr"]["inst_md"]:
                stores.append( {
                    "name": "itch.io",
                    "gameurl": extract_store_link("itch", data["attr"]["inst"], data["attr"]["inst_md"]),
                } )

            if "store.epicgames.com"in data["attr"]["inst"] or "store.epicgames.com" in data["attr"]["inst_md"]:
                stores.append( {
                    "name": "epic",
                    "gameurl": extract_store_link("epic", data["attr"]["inst"], data["attr"]["inst_md"]),
                } )

            if "store.steampowered.com" in data["attr"]["inst"] or "store.steampowered.com" in data["attr"]["inst_md"]:
                stores.append( {
                    "name": "steam",
                    "gameurl": extract_store_link("steam", data["attr"]["inst"], data["attr"]["inst_md"]),
                } )

            data["attr"]["store"] = stores
            try:
                validate(instance=data, schema=schema)
                cprint(f"Validation successful for {path_to_validate}", "green")

                cprint(json.dumps(data, indent=2), "blue")
            except ValidationError as ve:
                cprint(f"Validation error in {path_to_validate}: {ve.message}\n", "red")
    except IOError as e:
        print(f"I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    validate_json_files(
        path_to_validate="ports/celeste/port.json",
        schema_path="schema/v4_schema.json"
    )
