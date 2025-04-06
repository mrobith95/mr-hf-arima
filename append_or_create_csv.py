import os
import csv

def append_or_create_csv(filename, data, headers):

    file_exists = os.path.isfile(filename)
    updated = False
    rows = []

    # If file exists, read all rows
    if file_exists:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
    
    # If file doesn't exist or is empty, create it with headers and the new row
    if not file_exists or not rows:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerow(data)
        return

    # Assume the first row is the header
    header = rows[0]
    data_rows = rows[1:]
    
    # Check for a row with matching first column
    for i, row in enumerate(data_rows):
        # Ensure the row has at least two columns before comparing
        if len(row) >= 2 and row[0] == data[0]:
            # If the row has a third column, update it; otherwise, add it
            if len(row) >= 3:
                row[2] = data[2]
                row[1] = data[1]
            else:
                row.append(data[2])
            data_rows[i] = row
            updated = True
            break
    
    if updated:
        # Overwrite the file with the updated rows
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data_rows)
    else:
        # No matching row found; append the new row
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)