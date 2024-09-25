# This script includes the following steps:#
# 1. Read JSON data from the file.
# 2. Convert JSON data to CSV format with a cumulative length limit of 50,000 characters before each cell.
# 3. Save the CSV data to a file.

import json

# Function to read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to convert JSON data to TSV format with specified length limit
def convert_to_csv(data, length_limit=30000):
    csv_lines = []
    current_line = ""
    current_length = 0

    for node in data:
        node_str = json.dumps(node)
        if current_length + len(node_str) > length_limit:
            csv_lines.append(current_line.replace(' ','').replace('"', '""'))
            current_line = node_str
            current_length = len(node_str)
        else:
            if current_line:
                current_line += ","
            current_line += node_str
            current_length += len(node_str)

    if current_line:
        csv_lines.append(current_line.replace(' ','').replace('"', '""'))

    return '"' + '","'.join(csv_lines) + '"'

# Function to save TSV data to a file
def save_csv_file(file_path, csv_data):
    with open(file_path, 'w') as file:
        file.write(csv_data)

# Main function
def main():
    json_file_path = 'nodes-id-url.json'
    csv_file_path = 'nodes-id-url.csv'

    # Read JSON data from file
    data = read_json_file(json_file_path)

    # Convert JSON data to TSV format
    csv_data = convert_to_csv(data)

    # Save TSV data to file
    save_csv_file(csv_file_path, csv_data)

    print(f"TSV data has been saved to {csv_file_path}")

if __name__ == "__main__":
    main()
