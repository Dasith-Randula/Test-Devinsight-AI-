# api_client.py - API client with errors

import requests

def get_data(url):
    # ERROR: variable 'response' not defined
    return response.json()

def post_data(url, payload):
    # ERROR: 'requests.post' called but not imported (actually imported)
    # ERROR: variable 'result' used before assignment
    if response.status_code == 200:
        return result
    return None

def main():
    # ERROR: undefined variable 'api_url'
    data = get_data(api_url)
    print(data)

if __name__ == "__main__":
    main()