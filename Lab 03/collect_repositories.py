repositories_query = """
    {
      search(query: "stars:>100 sort:stars", type: REPOSITORY, first: 200) {
        nodes {
          ... on Repository {
            nameWithOwner
            url
            createdAt
            stargazers {
              totalCount
            }
            prCount: pullRequests {
                totalCount
            }
          }
        }
      }
    }
    """
