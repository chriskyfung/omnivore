#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: json2csv.py
Author: Chris K.Y. Fung
website: chriskyfung.github.io
Date: 2024-10-04

Description:
    This script reads JSON data from a file, converts it to CSV format with a cumulative length limit for each cell, and saves the CSV data to a file.

Usage:
    python json2csv.py

Requirements:
    - Python 3.x

License:
    AGPL-3.0 License. See LICENSE file for details.
"""

import json
import os
from typing import List, Dict

# Constants
JSON_FILE_PATH = 'nodes-id-url.json'
CSV_FILE_PATH = 'nodes-id-url.csv'
LENGTH_LIMIT = 30000

def read_json_file(file_path: str) -> List[Dict]:
    """Read JSON data from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def convert_to_csv(data: List[Dict], length_limit: int = LENGTH_LIMIT) -> str:
    """Convert JSON data to CSV format with specified length limit."""
    csv_lines = []
    current_line = ""
    current_length = 0

    for node in data:
        node_str = json.dumps(node)
        if current_length + len(node_str) > length_limit:
            csv_lines.append(current_line.replace(' ', '').replace('"', '""'))
            current_line = node_str
            current_length = len(node_str)
        else:
            if current_line:
                current_line += ","
            current_line += node_str
            current_length += len(node_str)

    if current_line:
        csv_lines.append(current_line.replace(' ', '').replace('"', '""'))

    return '"' + '","'.join(csv_lines) + '"'

def save_csv_file(file_path: str, csv_data: str) -> None:
    """Save CSV data to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(csv_data)

def main():
    """Main function to execute the script."""
    try:
        print("🚀 Starting JSON to CSV conversion...")

        # Read JSON data from file
        data = read_json_file(JSON_FILE_PATH)

        # Convert JSON data to CSV format
        csv_data = convert_to_csv(data)

        # Save CSV data to file
        save_csv_file(CSV_FILE_PATH, csv_data)

        print(f"✅ Data successfully saved to {CSV_FILE_PATH}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
