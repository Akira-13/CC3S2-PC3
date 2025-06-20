import json

def prettify_json(json_file, pretty_json):
    with open(json_file, 'r') as f:
        json_data = json.load(f)  

    if pretty_json is None:
        output_file = json_file
    
    with open(pretty_json, 'w') as f:
        json.dump(json_data, f, indent=4)  

if __name__ == "__main__":
    prettify_json("reports/tflint_iac.json", "reports/tflint_iac.json")