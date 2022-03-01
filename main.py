import os
import gh_issues_processor as ghip


def main():
    """
    directions:
        - scan all open issues in the repo
        - if "[Dd]uplicates: <org>/<repo>#XXX exists in PR body:
            - check if that issue or PR is closed
            - if so, close this issue
    """
    org, repo = os.environ["INPUT_ORGREPO"].split("/")

    print(f"::set-output name=orgRepo::{org}/{repo}")

    api_token = os.environ["INPUT_API_TOKEN"]

    gh_headers = ghip.get_github_headers(api_token)

    for issue in ghip.get_open_issues(gh_headers, org, repo):
        iurl = issue["html_url"]
        print(f"::set-output name=issueChecking::{iurl}")

        linked_issue_info = ghip.get_linked_info(issue)

        if linked_issue_info is not None:
            linked_status = ghip.get_linked_status(
                gh_headers, linked_issue_info
            )
            print(f"::set-output name=linkedIssueStatus::{linked_status}")

            if linked_status == "closed":
                ghip.close_issue(gh_headers, issue)


if __name__ == "__main__":
    main()
