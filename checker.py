import os
import re

import click
from github import Github


@click.command()
@click.option('--org', prompt='Organization Name',
              help='The organization to check')
@click.option('--team', prompt='The team name to check',
              help='The team name to check')
def check_org(org, team):
    g = Github(os.environ['GITHUB_TOKEN'])


    org = g.get_organization(org)
    repos = org.get_repos()

    for repo in repos:
        regex = '([a-zA-Z\-]+)-{team}-test'.format(
            team=team
        )

        if re.match(regex, repo.name):
            # check for a pr
            prs = repo.get_pulls()

            candidate_prs = []
            latest_update = None
            for pr in prs:
                if not pr.closed_at:
                    candidate_prs.append(
                        {
                            'title': pr.title,
                            'comments': pr.review_comments,
                            'closed_at': pr.closed_at
                        }
                    )

            if candidate_prs:
                print "Candidate {repo} has {prs_open} open PRs".format(
                    repo=repo.name,
                    prs_open=len(candidate_prs)
                )

if __name__  == '__main__':
    check_org()
