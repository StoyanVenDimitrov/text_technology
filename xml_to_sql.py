import argparse
import mysql.connector
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from bs4 import BeautifulSoup
from mysql.connector import connect, Error, DatabaseError


def create_single_table(file_name):
    """ Create SQL table for this term
    Args:
    file_name (string): path to the table
    """
    # ------------ create SQL DB and table --------------
    search_term = file_name.split('/')[-1].split('.')[0]
    # read the xml file:
    try:
        tree = ET.parse(file_name)
    except Error:
        raise
    try:
        # create database wiki_search_results
        connection = connect(
            host="localhost",
            user="root"
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
        CREATE TABLE {table_name}(
            title VARCHAR(100),
            pageid INT,
            snippet TEXT CHARACTER SET utf8,
            FULLTEXT (snippet)
        ) ENGINE=InnoDB;
        """.format(table_name=search_term)
        with connection.cursor() as cursor:
            cursor.execute(create_extract_table_query)
            connection.commit()
    except Error as e:
        # drop old table if the exists:
        print(e)
        print("dropping table...")
        drop_table_query = "DROP TABLE {table_name}".format(table_name=search_term)
        with connection.cursor() as cursor:
            cursor.execute(drop_table_query)
            connection.commit()
        # create new empty table:
        create_extract_table_query = """
        CREATE TABLE {table_name}(
            title VARCHAR(100),
            pageid INT,
            snippet TEXT CHARACTER SET utf8,
            FULLTEXT (snippet)
        ) ENGINE=InnoDB;
        """.format(table_name=search_term)
        with connection.cursor() as cursor:
            cursor.execute(create_extract_table_query)
            connection.commit()

    #------------- insert xml content in the SQL table --------
    root = tree.getroot()
    # read the element 'p' (at the xml it's the search results)
    vals = list()
    for v in root.iter("p"):
        soup = BeautifulSoup(v.attrib["snippet"])
        plain_text_snippet = soup.get_text()
        vals.append((v.attrib["title"], v.attrib["pageid"], plain_text_snippet))

    insert_wikis_query = """
    INSERT INTO {table_name}
    (title, pageid, snippet)
    VALUES ( %s, %s, %s )
    """.format(table_name=search_term)
    with connection.cursor() as cursor:
        cursor.executemany(insert_wikis_query, vals)
        connection.commit()
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        required=True,
        help="The xml file path.",
    )

    args = parser.parse_args()
    create_single_table(args.file)