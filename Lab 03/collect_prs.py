import requests

TOKEN = 'YOUR_GITHUB_API_TOKEN'
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.github.com/graphql"

def run_query(query, variables):
    request = requests.post(BASE_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed with status code {request.status_code}. {request.text}")

def collect_prs_from_repository(owner, name):
    PRs = []
    has_next_page = True
    cursor = None
    
    while has_next_page:
        variables = {
            "owner": owner,
            "name": name,
            "after": cursor
        }
        
        result = run_query(pull_requests, variables)
        
        PRs.extend(result['data']['repository']['pullRequests']['nodes'])
        page_info = result['data']['repository']['pullRequests']['pageInfo']
        has_next_page = page_info['hasNextPage']
        cursor = page_info['endCursor']
    
    return PRs


