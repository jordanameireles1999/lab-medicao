from random import randint
import requests
from time import sleep

MAX_QUERY_ATTEMPTS = 10
GITHUB_INDEX = 0
GITHUB_TOKEN = [
    # Add your tokens here
    ]

def query_runner(query: str, attemp=1) -> dict:
    """
    This function runs a query against the GitHub GraphQL API and returns the result.
    """
    url = 'https://api.github.com/graphql'
    global GITHUB_INDEX
    token = GITHUB_TOKEN[GITHUB_INDEX]
    headers = {'Authorization': 'Bearer {}'.format(token)}
    try:
        sleep(randint(1, 15))
        response = requests.post(url, json={'query': query}, headers=headers)
        remaing_requests = response.headers.get('x-ratelimit-remaining')
        message = ("Response: ", response.status_code, " -> ", response.json(), "\n") if not remaing_requests else None
        print(
            f'Remaining requests: {remaing_requests} {type(remaing_requests)}\n {message}',
            '-----------------------------------------------------------'
        )
        # Handle seconday rate limit
        if not remaing_requests and response.status_code in (403, 502):
            sleep(30)
            return query_runner(query, attemp)
        # Change token if necessary
        if remaing_requests <= '1':
            print('Renewing token...')
            GITHUB_INDEX = (GITHUB_INDEX + 1) % len(GITHUB_TOKEN)
            return query_runner(query, attemp)
        # Success
        elif response.status_code == 200:
            return response.json()
        # Handle server-side error calling the function again with the same query
        # but with a higher attemp number.
        elif response.status_code == 502 and attemp <= MAX_QUERY_ATTEMPTS:
            print('Attemp {}/{} get Error 502. Retrying...'.format(attemp, MAX_QUERY_ATTEMPTS))
            return query_runner(query, attemp + 1)
        # Terminate the program if the attemp number is greater than the maximum.
        elif response.status_code == 502 and attemp > MAX_QUERY_ATTEMPTS:
            print('Error 502. Maximum number of attempts reached. Try again later.')
            exit(1)
        # Unexpected error will be printed and the program will be terminated.
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))
    # Handle ChunkedEncodingError exception (connection broken)
    except Exception as e:
        print(e)
        return query_runner(query, attemp)
