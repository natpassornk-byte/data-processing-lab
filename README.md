# OOP Data Processing Lab

## Lab Overview
In this lab, I changed the code from the previous lab, which used functions, into OOP style using classes.
The program reads data about cities from `Cities.csv`. Then it can filter the data and calculate things
like the average temperature, the maximum temperature, and the number of different countries.

## Project Structure
- `README.md`: This file
- `Cities.csv`: The dataset
- `data_processing.py`: The code

All of them are in the folder data-processing-lab.

## Design

### `DataLoader`
- This class is used to load a csv file.
- Attribute: base_path is the folder that has the csv file. If we do not give it a path, it uses the folder where data_processing.py is.
- Method: load_csv(filename) reads the csv file and returns a list of dictionaries. Each dictionary is one row.

### `Table`
- This class stores the data of one table.
- Attributes:
  - table_name is the name of the table.
  - table is a list of dictionaries (the rows).
- Methods:
  - filter(condition) returns a new Table that has only the rows that match the condition. The name of the new table is the old name plus _filtered.
  - aggregate(aggregation_function, aggregation_key) takes the values in one column and uses the given function on them, for example max or a function to find the average.
  - __str__() is used when we print the table.

## How to Test and Run

1. Put `data_processing.py` and `Cities.csv` in the same folder.
2. Run this command in the terminal: python data_processing.py
3. The test code at the bottom of the file will print:
   - the average temperature of all cities
   - all cities in Germany
   - cities in Spain with temperature above 12°C
   - the number of unique countries
   - the average temperature in Germany
   - the maximum temperature in Italy