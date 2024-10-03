# main.py

import asyncio
import yaml
from rich.live import Live
from modules.git_insights import GitInsights
from modules.ci_status import CIStatus
from modules.issues_prs import IssuesPRs
from modules.system_metrics import SystemMetrics
from modules.terminal_interface import TerminalInterface

class DevDash:
    def __init__(self):
        self.load_config()
        self.setup_modules()
        self.terminal = TerminalInterface()

    def load_config(self):
        try:
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print("config.yaml not found. Please create one based on the template.")
            exit(1)

    def setup_modules(self):
        repo_path = self.config['git']['repo_path']
        github_token = self.config['github']['token']
        owner = self.config['github']['owner']
        repo = self.config['github']['repo']

        self.git_insights = GitInsights(repo_path)
        self.ci_status = CIStatus(github_token, owner, repo)
        self.issues_prs = IssuesPRs(github_token, owner, repo)
        self.system_metrics = SystemMetrics()

    async def update_modules(self):
        await asyncio.gather(
            self.git_insights.update(),
            self.ci_status.update(),
            self.issues_prs.update(),
            self.system_metrics.update()
        )

    async def refresh_dashboard(self, live):
        while True:
            await self.update_modules()
            layout = self.terminal.assemble_layout(
                self.git_insights,
                self.ci_status,
                self.issues_prs,
                self.system_metrics
            )
            live.update(layout)
            await asyncio.sleep(self.config.get('refresh_interval', 5))  # Default to 5 seconds

    def run(self):
        loop = asyncio.get_event_loop()
        with Live(console=self.terminal.console, refresh_per_second=4) as live:
            try:
                loop.run_until_complete(self.refresh_dashboard(live))
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    devdash = DevDash()
    devdash.run()
