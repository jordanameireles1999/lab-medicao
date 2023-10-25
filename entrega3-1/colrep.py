import requests
import csv

# Configurações
TOKEN = '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'
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Lista para guardar repositórios filtrados
filtered_repos = []

# Começar o cursor como null
cursor = "null"

for _ in range(20):  # 20 buscas para um total de 200 repositórios (10 de cada vez)
    # Consulta GraphQL
    QUERY = f"""
    {{
      search(query: "is:public", type: REPOSITORY, first: 10, after: {cursor}) {{
        edges {{
          node {{
            ... on Repository {{
              nameWithOwner
              mergedPRs: pullRequests(states: MERGED) {{
                totalCount
              }}
              closedPRs: pullRequests(states: CLOSED) {{
                totalCount
              }}
            }}
          }}
          cursor
        }}
      }}
    }}
    """
    
    response = requests.post('https://api.github.com/graphql', json={'query': QUERY}, headers=HEADERS)
    data = response.json()
    
    # Se não tivermos 'data' na resposta, imprimir o erro e sair
    if 'data' not in data:
        print("Erro na resposta da API:")
        print(data)
        exit()
    
    # Adicionar repositórios que têm mais de 100 PRs (MERGED + CLOSED) à nossa lista
    for edge in data['data']['search']['edges']:
        node = edge['node']
        total_prs = node['mergedPRs']['totalCount'] + node['closedPRs']['totalCount']
        if total_prs >= 100:
            filtered_repos.append(node)
    
    # Atualizar o cursor para a próxima busca
    cursor = f'"{data["data"]["search"]["edges"][-1]["cursor"]}"'

# Salvar em CSV
with open('popular_repos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["Repository", "PRs (MERGED)", "PRs (CLOSED)"])
    for repo in filtered_repos:
        writer.writerow([repo['nameWithOwner'], repo['mergedPRs']['totalCount'], repo['closedPRs']['totalCount']])

print("Arquivo CSV gerado com sucesso!")
