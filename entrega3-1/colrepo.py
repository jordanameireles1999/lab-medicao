import requests
import csv

# Configurações
TOKEN = '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'
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Lista para guardar repositórios
selected_repos = []

# Começar o cursor como null
cursor = "null"

while len(selected_repos) < 200:
    QUERY = f"""
    {{
      search(query: "is:public", type: REPOSITORY, first: 100, after: {cursor}) {{
        edges {{
          node {{
            ... on Repository {{
              nameWithOwner
            }}
          }}
          cursor
        }}
      }}
    }}
    """
    
    response = requests.post('https://api.github.com/graphql', json={'query': QUERY}, headers=HEADERS)
    data = response.json()

    if 'data' not in data:
        print("Erro na resposta da API:")
        print(data)
        exit()

    for edge in data['data']['search']['edges']:
        if len(selected_repos) < 200:
            selected_repos.append(edge['node']['nameWithOwner'])

    cursor = f'"{data["data"]["search"]["edges"][-1]["cursor"]}"'

print("200 repositórios populares selecionados.")
