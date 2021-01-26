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

# ------------ create SQL DB and table --------------
try:
    # create database wiki_search_results
    connection = connect(
        host="localhost",
        user="root",
        # user=input("Enter username: "),
        # password=getpass("Enter password: "),
    )
    create_db = "CREATE DATABASE wiki_search_results"
    with connection.cursor() as cursor:
        cursor.execute(create_db)
        connection.commit()
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
    with connection.cursor() as cursor:
        cursor.execute(create_extract_table_query)
        connection.commit()
except Error as e:
    # drop old table if the exists:
    print(e)
    print("dropping table...")
    drop_table_query = "DROP TABLE wikis"
    with connection.cursor() as cursor:
        cursor.execute(drop_table_query)
        connection.commit()
    # create new empty table:
    create_extract_table_query = """
    CREATE TABLE wikis(
        title VARCHAR(100),
        pageid INT,
        snippet TEXT CHARACTER SET utf8,
        FULLTEXT (snippet)
    ) ENGINE=InnoDB;
    """
    with connection.cursor() as cursor:
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

with connection.cursor() as cursor:
    cursor.executemany(insert_wikis_query, vals)
    connection.commit()
#-----------------

#--------------SQL full text search ----------

text_query = """
SELECT title
FROM wikis
WHERE Match(snippet) Against('array');
"""
with connection.cursor(buffered = True) as cursor:
    cursor.execute(text_query)
    result = cursor.fetchall()
    print(result)
connection.close()