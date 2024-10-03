# modules/git_insights.py

import asyncio
from aiohttp import ClientSession
import os

class GitInsights:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.current_branch = "N/A"
        self.repo_status = "N/A"
        self.recent_commits = []

    async def fetch_current_branch(self):
        # Use Git command to get the current branch
        process = await asyncio.create_subprocess_shell(
            f'git -C {self.repo_path} rev-parse --abbrev-ref HEAD',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            self.current_branch = stdout.decode().strip()
        else:
            self.current_branch = "Error"

    async def fetch_repo_status(self):
        # Use Git command to get repository status
        process = await asyncio.create_subprocess_shell(
            f'git -C {self.repo_path} status --porcelain',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            changes = stdout.decode().strip()
            if changes:
                self.repo_status = f"Uncommitted Changes ({len(changes.splitlines())})"
            else:
                self.repo_status = "Clean"
        else:
            self.repo_status = "Error"

    async def fetch_recent_commits(self, count=5):
        # Use Git command to get recent commits
        process = await asyncio.create_subprocess_shell(
            f'git -C {self.repo_path} log -n {count} --pretty=format:"%h - %s (%an)"',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            self.recent_commits = stdout.decode().strip().split('\n')
        else:
            self.recent_commits = ["Error fetching commits"]

    async def update(self):
        await self.fetch_current_branch()
        await self.fetch_repo_status()
        await self.fetch_recent_commits()
