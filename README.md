# SQLite Searcher

This tool searchers SQLite files for a string.

## What works?

This script will search for one or more strings or Regexes in a single SQLite database and produce either a Tabulate table ~or counts of how many instances of the search term exist in each Table~ I broke this.

## What doesn't work?

- ~Searching for more than one keyword~
- ~Searching using Regexes~
- Outputting something that can be consumed by another program/script
- Outputting just the counts of each instance of a keyword

## Dependencies?

This script depends on 'tabulate', pip install it if you don't have it.
