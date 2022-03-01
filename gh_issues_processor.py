import requests

import github as gh_api


def get_github_headers(api_token):
    """
    Load GH personal access token from file.
    """
    print("::set-output name=authenticating:: Authenticating.")
    gh_api.Github(api_token)
    print("::set-output name=authenticated:: Authenticated.")

    gh_headers = {"AUTHORIZATION": f"token {api_token}"}
    return gh_headers


def get_open_issues(gh_headers, org, repo):
    """
    Returns an iterator, over the org/repo open issues
    """
    issue_url = f"https://api.github.com/repos/{org}/{repo}/issues"

    params = {"page": 1}
    response = requests.get(
        issue_url, headers=gh_headers, params=params
    ).json()

    while len(response) > 0:
        for issue in response:
            yield issue
        params["page"] += 1
        response = requests.get(
            issue_url, headers=gh_headers, params=params
        ).json()


def get_linked_info(issue):
    """
    for the given issue, if "[Dd]uplicates: <org>/<repo>#XXX
    exists in PR body, returns the parsed org/repo/number
    Else return None
    """
    body = issue["body"].lower()

    if "\nduplicates" in body:
        _, url_string = body.split("\nduplicates ")
        next_newline = url_string.find("\n")
        if next_newline != -1:
            url_string = url_string[:next_newline]

        # form of: https://github.com/openedx/tcril-engineering/issues/32
        if url_string.startswith("https"):
            # find org/repo/issues/num
            orin = url_string[19:]
            org, repo, _, num = orin.split('/')

        # form of: openedx/tcril-engineering#130
        elif url_string.find('#') > 0:
            orepo, num = url_string.split('#')
            org, repo = orepo.split("/")

        else:
            print(f"::set-output name=error::Could not \
                    parse issue in duplicate line: {url_string}")
            return None

        return (org, repo, num)

    return None


def get_linked_status(gh_headers, linked_issue_info):
    """
    Returns the open/closed status of the linked issue
    """
    lorg, lrepo, lnum = linked_issue_info
    print(f"::set-output name=linkedIssueInfo::Found a \
           ßlinked issue: {lorg} {lrepo} {lnum}")
    issue_url = f"https://api.github.com/repos/{lorg}/{lrepo}/issues/{lnum}"

    response = requests.get(issue_url, headers=gh_headers).json()

    return response["state"]


def close_issue(gh_headers, issue):
    """
    Closes the issue (must be in the current repo)
    """
    issue_url = issue["url"]
    print(f"::set-output name=Closing::Closing Issue {issue_url}")
    params = {"state": "closed"}
    response = requests.patch(issue_url, headers=gh_headers, json=params)
    rs = response.status_code
    print(f"::set-output name=Closed::Closed with status code {rs}")
