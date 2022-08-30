from os import geteuid


def needroot(Function):
    def wrapper(*args, **kwargs):
        if geteuid() != 0:
            raise PermissionError("You need to be root to run this command")
        return Function(*args, **kwargs)
    return wrapper