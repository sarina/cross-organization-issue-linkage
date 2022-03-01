# Cross organization issue linkage action

## Usage

This is a simplistic action that allows you to link issues in your
user- or org- repos to issues present outside of your user or org
domain. The action is meant to be run on cron, and will simply sync
your open issues with the other project's, closing your issues if
the other project has closed its issue. If the other project has
re-opened its issue, this script will not find them. Iterating
over both opened and closed issues may be expensive for many repos.

Potential future work may include:

* Copying over comments from the other org's ticket to this one.
* Making a comment on the other org's ticket if it is still open
  while this one is closed (would possibly require a new action,
  to be run on PR close)
* Scripting over the beta API, so that project status changes are
  reflected on both boards as well as open/close status


### Example workflow

This workflow runs at minute 0 past every 2nd hour from 14
through 23 on every day-of-week from Monday through Friday
(GitHub runs on UTC, so these values work for EST)

```yaml
name: Sync Cross-Org Issues
on:
  schedule
    - cron: '0 14/2 * * 1-5'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action

      uses: sarina/cross-organization-issue-linkage@master

      with:
        API_TOKEN: ${{ secrets.API_TOKEN }}
        ORGREPO: ${{ github.repository }}
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `API_TOKEN`  | A token with read/write access to this repository (can close issues) and public read access (to get status of the other org's issues)    |
| `ORGREPO` | The org/repo where you are running the Action from. Present in the global envar `github.repository`    |

## Notes

See [GitHub's cron
documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
and/or [Crontab Guru](https://crontab.guru/) for help with cron syntax.

Note that the user, bot, or GitHub app who is associated with `API_TOKEN` will
be the user displayed on the PR that closes it. If you use a bot/app, be sure it
has an appropriate name that makes it clear what it is doing.