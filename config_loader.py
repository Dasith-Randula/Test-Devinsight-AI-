# config_loader.py - Config loader with errors

import json

def load_config():
    # ERROR: variable 'config' not defined
    return config

def save_config(data):
    # ERROR: variable 'f' not defined
    json.dump(data, f)

def main():
    # ERROR: undefined variable 'config_file'
    config = load_config(config_file)
    print(config)

if __name__ == "__main__":
    main()