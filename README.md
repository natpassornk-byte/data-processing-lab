# OOP Data Processing Lab

## Lab Overview

In this lab, we use OOP in Python to work with data about European cities and countries.
In Commit 3, we changed the code from functions into classes (`DataLoader` and `Table`).
In Commit 4, we added a `DB` class that keeps many tables, and we added a `join` method
so that two tables can be combined using a common key (for example `country`).
This lets us use data from `Cities.csv` and `Countries.csv` together.

## Project Structure

data-processing-lab/
├── README.md             # This file
├── Cities.csv            # City data (city, country, latitude, longitude, temperature)
├── Countries.csv         # Country data (country, population, EU, coastline)
└── data_processing.py    # The code

## Design Overview

DataLoader
- Loads a csv file.
- Attribute: `base_path` is the folder of the csv file.
- Method: `load_csv(filename)` returns a list of dictionaries (one dictionary = one row).

Table
- Stores the data of one table.
- Attributes: `table_name` is the table name, `table` is a list of dictionaries (the rows).
- Methods:
  - `filter(condition)` returns a new Table with only the rows that match the condition.
  - `aggregate(aggregation_function, aggregation_key)` uses the function on all values in one column (e.g. `max`).
  - `join(other_table, common_key)` joins this table with another table. Rows that have the same value
    in the common key are merged into one row. It returns a new Table.
  - `__str__()` is used for printing the table.

DB
- A simple database that stores a list of tables.
- Attribute: `database` is a list of Table objects.
- Methods:
  - `insert(table)` adds a table to the database.
  - `search(table_name)` returns the table with that name, or `None` if there is no such table.

## How to Test and Run

1. Put `data_processing.py`, `Cities.csv` and `Countries.csv` in the same folder.
2. Run this command in the terminal:


python data_processing.py


3. The test code at the bottom of the file loads both csv files, puts the tables in a `DB`, and then prints
the cities in Italy and their average temperature, the non-EU countries, the number of countries with a coastline,
the first 5 rows of the joined table, the cities below 5.0°C in non-EU countries, and the min and max temperature
of cities in EU countries without a coastline. The output should match the expected result from the lab.

name:Natpassorn Kantacheerawat id:6910546369