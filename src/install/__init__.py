from src.constants import TMP_DOWNLOAD_DIR
from src.db.connection import Connection
from rich.panel import Panel
from os import devnull
from rich.live import Live
from rich.progress import (Progress, SpinnerColumn, TimeElapsedColumn)
from subprocess import call
from shutil import which
from src.utils.downloader import Downloader
from src.install.summary import Summary
from src.install.validate import signature as Validate
DEVNULL = open(devnull, 'w')


class Install:
    def __init__(self, args):
        if len(args) == 0:
            raise FileNotFoundError("[-] Installation cantidate not found")
        self.progress = Progress(
            SpinnerColumn(style="bold"),
            "{task.description} : ",
            TimeElapsedColumn(),
        )
        self.panel = Panel(self.progress)
        self.args = args
        self.database = Connection()
        self.packages = []
        self.dependency = []
        self.not_found = []
        self.search()
        self.progress.add_task(description="Calculating dependencies",)
        with Live(self.panel, refresh_per_second=10):
            self.dependency_calculate()
        
        self.summary = Summary(self.packages)
        if self.summary.ask():
            Downloader(self.packages,TMP_DOWNLOAD_DIR, "Package Files")
            Validate(self.packages)
        else:
            raise SystemExit("[-] Aborted installation")

    def conflit(self, data):
        message = "Conflict : {} : ".format(data[0][0])
        for index, i in enumerate(data):
            message += f"({index+1}) {i[2]} V {i[1]}  "
        return data[int(input(message))-1]

    def is_installed(self, package):
        a = call(["dpkg", "-s", package], stdout=DEVNULL, stderr=DEVNULL) == 0
        b = which(package) is not None
        return a or b

    def write_value(self, data):
        value = {
            "package": data[0],
            "version": data[1],
            "repository": data[2],
            "depends": data[3],
            "size": data[4],
            "SHA256": data[5],
            "MD5sum": data[6],
            "url": data[7],
            "priority": data[8],
            "filename": data[7].split("/")[-1]
        }
        if value not in self.packages:
            self.packages.append(value)

    def dependency_calculate(self):
        for package in self.packages:
            depends = []
            repo = package["repository"].split(" ")[0].strip()
            # self.check_key(repo)
            for dependency in package["depends"].split(","):
                # These are temporary solutions and needed to be changed (issue found : wpscan)
                dependency = dependency.split(':')[0]
                # These are temporary solutions and needed to be changed (issue found : wpscan)
                dependency = dependency.split('|')[0].strip()
                if dependency not in depends and not self.is_installed(dependency) and dependency not in self.dependency:
                    depends.append(dependency.strip())
                    self.dependency.append(dependency.strip())

            for dependency in depends:
                self.search_d(dependency, repo)

    def search_d(self, package, repo):
        data = self.database.search_by_dep(package, repo)
        if len(data) == 0:
            self.not_found.append(package)
            return
        elif len(data) > 1:
            data = data[0]
        else:
            data = data[0]
        self.write_value(data)

    def search(self):
        for package in self.args:
            if not self.is_installed(package):
                data = self.database.search(package)
                if len(data) == 0:
                    raise FileNotFoundError("[-] Package not found {package}")
                elif len(data) > 1:
                    data = self.conflit(data)
                else:
                    data = data[0]
                self.write_value(data)
