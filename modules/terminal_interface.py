# modules/terminal_interface.py

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.group import Group  # Import Group
import asyncio

class TerminalInterface:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # Define the layout
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )

        self.layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1)
        )

    def build_header(self):
        return Panel(Align.center("[bold cyan]DevDash – Developer Dashboard[/bold cyan]", vertical="middle"))

    def build_footer(self):
        return Panel(Align.center("Press Ctrl+C to exit", vertical="middle"))

    def build_git_panel(self, git_insights):
        table = Table(title="Git Insights", expand=True)
        table.add_column("Current Branch", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Recent Commits", style="magenta")

        recent_commits = "\n".join(git_insights.recent_commits) if git_insights.recent_commits else "N/A"

        table.add_row(
            git_insights.current_branch,
            git_insights.repo_status,
            recent_commits
        )

        return Panel(table, border_style="cyan")

    def build_ci_panel(self, ci_status):
        table = Table(title="CI Status", expand=True)
        table.add_column("Latest Run", style="yellow")
        table.add_row(ci_status.latest_build_status)
        return Panel(table, border_style="yellow")

    def build_issues_prs_panel(self, issues_prs):
        table = Table(title="Issues & PRs", expand=True)
        table.add_column("Open Issues", style="red")
        table.add_column("Open PRs", style="blue")

        open_issues = "\n".join(issues_prs.open_issues) if issues_prs.open_issues else "N/A"
        open_prs = "\n".join(issues_prs.open_prs) if issues_prs.open_prs else "N/A"

        table.add_row(
            open_issues,
            open_prs
        )

        return Panel(table, border_style="red")

    def build_system_metrics_panel(self, system_metrics):
        table = Table(title="System Metrics", expand=True)
        table.add_column("CPU Usage", style="green")
        table.add_column("Memory Usage", style="green")
        table.add_column("Disk Usage", style="green")

        table.add_row(
            f"{system_metrics.cpu_usage}%",
            f"{system_metrics.memory_usage}%",
            f"{system_metrics.disk_usage}%"
        )

        return Panel(table, border_style="green")

    def assemble_layout(self, git_insights, ci_status, issues_prs, system_metrics):
        self.layout["header"].update(self.build_header())
        self.layout["footer"].update(self.build_footer())

        self.layout["main"]["left"].update(self.build_git_panel(git_insights))
        
        # Use Group to combine multiple panels vertically
        right_group = Group(
            self.build_ci_panel(ci_status),
            self.build_issues_prs_panel(issues_prs),
            self.build_system_metrics_panel(system_metrics)
        )
        self.layout["main"]["right"].update(right_group)

        return self.layout
