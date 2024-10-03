# modules/issues_prs.py

import asyncio
from aiohttp import ClientSession

class IssuesPRs:
    def __init__(self, github_token, owner, repo):
        self.github_token = github_token
        self.owner = owner
        self.repo = repo
        self.open_issues = []
        self.open_prs = []

    async def fetch_open_issues(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues?state=open&labels=&per_page=5"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Filter out pull requests
                    self.open_issues = [issue for issue in data if 'pull_request' not in issue]
                    self.open_issues = [f"#{issue['number']} - {issue['title']}" for issue in self.open_issues[:5]]
                else:
                    self.open_issues = [f"Error {response.status}"]

    async def fetch_open_prs(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls?state=open&per_page=5"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.open_prs = [f"#{pr['number']} - {pr['title']} by {pr['user']['login']}" for pr in data[:5]]
                else:
                    self.open_prs = [f"Error {response.status}"]

    async def update(self):
        await asyncio.gather(
            self.fetch_open_issues(),
            self.fetch_open_prs()
        )
