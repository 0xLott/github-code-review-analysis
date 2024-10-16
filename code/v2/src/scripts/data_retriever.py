import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import time

dotenv_path = Path('../.env')
load_dotenv(dotenv_path)

GITHUB_TOKEN = os.getenv('GITHUB_API_TOKEN')
GITHUB_API_URL = 'https://api.github.com/graphql'
GITHUB_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}


def dispatch_request(query, variables):
    try:
        response = requests.post(
            GITHUB_API_URL,
            json={
                "query": query,
                "variables": variables
            },
            headers=GITHUB_HEADERS
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        return response

    except Exception as e:
        print(f"Error: {e.message}, sleeping for 5 minutes")
        time.sleep(300)


def read_query(query_file):
    with open(query_file, 'r') as file:
        return file.read()


def run_query(query_file, variables, data_function):
    query = read_query(query_file)
    response = dispatch_request(query, variables)

    if response is None:
        return None
    else:
        data = response.json()
        data_function(data)
        return data
