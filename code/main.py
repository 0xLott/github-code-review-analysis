import os
from data_collector import run_query

queries = {
    "pr": "queries/pr_query.gql",
    "pr_size": "queries/pr_size_query.gql",
    "pr_time": "queries/pr_time_query.gql",
    "pr_body": "queries/pr_body_query.gql",
    "pr_interaction": "queries/pr_interaction_query.gql"
}

batch_size = 10

variables = {
    "num_repos": 100,
    "num_prs": 10,
}

if __name__ == "__main__":
    run_query("pr_body", batch_size, "queries/pr_body_query.gql", variables)
    # for query_name, query_file in queries.items():
    #     run_query(query_name batch_size, query_file, variables)