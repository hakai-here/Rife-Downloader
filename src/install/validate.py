from pydpkg import Dpkg
from src.constants import TMP_DOWNLOAD_DIR
import os 

def signature(package):
    for i in package:
        dp = Dpkg(os.path.join(TMP_DOWNLOAD_DIR, str(i['url'].split('/')[-1]).strip()))
        if not (dp.sha256 == i['SHA256'] and dp.md5 == i['MD5sum']):
            raise SystemExit(f"{i['Package']} Package signature is not valid")
    print("[+] All Package signatures are valid")