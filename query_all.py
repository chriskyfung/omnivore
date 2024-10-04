#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: query_all.py
Author: Chris K.Y. Fung
website: chriskyfung.github.io
Date: 2024-10-04

Description:
    This script performs the following tasks:
    1. Initializes pagination with `after_cursor` set to `None`.
    2. Makes requests to a GraphQL API, paginating through the results until there are no more pages.
    3. Extracts each `node` from the response and saves them to a JSON file named `nodes-id-url.json`.
    4. Validates the API key format and retrieves it from command line arguments or environment variables.

Usage:
    python query_all.py --apikey YOUR_API_KEY

Requirements:
    - Python 3.x
    - requests library

License:
    AGPL-3.0 License. See LICENSE file for details.
"""

import os
import re
import argparse
import requests
import json

# Define the GraphQL endpoint
url = "https://api-prod.omnivore.app/api/graphql"


def has_valid_api_key_format(api_key):
    # Regular expression pattern for the API key format
    apikey_pattern = re.compile(
        r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
    )

    if not apikey_pattern.match(api_key):
        print("Invalid API key format. Please provide a valid key.")
        return False

    return True


def get_api_key():
    # Check if it's provided as a command line argument
    parser = argparse.ArgumentParser(description="Process API key.")
    parser.add_argument("--apikey", type=str, help="API key for Omnivore")
    args = parser.parse_args()

    # Check if the API key matches the required format
    # If not set, check if the API key is set as an environment variable
    api_key = args.apikey or os.getenv("OMNIVORE_API_KEY")

    if api_key and has_valid_api_key_format(api_key):
        return api_key

    # If neither is provided, prompt the user to enter it
    while True:
        api_key = input("Please enter your Omnivore API key: ")
        # Check if the API key matches the required format
        if has_valid_api_key_format(api_key):
            break

    return api_key


# Define the GraphQL query
query = """
query Search($after: String) {
    search(after: $after, first: 100, query: "in:all") {
        ... on SearchError {
            errorCodes
        }
        ... on SearchSuccess {
            edges {
                cursor
                node {
                    url
                    id
                }
            }
            pageInfo {
                hasNextPage
            }
        }
    }
}
"""

# Function to make a request to the GraphQL API
def make_request(after_cursor):
    variables = {"after": after_cursor}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers={'Content-Type':'application/json','Authorization': apikey})
    return response.json()

# Initialize variables
after_cursor = None
has_next_page = True
nodes = []
max_length_per_cell = 50000
current_length = 0
cum_length_in_cell = 0

apikey = get_api_key()

print("Start querying...")

# Paginate through the results
while has_next_page:
    result = make_request(after_cursor)
    data = result.get('data', {}).get('search', {})
    
    if 'edges' in data:
        for edge in data['edges']:
            nodes.append(edge['node'])
        after_cursor = data['edges'][-1]['cursor']
        has_next_page = data['pageInfo']['hasNextPage']
    else:
        has_next_page = False

# Save nodes to a JSON file
with open('nodes-id-url.json', 'w') as file:
    file.write('[\n')
    for i, node in enumerate(nodes):
        file.write(json.dumps(node))
        if i < len(nodes) - 1:
            file.write(',\n')
    file.write('\n]\n')

print("Saved to nodes-id-url.json")
