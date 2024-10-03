# modules/system_metrics.py

import asyncio
import psutil

class SystemMetrics:
    def __init__(self):
        self.cpu_usage = 0
        self.memory_usage = 0
        self.disk_usage = 0

    async def fetch_metrics(self):
        self.cpu_usage = psutil.cpu_percent(interval=1)
        self.memory_usage = psutil.virtual_memory().percent
        self.disk_usage = psutil.disk_usage('/').percent

    async def update(self):
        await self.fetch_metrics()
