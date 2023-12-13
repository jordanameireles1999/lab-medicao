repositories = """
    {
      search(query: "stars:>100 sort:stars", type: REPOSITORY, first: 25, after: {after}) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          ... on Repository {
            nameWithOwner
            url
            createdAt
            stargazers {
              totalCount
            }
            prClosed: pullRequests(states: [CLOSED]) {
                totalCount
            }
            prMerged: pullRequests(states: [MERGED]) {
                totalCount
            }
          }
        }
      }
    }
    """

# mergedAt always return null when is not merged
# or return the same timestamp as closedAt
pull_requests = """
    {
      repository(owner: "{owner}", name: "{name}") {
        pullRequests(states: [CLOSED, MERGED], first: 100, after: {after}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            id
            title
            state
            createdAt
            closedAt
            changedFiles
            additions
            deletions
            reviews { totalCount }
            body
            participants { totalCount }
            comments { totalCount }
          }
        }
      }
    }
    """