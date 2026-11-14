import csv, os
from pathlib import Path


class DataLoader:
    """Handles loading CSV data files."""

    def __init__(self, base_path=None):
        """Initialize the DataLoader with a base path for data files.
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.resolve()
        else:
            self.base_path = Path(base_path)

    def load_csv(self, filename):
        """Load a CSV file and return its contents as a list of dictionaries.
        """
        filepath = self.base_path / filename
        data = []

        with filepath.open() as f:
            rows = csv.DictReader(f)
            for row in rows:
                data.append(dict(row))

        return data


class DB:
    """A very simple database: a list of tables."""

    def __init__(self):
        """Create an empty database."""
        self.database = []

    def insert(self, table):
        """Add a Table to the database."""
        self.database.append(table)

    def search(self, table_name):
        """Return the Table whose name is table_name, or None if not found."""
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


class Table:
    """A table with a name and a list of rows (each row is a dictionary)."""

    def __init__(self, table_name, table):
        """Create a table.

        Args:
            table_name: Name of the table, e.g. 'cities'.
            table: A list of dictionaries, one dictionary per row.
        """
        self.table_name = table_name
        self.table = table

    def filter(self, condition):
        """Return a new Table that keeps only the rows where condition(row) is True.

        Args:
            condition: A function that takes a row (dictionary) and returns True/False.
        """
        filtered_table = []
        for item in self.table:
            if condition(item):
                filtered_table.append(item)
        return Table(self.table_name + '_filtered', filtered_table)

    def aggregate(self, aggregation_function, aggregation_key):
        """Apply aggregation_function to all the values in one column.

        Values that look like numbers are converted to float; other values
        (e.g. country names) are kept as text.

        Args:
            aggregation_function: A function that takes a list, e.g. max, min, len.
            aggregation_key: The column (dictionary key) to aggregate.
        """
        values = []
        for item in self.table:
            try:
                values.append(float(item[aggregation_key]))
            except ValueError:
                values.append(item[aggregation_key])
        return aggregation_function(values)

    def join(self, other_table, common_key):
        """Join this table with another table on a common key.

        For every pair of rows (one from each table) that have the same value
        for common_key, the two rows are merged into one dictionary.

        Args:
            other_table: The Table to join with.
            common_key: The column that both tables share, e.g. 'country'.

        Returns:
            A new Table containing the merged rows.
        """
        joined_table = []
        for row1 in self.table:
            for row2 in other_table.table:
                if row1[common_key] == row2[common_key]:
                    joined_table.append({**row1, **row2})
        return Table(self.table_name + '_joined_' + other_table.table_name, joined_table)

    def __str__(self):
        return self.table_name + ':' + str(self.table)


loader = DataLoader()
cities = loader.load_csv('Cities.csv')
table1 = Table('cities', cities)
countries = loader.load_csv('Countries.csv')
table2 = Table('countries', countries)

my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)

my_table1 = my_DB.search('cities')
print("List all cities in Italy:")
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Average temperature for all cities in Italy:")
print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
print()

my_table2 = my_DB.search('countries')
print("List all non-EU countries:")
my_table2_filtered = my_table2.filter(lambda x: x['EU'] == 'no')
print(my_table2_filtered)
print()

print("Number of countries that have coastline:")
print(my_table2.filter(lambda x: x['coastline'] == 'yes').aggregate(lambda x: len(x), 'coastline'))
print()

my_table3 = my_table1.join(my_table2, 'country')
print("First 5 entries of the joined table (cities and countries):")
for item in my_table3.table[:5]:
    print(item)
print()

print("Cities whose temperatures are below 5.0 in non-EU countries:")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()

print("The min and max temperatures for cities in EU countries that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()