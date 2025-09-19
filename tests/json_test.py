import os
import json
import pytest

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("filename", ["./sv.json", "./en.json"])
def test_json_format(filename):
    try:
        load_json(filename)
    except json.JSONDecodeError as e:
        pytest.fail(f"JSONDecodeError in {filename}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error reading {filename}: {e}")

def check_translation_keys(sv_data, en_data, path=""):
    sv_keys = set(sv_data.keys())
    en_keys = set(en_data.keys())
    for key in sv_keys - en_keys:
        yield f"Key '{path + key}' present in sv.json but missing in en.json"
    for key in en_keys - sv_keys:
        yield f"Key '{path + key}' present in en.json but missing in sv.json"
    for key in sv_keys & en_keys:
        if isinstance(sv_data[key], dict) and isinstance(en_data[key], dict):
            yield from check_translation_keys(sv_data[key], en_data[key], path + key + ".")

def test_matching_translation_keys():
    sv_data = load_json("./sv.json")
    en_data = load_json("./en.json")

    errors = list(check_translation_keys(sv_data, en_data))
    if errors:
        pytest.fail("\n".join(errors))
