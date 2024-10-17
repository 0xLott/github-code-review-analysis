import json
import uuid
from datetime import datetime, timedelta
from scripts import data_retriever
from dotenv import load_dotenv
from pathlib import Path
import scripts.file_manager as file_manager

dotenv_path = Path('../.env')
load_dotenv(dotenv_path)

# Constants
PULL_REQUESTS_PER_PAGE = 20
DEPENDABOT_GITHUB_USERNAME = 'dependabot'

# GraphQL Queries
pull_request_query = 'query/pull_request_query.graphql'
repository_query = 'query/repository_query.graphql'

# Datasets
repository_dataset_file = 'dataset/repository.json'
pull_requests_dataset_file = 'dataset/pullrequest.json'


def is_difference_greater_than_one_hour(datetime1, datetime2):
    dt1 = datetime.strptime(datetime1, "%Y-%m-%dT%H:%M:%SZ")
    dt2 = datetime.strptime(datetime2, "%Y-%m-%dT%H:%M:%SZ")
    difference = abs(dt1 - dt2)
    return difference > timedelta(hours=1)


def pull_requests_data_function(data):
    pull_requests = data['data']['repository']['pullRequests']['nodes']

    print(f'Mined pull requests! {pull_requests}')

    for pull_request in pull_requests:
        if pull_request['author'] is not None and pull_request['reviews']['totalCount'] > 0 and is_difference_greater_than_one_hour(
            pull_request['closedAt'], pull_request['createdAt']
        ):
            pull_request_data = {
                'objectId': str(uuid.uuid4()),
                'repositoryName': data['data']['repository']['name'],
                'ownerName': data['data']['repository']['owner']['login'],
                'author': pull_request['author']['login'],
                'state': pull_request['state'],
                'createAt': str(pull_request['createdAt']),
                'closetAt': str(pull_request['closedAt']),
                'mergedAt': str(pull_request['mergedAt']),
                'changedFiles': pull_request['changedFiles'],
                'deletions': pull_request['deletions'],
                'additions': pull_request['additions'],
                'description': str(pull_request['body']),
                'participantsCount': pull_request['participants']['totalCount'],
                'commentsCount': pull_request['comments']['totalCount'],
                'reviewsCount': pull_request['reviews']['totalCount'],
            }

            file_manager.save_to_json(pull_requests_dataset_file, pull_request_data)


def mine_pull_requests(repository):
    pull_requests_total_count = repository['pullRequests']['totalCount']

    variables = {
        'repo_name': repository['name'],
        'repo_owner': repository['owner']['login'],
        'pull_request_num': 20,
        'cursor': ''
    }

    total_batches = (pull_requests_total_count % PULL_REQUESTS_PER_PAGE) + (
            pull_requests_total_count // PULL_REQUESTS_PER_PAGE)

    for batch in range(total_batches):
        data = data_retriever.run_query(
            query_file=pull_request_query,
            variables=variables,
            data_function=pull_requests_data_function
        )

        if data is not None:
            variables['cursor'] = data['data']['repository']['pullRequests']['pageInfo']['endCursor']


def repository_data_function(data):
    for item in data['data']['search']['edges']:
        repository = item['node']

        if repository['pullRequests']['totalCount'] > 100:
            repository_data = {
                'objectId': str(uuid.uuid4()),
                'name': repository['name'],
                'owner': repository['owner']['login'],
                'stargazers': repository['stargazerCount'],
                'pullRequestsCount': repository['pullRequests']['totalCount'],
                'nextPageCursor': data['data']['search']['pageInfo']['endCursor'],
                'createdAt': str(datetime.now())
            }

            file_manager.save_to_json(repository_dataset_file, repository_data)

            print(f'Mined repository: {repository['name']}')

            mine_pull_requests(repository)


def lambda_handler():
    while file_manager.get_json_size(repository_dataset_file) < 200:
        last_repository = file_manager.get_last_item(repository_dataset_file)

        cursor = last_repository['nextPageCursor'] if last_repository else ''

        variables = {
            'cursor': cursor,
            'num_repos': 1
        }

        data_retriever.run_query(
            query_file=repository_query,
            variables=variables,
            data_function=repository_data_function
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Repository mining completed.')
    }


if __name__ == '__main__':
    lambda_handler()
