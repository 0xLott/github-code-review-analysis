import os
from data_collector import run_query

queries = {
    "pr": "queries/pr_query.gql",
    "pr_size": "queries/pr_size_query.gql",
    "pr_time": "queries/pr_time_query.gql",
    "pr_body": "queries/pr_body_query.gql",
    "pr_interaction": "queries/pr_interaction_query.gql"
}

batch_size = 1  # batch_size = max_requests_per_hour / repos * prs

variables = {
    "num_repos": 200,
    "num_prs": 100,
}

if __name__ == "__main__":
    print('''
    1: Fetch data from GitHub GraphQL API
    2: Calculate and display stats
    ''')
    
    option = input("Action: ")
    match option:
        case "1":
            for query_name, query_file in queries.items():
                run_query(query_name, batch_size, query_file, variables)
        case _:
            exit()

    # Run single query
    # run_query("pr_body", batch_size, queries["pr_size"], variables)