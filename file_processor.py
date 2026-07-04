# file_processor.py - File processing with errors

import os
import json

def read_file(filepath):
    # ERROR: variable 'content' used before assignment
    return content

def write_file(filepath, data):
    # ERROR: variable 'f' undefined (try/except error)
    try:
        f.write(data)
    except:
        pass

def main():
    # ERROR: undefined variable 'filename'
    data = read_file(filename)
    print(data)

if __name__ == "__main__":
    main()