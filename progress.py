import sys


def progress_refresh(display_title, current_val, end_val, bar_length=30):
    percent = float(current_val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\r" + display_title + ": [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()