import sqlite3
import argparse

from tabulate import tabulate

# SQLite Search
# Hacked together by Jordan Bussanich

def search_sqlite(input_file: str, search_text: str, case_sensitive: bool = False, show_details: bool = False) -> None:
    print(f"Opening database '{input_file}' in read-only mode.")

    conn = sqlite3.connect(rf"{input_file}")

    get_tables_query = """SELECT name 
                          FROM sqlite_master 
                          WHERE type='table' AND name NOT LIKE 'sqlite%'"""     # Exclude sqlite system tables

    cursor = conn.cursor()

    # Ensure the database is read-only
    cursor.execute("PRAGMA query_only = ON")

    cursor.execute(get_tables_query)

    tables_raw = cursor.fetchall()

    tables = [table[0] for table in tables_raw]

    print(f"Got {len(tables)} tables.\n")


    # There's probably a more elegant way to do this
    table_name_matches = []
    for table in tables:
        if case_sensitive:
            if search_text in table:
                table_name_matches.append(table)
        else:
            if search_text.casefold() in table.casefold():
                table_name_matches.append(table)

    if len(table_name_matches) > 0:
        print(f"Found '{search_text}' in the following Table names:\n")
        for match in table_name_matches:
            print(match)
    else:
        print(f"Did not find '{search_text}' in any Table names.\n")

    for table in tables:
        get_table_query = f"""SELECT * FROM {table}"""

        cursor.execute(get_table_query)

        column_names = [description[0] for description in cursor.description]
        
        row_matches = []

        for row in cursor:
            for col in row:
                if case_sensitive:
                    if search_text in str(col):
                        row_matches.append(row)
                else:
                    if search_text.casefold() in str(col).casefold():
                        row_matches.append(row)
        
        if len(row_matches) > 0:
            if not show_details:
                print(f"Found {str(len(row_matches))} instances of '{search_text}' in '{table}'")
            else:
                print(f"Found '{search_text}' in the following rows in '{table}'.\n")
                print(tabulate(row_matches, headers=column_names, tablefmt='orgtbl'))
                print()
        else:
            print(f"Did not find '{search_text}' in '{table}'.")
    
    conn.close()
        

parser = argparse.ArgumentParser(prog='sqlite_searcher',
                                 description='This program searches SQLite files for a string')

parser.add_argument('-i', '--input',
                    help='The input SQLite database.',
                    required=True,
                    dest='input_file')

parser.add_argument('-s', '--search-for',
                    help='The text you want to search for.',
                    required=True,
                    dest='search_string')

parser.add_argument('-c', '--case-sensitive',
                    action='store_true',
                    help='Search for a case-sensitive string.')

parser.add_argument('-d', '--show-details',
                    action='store_true',
                    help='Show each row that contains the search text, rather than just the counts.')

arguments = parser.parse_args()
search_sqlite(arguments.input_file, arguments.search_string, arguments.case_sensitive, arguments.show_details)
