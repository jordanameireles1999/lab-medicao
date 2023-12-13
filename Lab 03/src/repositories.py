import pandas as pd

import src.queries as queries
from src.utils import query_runner


OUTPUT = 'out/repositories.csv'

def generate_csv(num_repos: int):
    """
    This function generates a CSV file with the most popular repositories on GitHub.
    """
    after = 'null'
    df = pd.DataFrame(columns=['nameWithOwner', 'url', 'createdAt', 'stargazers', 'pullRequests'])
    while len(df) < num_repos:
        query = queries.repositories.replace('{after}', after)
        results = query_runner(query)
        for repo in results['data']['search']['nodes']:
            pull_requests = repo['prClosed']['totalCount'] + repo['prMerged']['totalCount']
            if pull_requests < 100: continue
            df = pd.concat([df, pd.DataFrame({
                'nameWithOwner': [repo['nameWithOwner']],
                'url': [repo['url']],
                'createdAt': [repo['createdAt']],
                'stargazers': [repo['stargazers']['totalCount']],
                'pullRequests': [pull_requests]
            })])
        after = '"' + results['data']['search']['pageInfo']['endCursor'] + '"'
        if not results['data']['search']['pageInfo']['hasNextPage']:
            break
    df = df.sort_values(by='stargazers', ascending=False)[:num_repos]
    df.to_csv(OUTPUT, index=False)
    return OUTPUT



