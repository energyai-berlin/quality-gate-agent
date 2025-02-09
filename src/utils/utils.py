import requests
import json
import ast
import re



def update_table(table,data):
    id= data["id"]
    headers = {'Content-Type': 'application/json'}
    url = f"https://quality-gate.onrender.com/api/{table}/{id}/"
    try:
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Request failed:", e)
        return

    try:
        data = response.json()
    except ValueError:
        data = response.text

    print("Status Code:", response.status_code)
    print("Response:", data)


def parse_json_string(json_string):
    json_string = json_string.strip()
    """
    Parse a JSON-formatted string or a Python literal string into a Python dictionary.
    Tries json.loads first; if that fails, replaces 'true'/'false' with Python booleans 
    before using ast.literal_eval.
    """

    with open("json_input.txt", "w") as file:
        file.write(json_string)

    if isinstance(json_string, dict):
        return json_string

    try:
        return json.loads(json_string)
    except json.JSONDecodeError as json_err:
        try:
            corrected = re.sub(r"\btrue\b", "True", json_string)
            corrected = re.sub(r"\bfalse\b", "False", corrected)
            result = ast.literal_eval(corrected)
            if isinstance(result, dict):
                return result
            else:
                print("Parsed result is not a dictionary.")
                return None
        except Exception as ast_err:
            print("JSON parsing failed:", json_err)
            print("Fallback parsing with ast.literal_eval failed:", ast_err)
            return None

# Example usage
if __name__ == '__main__':
    sample = "{\"table_name\":\"line\",\"data\":{\"id\":5,\"net\":\"Default Network\",\"from_bus\":\"Default From Bus\",\"to_bus\":\"\",\"length_km\":10.5,\"std_type\":\"\",\"name\":\"Updated Line Name\",\"index\":0,\"geodata\":[],\"df\":1.0,\"parallel\":1,\"in_service\":true,\"max_loading_percent\":100.0,\"alpha\":0.0,\"temperature_degree_celsius\":20.0}}"
    result = parse_json_string(sample)
    print("Parsed Dictionary:", result)