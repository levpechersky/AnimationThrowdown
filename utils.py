
__DEBUG = True


def debug(*args):
    if __DEBUG:
        print(*args)


def set_debug(bool):
    global __DEBUG
    __DEBUG = bool
