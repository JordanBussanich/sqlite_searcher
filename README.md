# SQLite Searcher

This tool searchers SQLite files for a string.

## What works?

Right now this script will search for a single string in a single SQLite database and produce either a table or counts of how many instances of the search terms exist in each Table.

## What doesn't work?

- Searching for more than one keyword
- Searching using Regexes
- Outputting something that can be consumed by another program/script

## Dependencies?

This script depends on 'tabulate', pip install it if you don't have it.
