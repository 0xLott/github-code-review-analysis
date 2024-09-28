import os
import requests
import csv
import ast

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# GitHub GraphQL API endpoint
url = "https://api.github.com/graphql"

def load_query(query_file):
    with open(query_file, 'r') as file:
        return file.read()

def run_query(query_name, batch_size, query_file, variables):
    query = load_query(query_file)
    variables['cursor'] = ''
    total_repos = variables['num_repos']
    total_prs = variables['num_prs']
    retrieved_data = []

    def process_batch(batch_repos_size, cursor):
        variables['num_repos'] = batch_repos_size
        variables['cursor'] = cursor
        json = dispatch_request(query, variables).json()

        nodes = json['data']['search']['edges']
        for node in nodes:
            repository_data = {
                "id": node['node']['id'],
                "pullRequests": []
            }

            # Process pull requests for the current repository and extend with the nodes since pull requests might not be paginated
            pull_requests = node['node']['pullRequests']
            repository_data["pullRequests"].extend(pull_requests['nodes'])

            retrieved_data.append(repository_data)

        return json

    def process_pagination(total_repos):
        full_batches_repos = total_repos // batch_size
        remaining_repos = total_repos % batch_size
        cursor = None

        for batch_number in range(full_batches_repos):
            print(f'Page {batch_number + 1}')
            cursor = json['data']['search']['pageInfo']['endCursor'] if cursor else ''
            process_batch(batch_size, cursor)

        if remaining_repos > 0:
            print('Last Page:')
            process_batch(remaining_repos, cursor)

    if total_repos > batch_size:
        process_pagination(total_repos)
    else:
        process_batch(total_repos, None)

    write_data(retrieved_data, query_name)


def dispatch_request(query, variables):
    response = requests.post(
        url,
        json={
            "query": query,
            "variables": variables
        },
        headers=headers
    )

    print("Query dispatched")

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    return response


def write_data(data, query_name):
    file_path = f'queries/results/{query_name}_results.csv'
    
    parsed_data = [ast.literal_eval(item) if isinstance(item, str) else item for item in data]
    headers = parsed_data[0].keys()

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(parsed_data)

    print(f'Data written to {file_path} file')
