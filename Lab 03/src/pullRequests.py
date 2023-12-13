from datetime import datetime as dt, timedelta
import multiprocessing as mul

import pandas as pd

import src.queries as queries
from src.utils import query_runner


OUTPUT = 'out/pullRequests.csv'
COLUMNS = [
    'nameWithOwner', 'id', 'title', 'state', 'createdAt', 'closedAt',
    'changedFiles', 'additions', 'deletions', 'reviews', 'body',
    'participants', 'comments'
    ]


def get_pull_requests(nameWithOwner: str):
    """
    This function returns the pull requests data of a repository.
    """
    after = 'null'
    prs = []
    owner, name = nameWithOwner.split('/')
    while True:
        query = queries.pull_requests.replace('{owner}', owner)\
                                     .replace('{name}', name)\
                                     .replace('{after}', after)
        results = query_runner(query)
        if not results: continue
        for pr in results['data']['repository']['pullRequests']['nodes']:
            prs.append((
                nameWithOwner,
                pr['id'],
                pr['title'],
                pr['state'],
                pr['createdAt'],
                pr['closedAt'],
                pr['changedFiles'],
                pr['additions'],
                pr['deletions'],
                pr['reviews']['totalCount'],
                len(pr['body']),
                pr['participants']['totalCount'],
                pr['comments']['totalCount']
            ))
        after = '"' + results['data']['repository']['pullRequests']['pageInfo']['endCursor'] + '"'
        if not results['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
            break

    output = pd.DataFrame(prs, columns=COLUMNS)
    # Filter pull requests that have at least a review.
    output = output[output['reviews'] > 0]
    # Add the review time spent.
    output['hours_spent'] = output.apply(lambda x: (dt.strptime(x['closedAt'], '%Y-%m-%dT%H:%M:%SZ') - dt.strptime(x['createdAt'], '%Y-%m-%dT%H:%M:%SZ')), axis=1)
    output['hours_spent'] = output['hours_spent'].apply(lambda x: x.days * 24 + x.seconds / 3600)
    # Filter pull requests that have more than an hour to review.
    output = output[output['hours_spent'] >= 1]
    return output


def generate_csv(input_path: str):
    """
    This function generates a CSV file with the selected pull requests from a file.
    """
    input = pd.read_csv(input_path)
    repositories = input['nameWithOwner'].unique().tolist()
    pool = mul.Pool(10)
    results = pool.map(get_pull_requests, repositories)
    output = pd.concat(results)
    output.to_csv(OUTPUT, index=False)
    return OUTPUT
