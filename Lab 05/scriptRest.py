import requests
import csv
import time  # Importe o módulo de tempo

GITHUB_API_TOKEN = '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'

# URL da API do GitHub para pesquisar repositórios
url = 'https://api.github.com/search/repositories?q=stars:>100&per_page=100&page='

# Cabeçalho da requisição com o token de acesso
headers = {
    'Authorization': f'token {GITHUB_API_TOKEN}'
}

# Tempo de espera entre as requisições (em segundos)
intervalo_entre_requisicoes = 5  # Defina o tempo desejado, por exemplo, 5 segundos

try:
    # Cria um arquivo CSV para escrever as informações dos repositórios e issues
    with open('repositories_with_issues.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'full_name', 'html_url', 'stargazers_count', 'issue_number', 'title', 'state', 'created_at', 'updated_at', 'user']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Coleta informações de 200 repositórios (2 páginas com 100 repositórios cada)
        for page in range(1, 3):
            # Faz a requisição GET para obter os repositórios da página atual
            response = requests.get(f'{url}{page}', headers=headers)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                data = response.json()
                repositories = data['items']

                for repo in repositories:
                    # Coleta informações básicas do repositório
                    name = repo['name']
                    full_name = repo['full_name']
                    html_url = repo['html_url']
                    stargazers_count = repo['stargazers_count']

                    # Escreve as informações básicas no arquivo CSV
                    writer.writerow({
                        'name': name,
                        'full_name': full_name,
                        'html_url': html_url,
                        'stargazers_count': stargazers_count,
                        'issue_number': '',
                        'title': '',
                        'state': '',
                        'created_at': '',
                        'updated_at': '',
                        'user': ''
                    })

                    # Coleta informações de issues do repositório
                    issues_url = f'{repo["url"]}/issues?per_page=100'
                    issues_response = requests.get(issues_url, headers=headers)

                    # Verifica se a requisição das issues foi bem-sucedida
                    if issues_response.status_code == 200:
                        issues = issues_response.json()

                        for issue in issues:
                            issue_number = issue['number']
                            title = issue['title']
                            state = issue['state']
                            created_at = issue['created_at']
                            updated_at = issue['updated_at']
                            user = issue['user']['login']

                            # Escreve as informações das issues no arquivo CSV
                            writer.writerow({
                                'name': '',
                                'full_name': '',
                                'html_url': '',
                                'stargazers_count': '',
                                'issue_number': issue_number,
                                'title': title,
                                'state': state,
                                'created_at': created_at,
                                'updated_at': updated_at,
                                'user': user
                            })

                    print(f'Página {page} processada. {len(repositories)} repositórios adicionados.')
                    
                    # Adicione um atraso entre as requisições
                    time.sleep(intervalo_entre_requisicoes)
            else:
                print(f'Erro na requisição da página {page}: Código {response.status_code}')
except Exception as e:
    print(f'Erro na requisição: {str(e)}')

print(f'Arquivo "repositories_with_issues.csv" criado com informações de repositórios e issues.')
