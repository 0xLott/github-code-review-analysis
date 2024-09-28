import os
from data_collector import run_query

queries = {
    "pr_body": "queries/pr_body_query.gql",
    "pr_size": "queries/pr_size_query.gql",
    "pr_description": "queries/pr_description_query.gql",
    "pr_interaction": "queries/pr_interaction_query.gql",
    "pr": "queries/pr_query.gql"
}

batch_size = 20

variables = {
    "num_repos": 10,
    "num_prs": 5,
}


if __name__ == "__main__":
    for query_name, query_file in queries.items():
        run_query("pr_body", batch_size, query_file, variables)