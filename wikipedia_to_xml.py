import os
import requests
import argparse
import xml
from lxml import etree


def wikimedia_request(search_term, search_limit):
    """search for content on wikipedia pages
    Args:
    search_term (string)
    """
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "xml",
        "list": "search",
        "srsearch": search_term,
        "srlimit": search_limit
    }
    R = S.get(url=URL, params=PARAMS)

    if not os.path.exists('xml_single_files'):
        os.makedirs('xml_single_files')
    file_name = 'xml_single_files/' + '_'.join(search_term.split()).lower() + '.xml'
    r = etree.XML(R.content)
    with open("data/api.dtd") as f:
        dtd = etree.DTD(f)
    if dtd.validate(r) is True:
        root = etree.XML(R.text)
        with open(file_name, 'wb') as f:
            f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--term",
        required=True,
        default="matrix",
        help="Search for this term on Wikipedia",
    )
    parser.add_argument(
        "--search_limit",
        required=False,
        default=5,
        help="Number of results from the wikipedia search",
    )

    args = parser.parse_args()
    wikimedia_request(args.term, args.search_limit)
