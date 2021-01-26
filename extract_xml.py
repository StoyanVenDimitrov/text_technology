import requests
import psycopg3

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

# ------------ create SQL DB and table --------------
try:
    # create database wiki_search_results
    connection = psycopg2.connect(
        host="localhost",
        user="postgres"
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
        user="postgres",
        database="wiki_search_results",
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    )
    cursor = connection.cursor()
except Error as e:
    print(e)

try:
    create_extract_table_query = """
    CREATE TABLE wikis(
        title VARCHAR(100),
        pageid INT,
        snippet TEXT CHARACTER SET utf8
    )
    """
    cursor.execute(create_extract_table_query)
except Error as e:
    # drop old table if the exists:
    print(e)
    print("dropping table...")
    drop_table_query = "DROP TABLE wikis"
    cursor.execute(drop_table_query)
    # create new empty table:
    create_extract_table_query = """
    CREATE TABLE wikis(
        title VARCHAR(100),
        pageid INT,
        snippet TEXT CHARACTER SET utf8
    )
    """
    cursor.execute(create_extract_table_query)
connection.commit()
# --------------------

#------------- insert xml content in the SQL table --------
# write the xml as string:
tree = ET.parse("data/sample.xml")
root = tree.getroot()
# read the element 'p' (at the xml it's the search results)
# TODO: remove the tags with BeautifulSoup
vals = [(v.attrib["title"], v.attrib["pageid"], v.attrib["snippet"]) for v in root.iter("p")]

insert_wikis_query = """
INSERT INTO wikis
(title, pageid, snippet)
VALUES ( %s, %s, %s )
"""

cursor.executemany(insert_wikis_query, vals)
connection.commit()
#-----------------

#--------------SQL full text search ----------

text_query = """
SELECT title
FROM wikis
WHERE to_tsvector('english', snippet) @@ to_tsquery('english', 'array');
"""
cursor.execute(text_query)

connection.close()