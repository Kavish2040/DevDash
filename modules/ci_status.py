# modules/ci_status.py

import asyncio
from aiohttp import ClientSession
from plyer import notification

class CIStatus:
    def __init__(self, github_token, owner, repo):
        self.github_token = github_token
        self.owner = owner
        self.repo = repo
        self.latest_build_status = "N/A"
        self.previous_build_status = None  # To track status changes

    async def fetch_latest_build_status(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/actions/runs?per_page=1"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['workflow_runs']:
                        run = data['workflow_runs'][0]
                        status = run['conclusion']
                        if status:
                            self.latest_build_status = status.capitalize()
                        else:
                            self.latest_build_status = run['status'].capitalize()
                    else:
                        self.latest_build_status = "No Runs"
                else:
                    self.latest_build_status = f"Error {response.status}"

    async def check_and_notify(self):
        await self.fetch_latest_build_status()
        if self.previous_build_status != self.latest_build_status:
            self.previous_build_status = self.latest_build_status
            if self.latest_build_status.lower() == "failure":
                notification.notify(
                    title="CI Build Failure",
                    message=f"The latest build of {self.repo} has failed.",
                    timeout=5
                )
            elif self.latest_build_status.lower() == "success":
                notification.notify(
                    title="CI Build Success",
                    message=f"The latest build of {self.repo} was successful.",
                    timeout=5
                )

    async def update(self):
        await self.check_and_notify()
