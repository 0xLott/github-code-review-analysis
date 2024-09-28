from data_collector import run_query

batch_size = 20

if __name__ == '__main__':
    with open("query/query.gql", "r") as file:
        query = file.read()

    variables = {'num_repos': 8, 'num_prs': 2}

    run_query(batch_size, query, variables)