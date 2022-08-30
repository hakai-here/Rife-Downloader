from src.db.connection import Connection
from subprocess import call
from os import devnull
from rich.tree import Tree
from rich import print
from shutil import which
DEVNULL = open(devnull, 'w')


class Search:
    def __init__(self,query):
        self.database = Connection()
        self.result = self.database.find(query)
        self.print()
        
    def print(self):
        for i in self.result:
            tree = Tree(f"[bold green]{i[0]} [blue1]{i[1]}[yellow] {i[2]}")
            if(self.is_tool(i[0])):
                tree.add(
                    "Already Installed (Same or different Version)", style="bold")
            tree.add(i[3])
            print(tree)
            print()
            
    def is_tool(self, package):
        a = call(["dpkg", "-s", package], stdout=DEVNULL, stderr=DEVNULL) == 0
        b = which(package) is not None
        return a or b