import requests
import csv
import time
from datetime import datetime
import os  # Importe o módulo os para verificar se o arquivo já existe

# Configuração
TOKEN = "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"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
ENDPOINT = "https://api.github.com/graphql"

# Consulta GraphQL para listar os repositórios Java
QUERY = """
query SearchRepositories($queryString: String!, $first: Int, $after: String) {
    search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
        pageInfo {
            endCursor
            hasNextPage
        }
        edges {
            node {
                ... on Repository {
                    nameWithOwner
                    url
                    stargazers {
                        totalCount
                    }
                    languages(first: 1) {
                        nodes {
                            name
                        }
                    }
                    createdAt
                    releases {
                        totalCount
                    }
                }
            }
        }
    }
}
"""

# Função para calcular a idade em anos
def calculate_age(created_at):
    created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    current_date = datetime.now()
    age = current_date.year - created_date.year - ((current_date.month, current_date.day) < (created_date.month, created_date.day))
    return age

# Função para exportar dados para CSV
def export_to_csv(repositories):
    csv_file_path = "repositories.csv"
    # Verifique se o arquivo já existe
    file_exists = os.path.exists(csv_file_path)

    with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Repository", "URL", "Owner", "Stars", "Primary Language", "LOC", "Comments", "Releases", "Age (years)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        # Se o arquivo não existir, escreva o cabeçalho
        if not file_exists:
            writer.writeheader()

        for repo in repositories:
            owner, name = repo["node"]["nameWithOwner"].split("/")
            row = {
                "Repository": name,
                "URL": repo["node"]["url"],
                "Owner": owner,
                "Stars": repo["node"]["stargazers"]["totalCount"],
                "Primary Language": repo["node"]["languages"]["nodes"][0]["name"] if repo["node"]["languages"]["nodes"] else "N/A",
                "LOC": 0,  # Preencha com as métricas reais de LOC
                "Comments": 0,  # Preencha com as métricas reais de comentários
                "Releases": repo["node"]["releases"]["totalCount"],
                "Age (years)": calculate_age(repo["node"]["createdAt"])
            }
            writer.writerow(row)

# Execução da consulta GraphQL e exportação para CSV
def get_repositories(cursor=None):
    response = requests.post(ENDPOINT, json={"query": QUERY, "variables": {"queryString": "language:Java", "first": 100, "after": cursor}}, headers=HEADERS)
    data = response.json()

    if data and isinstance(data, dict) and "data" in data and "search" in data["data"] and "edges" in data["data"]["search"]:
        repositories = data["data"]["search"]["edges"]
        export_to_csv(repositories)

        pageInfo = data["data"]["search"]["pageInfo"]
        return pageInfo["endCursor"] if pageInfo["hasNextPage"] else None

    elif data and "errors" in data:
        print("Erro na consulta. Tentando novamente após 2 segundos...")
        time.sleep(2)
        return get_repositories(cursor=cursor)

    else:
        print("Nenhum dado encontrado na resposta.")
        return None

endCursor = None
for _ in range(10):  # 10 iterações para buscar 1000 registros (100 por iteração)
    endCursor = get_repositories(cursor=endCursor)
    if not endCursor:
        break

print("Lista de repositórios Java exportada para 'repositories.csv'.")
