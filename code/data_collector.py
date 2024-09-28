from dotenv import load_dotenv
import csv
import os
import requests

load_dotenv()
token = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# GitHub GraphQL API endpoint
url = "https://api.github.com/graphql"


def run_query(batch_size, query, variables):
    variables['cursor'] = ''
    total_repos = variables['num_repos']
    retrieved_data = []

    def process_batch(batch_size):
        variables['num_repos'] = batch_size
        json = dispatch_request(query, variables).json()

        nodes = json['data']['search']['edges']
        for node in nodes:
            retrieved_data.append(node['node'])

        variables['cursor'] = json['data']['search']['pageInfo']['endCursor']
        return json

    if total_repos > batch_size:
        full_batches = total_repos // batch_size
        remaining_items = total_repos % batch_size

        for batch_number in range(full_batches):
            print(f'Page {batch_number + 1}')
            process_batch(batch_size)

        if remaining_items > 0:
            print('Last Page:')
            process_batch(remaining_items)
    else:
        process_batch(total_repos)

    write_data(retrieved_data)


def dispatch_request(query, variables):
    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        },
        headers=headers
    )    

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    print("Query dispatched")

    return response


def write_data(json):
    csv_file_path = 'query/results.csv'

    parsed_data = [ast.literal_eval(item) if isinstance(item, str) else item for item in json]

    headers = parsed_data[0].keys()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(parsed_data)