import csv

def load_symbol_data(csv_file):
    """
    Loads symbol data from a CSV file into a dictionary.
    """
    symbol_dict = {}
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                symbol_dict[row[0]] = row[1]
    return symbol_dict

def get_symbol_name(symbol, symbol_dict):
    """
    Given a symbol, returns the corresponding name.
    """
    return symbol_dict.get(symbol, "Symbol not found")

# Example usage:
# symbol_dict = load_symbol_data('symbols.csv')
# print(get_symbol_name('AAPL', symbol_dict))
