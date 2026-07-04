# data_utils.py - Data utilities with errors

import os
import sys

def process_data(data):
    # ERROR: variable 'result' not defined
    return result

def load_config():
    # ERROR: undefined variable 'config_file'
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    # ERROR: 'json' not imported
    data = json.loads('{"key": "value"}')
    print(data)

if __name__ == "__main__":
    main()