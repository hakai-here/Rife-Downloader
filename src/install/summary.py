from rich import print as _print
from rich.table import Table
from rich.box import SIMPLE_HEAD


color = ["white","cyan", "blue","yellow","green"]

def size(size):
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return "{:.2f} {}B".format(size, power_labels[n])


class Summary:
    def __init__(self,list:dict):
        self.grid = Table(expand=True,box=SIMPLE_HEAD,show_footer=True)
        for i in ["Package", "Version", "Repository", "Size","Priority"]:
            self.grid.add_column(i,style=color.pop())
        
        for i in list:
            self.grid.add_row(i["package"],i["version"],i["repository"].split(" ")[0],size(i["size"]),i["priority"])
        
    def ask(self):
        _print(self.grid)
        return input("Do you want to install these packages? [ Y/n ] ").lower() == "y"