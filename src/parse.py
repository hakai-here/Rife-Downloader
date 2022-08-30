import click 
from src.constants import create_dirs
from src.sync import Sync
from src.install import Install
from src.utils.needroot import needroot
from subprocess import call
from src.constants import SOURCELIST
from src.search import Search

@click.group()
def __main__():
    create_dirs()

@__main__.command("edit", help="Edit the sourcelist")
def edit():
    call(["nano", SOURCELIST])


@__main__.command("sync", help="Sync the database")
@needroot
def sync():
    Sync()

@__main__.command("search", help="Search for packages")
@click.argument("query")
def search(query):
    Search(query)

@__main__.command("install", help="Install packages")
@click.argument("packages", nargs=-1)
@needroot
def install(packages):
    Install(packages)