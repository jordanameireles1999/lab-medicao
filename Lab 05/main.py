import requests
import csv

# Seu token de acesso pessoal do GitHub
token = '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'
headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/json'
}

# A consulta GraphQL com uma variável de cursor para paginação
query = """
query ($cursor: String) {
  search(query: "stars:>100", type: REPOSITORY, first: 10, after: $cursor) {
    edges {
      node {
        ... on Repository {
          name
          description
          url
          primaryLanguage {
            name
          }
          createdAt
          updatedAt
          stargazers {
            totalCount
          }
          forks {
            totalCount
          }
          watchers {
            totalCount
          }
          issues(states: [OPEN, CLOSED]) {
            totalCount
          }
          pullRequests(states: [OPEN, CLOSED, MERGED]) {
            totalCount
          }
          releases {
            totalCount
          }
          branches: refs(refPrefix: "refs/heads/") {
            totalCount
          }
          tags: refs(refPrefix: "refs/tags/") {
            totalCount
          }
          commitComments {
            totalCount
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

cursor = None  # Inicialmente, não há cursor
formatted_data = []

for page_number in range(3):  # Faz três consultas para obter até 30 repositórios
    response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
    json_data = response.json()

    if 'errors' in json_data:
        print(f"Erro na resposta da API: {json_data['errors']}")
        break

    repositories_data = json_data['data']['search']['edges']
    
    for repo in repositories_data:
        repo_node = repo['node']
        # Verifique se primaryLanguage não é None antes de tentar acessar 'name'
        primary_language = repo_node.get('primaryLanguage')
        primary_language_name = primary_language.get('name', None) if primary_language else None

        repo_info = {
            'name': repo_node.get('name', ''),
            'description': repo_node.get('description', ''),
            'url': repo_node.get('url', ''),
            'primaryLanguage': primary_language_name,
            'createdAt': repo_node.get('createdAt', ''),
            'updatedAt': repo_node.get('updatedAt', ''),
            'stargazers': repo_node.get('stargazers', {}).get('totalCount', 0),
            'forks': repo_node.get('forks', {}).get('totalCount', 0),
            'watchers': repo_node.get('watchers', {}).get('totalCount', 0),
            'issues': repo_node.get('issues', {}).get('totalCount', 0),
            'pullRequests': repo_node.get('pullRequests', {}).get('totalCount', 0),
            'releases': repo_node.get('releases', {}).get('totalCount', 0),
            'branches': repo_node.get('branches', {}).get('totalCount', 0),
            'tags': repo_node.get('tags', {}).get('totalCount', 0),
            'commitComments': repo_node.get('commitComments', {}).get('totalCount', 0)
        }
        formatted_data.append(repo_info)

    cursor = json_data['data']['search']['pageInfo']['endCursor']
    if not json_data['data']['search']['pageInfo']['hasNextPage']:
        break

# Escrevendo os dados coletados em um arquivo CSV
fieldnames = ['name', 'description', 'url', 'primaryLanguage', 'createdAt', 'updatedAt', 'stargazers', 'forks', 'watchers', 'issues', 'pullRequests', 'releases', 'branches', 'tags', 'commitComments']

with open('github_repositories.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in formatted_data:
        writer.writerow(data)

print(f"Total de repositórios processados: {len(formatted_data)}")