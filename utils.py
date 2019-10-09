__DEBUG = False

NEW_PART = "=" * 80


def debug(*args):
	if __DEBUG:
		print("[DEBUG]", *args)


def set_debug(bool):
	global __DEBUG
	__DEBUG = bool


def new_part(*args):
	print()
	print(NEW_PART)
	print(*args)
