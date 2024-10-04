# This script will:
# 1. Initialize the pagination with `after_cursor` set to `None`.
# 2. Make requests to the GraphQL API, paginating through the results until there are no more pages.
# 3. Extract each `node` and save it as a new line in a `nodes.txt` file.

import os
import argparse
import requests
import json

# Define the GraphQL endpoint
url = "https://api-prod.omnivore.app/api/graphql"


apikey = "<your-omnivore-api-key>"

def get_api_key():
    # Check if it's provided as a command line argument
    parser = argparse.ArgumentParser(description="Process API key.")
    parser.add_argument("--apikey", type=str, help="API key for Omnivore")
    args = parser.parse_args()

    # Check if the API key matches the required format
    if args.apikey:
        return args.apikey

    # If not set, check if the API key is set as an environment variable
    api_key = os.getenv("OMNIVORE_API_KEY")

    if api_key:
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

print("Nodes have been saved to nodes-id-url.json")
