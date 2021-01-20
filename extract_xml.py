import requests

def wikimedia_request(search_term):
    """search for content on wikipedia pages
    Args:
    search_term (string)
    """
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    # SEARCHPAGE = "matrix"

    PARAMS = {
        "action": "query",
        "format": "xml",
        "list": "search",
        "srsearch": search_term,
        "srlimit": 5
    }
    R = S.get(url=URL, params=PARAMS)
    return R.text

print(wikimedia_request('matrix'))