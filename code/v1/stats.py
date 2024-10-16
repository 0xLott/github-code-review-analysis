import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Helper function
def parse_pull_requests(pull_request_data):
    return ast.literal_eval(pull_request_data)

def load_data():
    pr_body = pd.read_csv('pr_body_results.csv')
    pr_size = pd.read_csv('pr_size_results.csv')
    pr_interaction = pd.read_csv('pr_interaction_results.csv')
    pr_results = pd.read_csv('pr_results.csv')

    return pr_body, pr_size, pr_interaction, pr_results

# RQ 01
def rq_01(pr_size_data, pr_results_data):
    sizes = []
    reviews = []

    for size_row, result_row in zip(pr_size_data['pullRequests'], pr_results_data['pullRequests']):
        size_data = parse_pull_requests(size_row)
        result_data = parse_pull_requests(result_row)
        
        for size_info, result_info in zip(size_data, result_data):
            pr_size = size_info['changedFiles'] + size_info['additions'] + size_info['deletions']
            review_count = result_info['reviews']['totalCount']

            sizes.append(pr_size)
            reviews.append(review_count)

    sizes = np.array(sizes)
    reviews = np.array(reviews)

    correlation = np.corrcoef(sizes, reviews)[0, 1]
    return correlation

print(rq_01(pr_size, pr_results))