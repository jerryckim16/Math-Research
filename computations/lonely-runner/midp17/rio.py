"""Open a results file whether it is stored plain or gzipped (the committed results are gzipped)."""
import gzip
import os


def opn(path):
    if os.path.exists(path):
        return open(path)
    return gzip.open(path + ".gz", "rt")


def exists(path):
    return os.path.exists(path) or os.path.exists(path + ".gz")
