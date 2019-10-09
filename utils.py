__DEBUG = False
__NEW_PART = "=" * 80


USER_WEIGHTS_FILE = 'weights_user.py'


def debug(*args):
	if __DEBUG:
		print("[DEBUG]", *args)


def set_debug(bool):
	global __DEBUG
	__DEBUG = bool


def new_part(*args):
	print()
	print(__NEW_PART)
	print(*args)
