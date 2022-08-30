from distutils.debug import DEBUG
import os
APP = "rife"
# BASE_DIR = os.path.join("/","opt", APP)
BASE_DIR = os.path.join("opt", APP)
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "package.db")
APP_DIR = os.path.join(BASE_DIR, "app")
TMP_PACKAGE_DIR = os.path.join("/tmp",APP,"packages")
TMP_DOWNLOAD_DIR = os.path.join("/tmp",APP,"download")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
SOURCELIST = os.path.join(CONFIG_DIR, "sources.list")
DEFALUT_MIRROR = "deb https://deb.parrot.sh/parrot/ parrot main contrib non-free"

def create_dirs():
        for dir in [BASE_DIR, DATA_DIR, APP_DIR, CONFIG_DIR, TMP_PACKAGE_DIR,TMP_DOWNLOAD_DIR]:

            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                except PermissionError:
                    print(f"{dir} is not writable")
                    exit(1)
        if not os.path.exists(SOURCELIST):
            with open(SOURCELIST, "w") as f:
                 f.write(DEFALUT_MIRROR)
    
