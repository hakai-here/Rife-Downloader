import asyncio
import os
import gzip
import re
from src.constants import DATABASE, TMP_PACKAGE_DIR
from src.db.connection import Connection
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
spinner = Spinner(
    'dots2', text='[bold] Updating the information to the Database')
panel = Panel(spinner)
keys = ["Package", "Source", "Version",
        "Depends", 'Description', "Size", "SHA256", "MD5sum", "Priority", "Filename"]


class Extractor:
    def __init__(self, data):
        self.data = data
        try:
            os.remove(DATABASE)
        except FileNotFoundError:
            pass
        with Live(panel, refresh_per_second=10):
            self.database = Connection()
            self.database.create_table()
            asyncio.run(self.extract())
            self.database.__exit__()

    async def extract(self):
        task = []
        for package in self.data:
            task.append(asyncio.ensure_future(
                self.extract_package(package["filename"], package["source"], package["repository"])))
        await asyncio.gather(*task)

    async def extract_package(self, filename, source,repository):
        getpack = {}
        with gzip.open(os.path.join(TMP_PACKAGE_DIR, filename), 'rb') as f:
            for line in f:
                key, value = line.decode().strip().partition(':')[::2]
                if key in keys and value:
                    if key == "Filename":
                        value = "/".join([source.strip(), value.strip()])
                    getpack[key] = re.sub(r'\([^)]*\)',
                                          "", value.strip()) if value else None
                elif key == "":
                    getpack["Repository"] = repository.strip()
                    self.database.cursor.execute(
                        f"INSERT INTO packages ({ ','.join(getpack.keys())}) VALUES ({ ', '.join('?' * len(getpack.keys()))})", [getpack[i] for i in getpack.keys()])