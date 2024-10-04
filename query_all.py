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
import time
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
query Search($after: String, $searchTerms: String!) {
    search(after: $after, first: 100, query: $searchTerms) {
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
                totalCount
            }
        }
    }
}
"""


# Function to make a request to the GraphQL API
def make_request(after_cursor, searchTerms):
    variables = {"after": after_cursor, "searchTerms": searchTerms}
    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json", "Authorization": apikey},
    )
    return response


# Initialize variables
after_cursor = None
has_next_page = True
search_terms = "in:all"
nodes = []
max_length_per_cell = 50000
current_length = 0
cum_length_in_cell = 0
sleep_time_seconds = 100 * 0.05

apikey = get_api_key()

print("Start querying...\n    Progress:")

# Paginate through the results
while has_next_page:
    try:
        # Call the make_request function
        response = make_request(after_cursor, search_terms)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        # If the request was successful, extract the data
        data = response.json().get("data", {}).get("search", {})

        if "edges" in data:
            for edge in data["edges"]:
                nodes.append(edge["node"])
            after_cursor = data["edges"][-1]["cursor"]

        has_next_page = data["pageInfo"]["hasNextPage"]
        total_count = data["pageInfo"]["totalCount"]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    finally:
        print(f"        {after_cursor} of {total_count}")
        # Set an interval between each API call
        time.sleep(sleep_time_seconds)  # Sleep for 3 seconds (adjust as needed)

# Save nodes to a JSON file
with open('nodes-id-url.json', 'w') as file:
    file.write('[\n')
    for i, node in enumerate(nodes):
        file.write(json.dumps(node))
        if i < len(nodes) - 1:
            file.write(',\n')
    file.write('\n]\n')

print("Saved to nodes-id-url.json")
