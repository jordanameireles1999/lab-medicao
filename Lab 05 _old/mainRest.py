import requests
import csv
import time
import numpy as np

# Token de acesso e cabeçalhos
token = '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'  
headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/json'
}

# Função para obter uma lista de repositórios
def get_repositories(query, headers):
    try:
        url = f"https://api.github.com/search/repositories?q={query}&per_page=10"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Erro de Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro na Requisição: {err}")
    return []

# Função para obter detalhes adicionais do repositório
def get_additional_repo_details(repo, headers):
    repo_details = {}
    base_url = repo['url']

    details_endpoints = ['stargazers', 'subscribers', 'forks', 'issues', 'pulls', 'releases', 'branches', 'tags', 'comments']

    for endpoint in details_endpoints:
        try:
            url = f"{base_url}/{endpoint}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            repo_details[endpoint] = len(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter {endpoint} de {repo['name']}: {e}")
            repo_details[endpoint] = 0

    return repo_details

# Coleta de dados
print("Iniciando a coleta de dados dos repositórios...")
repositories = get_repositories("stars:>100", headers)
formatted_data = []
request_times = []  # Lista para armazenar os tempos de cada requisição

for repo in repositories:
    print(f"Coletando dados para o repositório: {repo['name']}")
    start_time = time.time()

    try:
        repo_details = get_additional_repo_details(repo, headers)
        end_time = time.time()
        request_time = end_time - start_time
        request_times.append(request_time)

        repo_info = {
            'name': repo['name'],
            'description': repo['description'],
            'url': repo['html_url'],
            'createdAt': repo['created_at'],
            'updatedAt': repo['updated_at'],
            'stargazers': repo_details['stargazers'],
            'watchers': repo_details['subscribers'],
            'forks': repo_details['forks'],
            'issues': repo_details['issues'],
            'pullRequests': repo_details['pulls'],
            'releases': repo_details['releases'],
            'branches': repo_details['branches'],
            'tags': repo_details['tags'],
            'commitComments': repo_details['comments']
        }
        formatted_data.append(repo_info)
    except Exception as e:
        print(f"Erro ao processar o repositório {repo['name']}: {e}")

print("Coleta de dados concluída.")

# Cálculo de média e desvio padrão
mean_time = np.mean(request_times)
std_dev_time = np.std(request_times)
print(f"Média do Tempo de Requisição: {mean_time}, Desvio Padrão: {std_dev_time}")

# Gravação dos dados em CSV
csv_filename = 'github_repositories_rest.csv'
fieldnames = ['name', 'description', 'url', 'createdAt', 'updatedAt', 'stargazers', 'watchers', 'forks', 'issues', 'pullRequests', 'releases', 'branches', 'tags', 'commitComments']

print(f"Gravando dados em {csv_filename}...")
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in formatted_data:
        writer.writerow(data)

print("Dados gravados com sucesso.")

# Contando o número de caracteres no arquivo CSV
total_characters = 0
with open(csv_filename, 'r', encoding='utf-8') as file:
    total_characters = sum(len(line) for line in file)

print(f"Total de caracteres no arquivo CSV: {total_characters}")