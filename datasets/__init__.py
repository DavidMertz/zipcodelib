"""Magic module functions imported from various plugins in directory
"""
from glob import glob
from os.path import dirname, basename


def list_loaders():
    dir = dirname(__file__)
    loaders = glob(dir + "/load_*.py") + glob(dir + "/make_*.py")
    loaders = [basename(f).replace(".py", "") for f in loaders]
    return loaders


loaders = list_loaders()
for name in loaders:
    exec("from .%s import _run as %s" % (name, name))
del name


def load_all(use_cached=True):
    # Note that by sorting order, load_ functions will run before
    # make_ functions.  Therefore, using load_all() will assure
    # data needed by meta-loaders is available.
    for name in loaders:
        exec("%s(use_cached=%s)" % (name, use_cached))
