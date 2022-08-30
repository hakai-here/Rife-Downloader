import os
import asyncio
import aiohttp
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    DownloadColumn,
    TransferSpeedColumn
)
from rich.panel import Panel
from rich.live import Live
from rich.style import Style
bar_front = Style(color="blue")
bar_back = Style(color="red")


class Downloader:
    def __init__(self, package, path, task):
        self.package = package
        self.path = path
        self.download_progress = Progress(
            SpinnerColumn('dots2'),
            "{task.description}",
            BarColumn(bar_width=None, style=bar_back,
                      complete_style=bar_front, finished_style=bar_front),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            "•",
            TimeRemainingColumn(),
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),)
        self.panel = Panel(self.download_progress,
                           expand=True, title=f"Downloading {task}",padding=(1,1),title_align="right")
        asyncio.run(self.__init__download())

    def name(self, url, name):
        if "Package.gz" in url:
            return str(name)
        return str(url.split("/")[-1])

    async def __init__download(self):
        with Live(self.panel, refresh_per_second=10):
            async with aiohttp.ClientSession() as session:
                task = []
                for i in self.package:
                    task.append(asyncio.ensure_future(
                        self.__download_file(session, i['url'], i['package'],i['filename'])))
                await asyncio.gather(*task)

    async def __download_file(self, session, url,package,filename):
        async with session.get(url) as resp:
            if resp.status == 200:
                job = self.download_progress.add_task(
                    f"{package}", total=resp.content_length)
                with open(os.path.join(self.path,filename), "wb") as f:
                    async for data in resp.content.iter_chunked(1024):
                        f.write(data)
                        self.download_progress.advance(job, advance=len(data))
