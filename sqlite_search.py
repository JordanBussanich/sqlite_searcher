# SQLite Search
# Hacked together by Jordan Bussanich

# Copyright (C) 2023  Jordan Bussanich

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sqlite3
import argparse
import re

# tabulate is an MIT licensed library and can be found here: https://pypi.org/project/tabulate/
from tabulate import tabulate

# This is bad, but I'm doing it anyway
# I could probably do this with some kind of dependency injection -- pass in a "CellSearcher" object which contains the search method
regex = None

def search_sqlite(input_file: str, 
                  search_text: str, 
                  case_sensitive: bool = False, 
                  show_details: bool = False,
                  regex_search: bool = False) -> None:
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

    if regex_search:
        regex = re.compile(search_text)
    
    # There's probably a more elegant way to do this
    table_name_matches = []
    for table in tables:
        matched = False

        if regex_search and regex != None:
            if regex.search(table):
                matched = True
        else:
            if case_sensitive:
                if search_text in table:
                    matched = True
            else:
                if search_text.casefold() in table.casefold():
                    matched = True

        if matched:
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
            matched = False
            for col in row:
                if regex_search and regex != None:
                    if regex.search(col):
                        matched = True
                else:
                    if case_sensitive:
                        if search_text in str(col):
                            matched = True
                    else:
                        if search_text.casefold() in str(col).casefold():
                            matched = True
                
                if matched:
                    row_matches.append(row)
                    break
        
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
                    dest='search_string')

# This is disabled since I hacked in Regex support. When that gets fixed I'll enable this.
# parser.add_argument('-k', '--keyword-list',
#                     help='A text file containing a single search term on each line. Do not use -s with -k.',
#                     dest='keyword_list')

parser.add_argument( '--regex',
                    action='store_true',
                    help='Search using Regexs.')

# This is disabled until it's implemented. A cool way to do that would be to build an "Outputter" class
# parser.add_argument('--csv',
#                     action='store_true',
#                     help='Output a CSV of each result, with the Table name in the leftmost column. This script does not write the CSV to the disk, only to STDOUT')

parser.add_argument('--case-sensitive',
                    action='store_true',
                    help='Search for a case-sensitive string. Do not use this with --regex.')

parser.add_argument('--show-details',
                    action='store_true',
                    help='Show each row that contains the search text, rather than just the counts.')

arguments = parser.parse_args()
search_sqlite(arguments.input_file, arguments.search_string, arguments.case_sensitive, arguments.show_details)
