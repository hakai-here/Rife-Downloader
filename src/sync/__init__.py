from subprocess import check_output
from src.constants import SOURCELIST,TMP_PACKAGE_DIR
from src.utils.downloader import Downloader
from src.sync.Extractor import Extractor

def arch():
    return check_output('dpkg --print-architecture', shell=True).decode('utf-8').strip()


def Sync():
    updatelist = []
    arc = arch()
    with open(SOURCELIST, "r") as f:
        for line in f.readlines():
            sp = line.split()
            url = sp[1:-3]
            for i in sp[-3:]:
                updatelist.append({
                    "package": f"{url[1]}-{i}",
                    "filename": f"{url[1]}-{i}-Packages.gz",
                    "url": "/".join([url[0], 'dists', url[1], i, f"binary-{arc}", 'Packages.gz']),
                    "source": url[0],
                    "repository": f'{url[1]} {i}'
                })
    Downloader(updatelist,TMP_PACKAGE_DIR, "Package Files")
    Extractor(updatelist)