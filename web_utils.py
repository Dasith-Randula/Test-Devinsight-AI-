# web_utils.py - Web utilities with errors

import requests  # Unused import

def fetch_data(url):
    # ERROR: variable 'response' used before assignment
    return response.json()

def parse_html(html):
    # ERROR: 'BeautifulSoup' not imported
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title

def main():
    # ERROR: 'url' undefined
    print(fetch_data(url))

if __name__ == "__main__":
    main()