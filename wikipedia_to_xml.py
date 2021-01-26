import os
import requests
import argparse
import xml
from xml.dom import minidom


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

    if not os.path.exists('xml_single_files'):
        os.makedirs('xml_single_files')
    file_name = 'xml_single_files/' + '_'.join(search_term.split()).lower() + '.xml'
    xml = minidom.parseString(R.text)
    xml_pretty_str = xml.toprettyxml()
    with open(file_name, 'w') as f:
        f.write(xml_pretty_str)

    return R.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--term",
        required=True,
        default="matrix",
        help="Search for this term on Wikipedia",
    )

    args = parser.parse_args()
    wikimedia_request(args.term)
