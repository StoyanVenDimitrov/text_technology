import requests
import mysql.connector
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from mysql.connector import connect, Error, DatabaseError


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

# print(wikimedia_request('matrix'))

try:
    # create database wiki_search_results
    connection = connect(
        host="localhost",
        user="root",
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    )
    create_db = "CREATE DATABASE wiki_search_results"
    cursor = connection.cursor()
    cursor.execute(create_db)
except DatabaseError as e:
    print(e)
    # connect if wiki_search_results exists already
    connection = connect(
        host="localhost",
        user="root",
        database="wiki_search_results",
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    )
    cursor = connection.cursor()
except Error as e:
    print(e)

# write the xml as string:
tree = ET.parse("data/sample.xml")
root = tree.getroot()
# read the element 'p' (at the xml it's the search results)
for search in root.iter("p"):
    print(search.attrib.keys())



connection.close()