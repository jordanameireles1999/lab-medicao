import requests
import csv
import time
import numpy as np  # Importa a biblioteca numpy para cálculos estatísticos

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

cursor = None
formatted_data = []
request_times = []  # Lista para armazenar os tempos de cada requisição

while True:  # Loop até que o desvio padrão esteja próximo de 1
    start_time = time.time()  # Início da requisição
    response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': {'cursor': cursor}}, headers=headers)
    end_time = time.time()  # Fim da requisição

    request_time = end_time - start_time
    request_times.append(request_time)

    json_data = response.json()

    if 'errors' in json_data:
        print(f"Erro na resposta da API: {json_data['errors']}")
        break
    elif 'data' not in json_data:
        print(f"Resposta inesperada da API: {json_data}")
        break

    repositories_data = json_data['data']['search']['edges']
    for repo in repositories_data:
        repo_node = repo['node']
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

    # Cálculo de média e desvio padrão após cada requisição
    if len(request_times) > 1:  # Calcula se houver mais de uma medição
        mean = np.mean(request_times)
        std_dev = np.std(request_times)
        print(f"Média atual: {mean}, Desvio Padrão atual: {std_dev}")

        if abs(std_dev - 1) < 0.1:  # Condição de parada: desvio padrão próximo de 1
            break
          
# Escrevendo os dados coletados em um arquivo CSV
fieldnames = ['name', 'description', 'url', 'primaryLanguage', 'createdAt', 'updatedAt', 'stargazers', 'forks', 'watchers', 'issues', 'pullRequests', 'releases', 'branches', 'tags', 'commitComments']

with open('github_repositories.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in formatted_data:
        writer.writerow(data)

print(f"Total de repositórios processados: {len(formatted_data)}")
print(f"Tempo médio das requisições: {mean} segundos")
print(f"Desvio padrão do tempo das requisições: {std_dev} segundos")

# Contando o número de caracteres no arquivo CSV
total_characters = 0
with open('github_repositories.csv', 'r', encoding='utf-8') as file:
    for line in file:
        total_characters += len(line)

print(f"Total de caracteres no arquivo CSV: {total_characters}")