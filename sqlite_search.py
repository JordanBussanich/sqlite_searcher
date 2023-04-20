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
import typing
import sys

from abc import ABC, abstractmethod

# tabulate is an MIT licensed library and can be found here: https://pypi.org/project/tabulate/
from tabulate import tabulate

# This is bad, but I'm doing it anyway
# I could probably do this with some kind of dependency injection -- pass in a "CellSearcher" object which contains the search method
regex = None

class RowSearchResult:
    def __init__(self, search_term: str, result: str, column_names: list[str], table_name: str, row: list) -> None:
        self.search_term = search_term
        self.result = result
        self.column_names = column_names
        self.table_name = table_name
        self.row = row
    
    def __hash__(self) -> int:
        return hash((self.search_term, self.result, ','.join(self.column_names), ','.join(map(str, self.row)), self.table_name))
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, type(self)):
            return NotImplemented
        return self.search_term == __value.search_term and self.result == __value.result and self.column_names == __value.column_names and self.table_name == __value.table_name and self.row == __value.row


class TableSearchResult:
    def __init__(self, search_term: str, result: str) -> None:
        self.search_term = search_term
        self.result = result
    
    def __hash__(self) -> int:
        return hash((self.search_term, self.result))
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, type(self)):
            return NotImplemented
        return self.search_term == __value.search_term and self.result == __value.result


class CellSearcher(ABC):
    @abstractmethod
    def search_cell(self, cell_content: str) -> bool:
        return
    
    def __init__(self, search_term: str, case_sensitive: bool) -> None:
        self.search_term = search_term


class TextCellSearcher(CellSearcher):
    def search_cell(self, cell_content: str) -> bool:
        if self.case_sensitive:
            if self.search_term in cell_content:
                return True
        else:
            if self.search_term.casefold() in str(cell_content).casefold():
                return True
        
        return False

    def __init__(self, search_term: str, case_sensitive: bool) -> None:
        super().__init__(search_term, case_sensitive)
        self.case_sensitive = case_sensitive


class RegexCellSearcher(CellSearcher):
    def search_cell(self, cell_content: str) -> bool:
        return bool(self.regex.match(self.search_term))

    def __init__(self, search_term: str, case_sensitive: bool) -> None:
        super().__init__(search_term, case_sensitive)

        if case_sensitive:
            self.regex = re.compile(search_term)
        else:
            self.regex = re.compile(search_term, re.IGNORECASE)

        self.case_sensitive = case_sensitive


def search_sqlite(searchers: list[CellSearcher], input_file: str) -> typing.Tuple[list[TableSearchResult], list[RowSearchResult]]:
    table_search_results = list[TableSearchResult]()
    row_search_results = list[RowSearchResult]()
    
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

    print(f"Got {len(tables)} tables.")
    
    table_name_matches = set()
    for table in tables:
        for searcher in searchers:
            if searcher.search_cell(table):
                table_name_matches.add(TableSearchResult(searcher.search_term, table))
    

    if len(table_name_matches) > 0:
        table_search_results.extend(table_name_matches)
    

    for table in tables:
        get_table_query = f"""SELECT * FROM {table}"""

        cursor.execute(get_table_query)

        column_names = [description[0] for description in cursor.description]
        
        row_matches = set()

        for row in cursor:
            for col in row:
                for searcher in searchers:
                    if searcher.search_cell(col):
                        row_matches.add(RowSearchResult(searcher.search_term, col, column_names, table, row))
        
        if len(row_matches) > 0:
            row_search_results.extend(row_matches)
    
    print(f"Closing database '{input_file}'.")
    conn.close()

    return (table_search_results, row_search_results)
        

parser = argparse.ArgumentParser(prog='sqlite_searcher',
                                 description='This program searches SQLite files for a string')

parser.add_argument('-i', '--input',
                    help='The input SQLite database.',
                    required=True,
                    dest='input_file')

parser.add_argument('-s', '--search-for',
                    help='The text you want to search for.',
                    dest='search_string')

parser.add_argument('-k', '--keyword-list',
                    help='A text file containing a single search term on each line. Do not use -s with -k.',
                    dest='keyword_list')

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

keywords = list[str]()

if arguments.keyword_list:
    with open(arguments.keyword_list) as f:
        keywords.extend(f.read().splitlines())
else:
    if arguments.search_string:
        keywords.append(arguments.search_string)
    else:
        print('ERROR: No search term or keyword list provided.')
        sys.exit(0)

print('Searching for the following keywords:\n')
print('\n'.join(keywords))
print()

searchers = list[CellSearcher]()
for keyword in keywords:
    if arguments.regex:
        searchers.append(RegexCellSearcher(keyword, arguments.case_sensitive))
    else:
        searchers.append(TextCellSearcher(keyword, arguments.case_sensitive))

results = search_sqlite(searchers, arguments.input_file)

print()

# Table names
if len(results[0]) > 0:
    print("Found the following keywords in the following Table names:")
    table_output = zip([r.search_term for r in results[0]], [r.result for r in results[0]])
    print(tabulate(table_output, ('Keyword', 'Table'), tablefmt='mixed_outline'))
else:
    print('No keywords found in any Table names.')

print()

# Table content
if len(results[1]) > 0:
    for table in set([r.table_name for r in results[1]]):
        table_output_rows = list()
        first = True
        column_headers = ['Search Term', 'Search Result']
        for row in [s for s in results[1] if s.table_name == table]:
            table_output = list()
            table_output.append(row.search_term)
            table_output.append(row.result)
            table_output.extend(row.row)
            table_output_rows.append(table_output)

            if first:
                column_headers.extend(row.column_names)
                first = False
        
        print(f"Keyword matches for '{table}':")
        print(tabulate(table_output_rows, column_headers, tablefmt='mixed_outline'))
        print()
    
else:
    print('No keywords found in any Tables.')