import os
from sys import exit
from src.parse import __main__



if __name__ == "__main__":
    try:
        __main__()
    except KeyboardInterrupt:
        print("[-] Exiting...")
        exit(0)    
    except FileNotFoundError as e:
        print(e)
        exit(1)
    except PermissionError:
        print("[-] PermissionError: Please run as root")
        exit(1)
    finally:
        os.system("pyclean")