import requests
import csv

GITHUB_API_TOKEN = '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'

# URL da API do GitHub para buscar repositórios com mais de 100 estrelas
url = 'https://api.github.com/search/repositories?q=stars:>100&per_page=100&page='

# Cabeçalho da requisição com o token de acesso
headers = {
    'Authorization': f'token {GITHUB_API_TOKEN}'
}

try:
    # Cria um arquivo CSV para escrever as informações dos repositórios
    with open('repositories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'full_name', 'html_url', 'stargazers_count']
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
                    writer.writerow({
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'html_url': repo['html_url'],
                        'stargazers_count': repo['stargazers_count']
                    })

                print(f'Página {page} processada. {len(repositories)} repositórios adicionados.')
            else:
                print(f'Erro na requisição da página {page}: Código {response.status_code}')
except Exception as e:
    print(f'Erro na requisição: {str(e)}')

print(f'Arquivo "repositories.csv" criado com informações de 200 repositórios com mais de 100 estrelas.')