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
from typing import Optional, List, Dict

# Constants
GRAPHQL_ENDPOINT = "https://api-prod.omnivore.app/api/graphql"
QUERY = """
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
SLEEP_TIME_SECONDS = 5

def check_api_key_format(api_key: str) -> bool:
    """Validate the API key format."""
    apikey_pattern = re.compile(
        r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$"
    )
    if not apikey_pattern.match(api_key):
        print("❌ Error: Invalid API key format. Please provide a valid key.")
        return False
    return True

def get_api_key() -> str:
    """Retrieve the API key from command line arguments or environment variables."""
    parser = argparse.ArgumentParser(description="Process API key.")
    parser.add_argument("--apikey", type=str, help="API key for Omnivore")
    args = parser.parse_args()

    api_key = args.apikey or os.getenv("OMNIVORE_API_KEY")
    if api_key and check_api_key_format(api_key):
        return api_key

    while True:
        api_key = input("🔑 Please enter your Omnivore API key: ")
        if check_api_key_format(api_key):
            return api_key
        

# Function to make a request to the GraphQL API
def make_request(api_key: str, after_cursor: Optional[str], search_terms: str) -> requests.Response:
    """Make a request to the GraphQL API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    variables = {"after": after_cursor, "searchTerms": search_terms}
    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": QUERY, "variables": variables},
        headers=headers
    )
    response.raise_for_status()
    return response


def fetch_data(api_key: str, search_terms: str = "in:all") -> List[Dict]:
    """Fetch data from the API and return a list of nodes."""
    after_cursor = None
    nodes = []
    has_next_page = True

    while has_next_page:
        try:
            response = make_request(api_key, after_cursor, search_terms)
            data = response.json().get("data", {}).get("search", {})

            if "edges" in data:
                nodes.extend(edge["node"] for edge in data["edges"])
                after_cursor = data["edges"][-1]["cursor"]

            has_next_page = data["pageInfo"]["hasNextPage"]
            total_count = data["pageInfo"]["totalCount"]
            progress_percentage = (len(nodes) / total_count) * 100 if total_count else 0
            print(f"\r    Progress: Fetched {progress_percentage:.2f}% ({len(nodes)} of {total_count})", end='', flush=True)

        except requests.exceptions.RequestException as e:
            print(f"❌ Request error occurred: {e}")
            break
        except Exception as e:
            print(f"⚠️ An unexpected error occurred: {e}")
            break
        finally:
            time.sleep(SLEEP_TIME_SECONDS)

    return nodes

def save_to_file(nodes: List[Dict], filename: str = "nodes-id-url.json") -> None:
    """Save nodes to a JSON file."""
    with open(filename, "w") as file:
        json.dump(nodes, file, indent=4)
    print("\n✅ Data successfully saved to nodes-id-url.json")

def main():
    """Main function to execute the script."""
    api_key = get_api_key()
    print("🔍 Initiating data query...")
    nodes = fetch_data(api_key)
    save_to_file(nodes)

if __name__ == "__main__":
    main()
