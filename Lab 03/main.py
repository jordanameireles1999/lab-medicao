from os import environ

import src.repositories as repos
import src.pullRequests as prs


def main(num_repos: int):
    """
    Run the pipeline.
    """
    # print('Generating repositories CSV...')
    # repos_filename = repos.generate_csv(num_repos)
    # print('Generating pullRequests CSV...')
    # prs.generate_csv(repos_filename)
    prs.generate_csv('./out/repositories.csv')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a CSV file with the most popular repositories on GitHub.')
    parser.add_argument('-n', '--num_repos', type=int, default=100, help='Number of repositories to generate.')

    args = parser.parse_args()
    main(args.num_repos)
