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

    def __str__(self):
        return self.table_name + ':' + str(self.table)


loader = DataLoader()
cities = loader.load_csv('Cities.csv')
my_table1 = Table('cities', cities)

# Print the average temperature of all the cities
my_value = my_table1.aggregate(lambda x: sum(x)/len(x), 'temperature')
print(my_value)
print()

# Print all cities in Germany
my_cities = my_table1.filter(lambda x: x['country'] == 'Germany')
cities_list = [[city['city'], city['country']] for city in my_cities.table]
print("All the cities in Germany:")
for city in cities_list:
    print(city)
print()

# Print all cities in Spain with a temperature above 12°C
my_cities = my_table1.filter(lambda x: x['country'] == 'Spain' and float(x['temperature']) > 12.0)
cities_list = [[city['city'], city['country'], city['temperature']] for city in my_cities.table]
print("All the cities in Spain with temperature above 12°C:")
for city in cities_list:
    print(city)
print()

# Count the number of unique countries
my_countries = my_table1.aggregate(lambda x: len(set(x)), 'country')
print("The number of unique countries is:")
print(my_countries)
print()

# Print the average temperature for all the cities in Germany
my_value = my_table1.filter(lambda x: x['country'] == 'Germany').aggregate(lambda x: sum(x)/len(x), 'temperature')
print("The average temperature of all the cities in Germany:")
print(my_value)
print()

# Print the max temperature for all the cities in Italy
my_value = my_table1.filter(lambda x: x['country'] == 'Italy').aggregate(lambda x: max(x), 'temperature')
print("The max temperature of all the cities in Italy:")
print(my_value)
print()