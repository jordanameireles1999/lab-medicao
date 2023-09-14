import requests


# Configuração
TOKEN = "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"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
ENDPOINT = "https://api.github.com/graphql"

# Consulta GraphQL
QUERY = """
{
  search(query: "stars:>10000", type: REPOSITORY, first: 100) {
   edges{
      node{
        ... on Repository {
          nameWithOwner
          createdAt
          pullRequests(states: MERGED) {
            totalCount
          }
          updatedAt
            stargazers {
              totalCount
          }
          issues {
            totalCount
          }
          closedIssues: issues(states: CLOSED) {
            totalCount
          }
          primaryLanguage {
            name
          }
      }
    }
  }
  }
}
"""

response = requests.post(ENDPOINT, json={"query": QUERY}, headers=HEADERS) 
data = response.json()



# Processar os dados

# Verifica se a resposta não é nula e contém dados
if data.get("data") and data["data"]["search"] and data["data"]["search"]["edges"]:
    # Processar os dados
    for edge in data["data"]["search"]["edges"]:
        repo = edge["node"]
        print(f"Repository: {repo['nameWithOwner']}")
        print(f"Created At: {repo['createdAt']}")
        print(f"Total Merged PRs: {repo['pullRequests']['totalCount']}")
        print(f"Updated At: {repo['updatedAt']}")
        # Imprimindo o número de estrelas
        stars = repo['stargazers']['totalCount']
        print(f"Stars: {stars}")

        # Verifica se o campo de linguagem primária está presente
        if "primaryLanguage" in repo and repo["primaryLanguage"] is not None:
            primary_language = repo["primaryLanguage"]["name"]
            print(f"Primary Language: {primary_language}")
        else:
            print("Primary Language: N/A")

        # Calcula a porcentagem de issues fechadas
        total_issues = repo['issues']['totalCount']
        closed_issues = repo['closedIssues']['totalCount']
        
        if total_issues > 0:
            closed_percentage = (closed_issues / total_issues) * 100
            print(f"Closed Issues Percentage: {closed_percentage:.2f}%")
        else:
            print("Closed Issues Percentage: N/A")
            
        print("------") 
else:
    print("Nenhum dado encontrado na resposta.")

   
    
#"""print(f"Total Releases: {repo['releases']['totalCount']}")
    
#    print(f"Primary Language: {repo['primaryLanguage']['name']}")
    
#    print(f"Issues Closed Ratio: {closed_issues}/{total_issues}")
#    print("------") """#