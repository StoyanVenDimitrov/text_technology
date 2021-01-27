import argparse
import mysql.connector
from mysql.connector import connect, Error, DatabaseError


def sql_text_search(term, table):
    try:
        connection = connect(
            host="localhost",
            user="root",
            database="wiki_search_results",
            # user=input("Enter username: "),
            # password=getpass("Enter password: "),
        )
    except Error as e:
        print(e)

    # TODO: search for more than one term
    text_query = """
    SELECT title,
    MATCH(snippet) AGAINST('{term}' IN NATURAL LANGUAGE MODE) 
    FROM {table}
    WHERE MATCH(snippet) AGAINST('{term}' IN NATURAL LANGUAGE MODE);
    """.format(table=table, term=term)
    
    with connection.cursor(buffered = True) as cursor:
        cursor.execute(text_query)
        result = cursor.fetchall()
        print(result)
    connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--term",
        required=True,
        help="What to search for",
    )
    parser.add_argument(
        "--table",
        required=True,
        help="The table where to search",
    )

    args = parser.parse_args()
    sql_text_search(args.term, args.table)