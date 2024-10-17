"""Utility functions for zipcodelib"""

import sys
import os
from time import time
from os.path import exists, join, dirname

import requests


def download(
    url,
    fname=None,
    use_cached=True,
    cache_dir=join(dirname(__file__), "cache"),
    progress=sys.stderr,
    width=65,
):
    """Download a remote URL to a local file

    Optional progress bar and caching of downloads.

    - url:   required resource name
    - fname: optional local file to save resource,
             defaults to last component of URL
    - use_cached: optional boolean;
             skip downloading if local copy is already
    - cache_dir:
             directory where local file is saved
    - progress: optional device to show progress bar or False
    - width: default 65, display width of progress bar

    Returns the filename of the saved local resource.
    """
    start = time()

    if not progress:
        progress = open(os.devnull, "a")

    print("Downloading", url)

    if fname is None:
        fname = url.split("/")[-1]
    fname = join(cache_dir, fname)

    response = requests.get(url, stream=True)
    total = response.headers.get("content-length")
    if total is not None and use_cached and exists(fname):
        total = int(total)
        if total == os.stat(fname).st_size:
            print("Using cached file", fname)
            return fname

    with open(fname, "wb") as f:
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(
                chunk_size=max(int(total / 1000), 1024 * 1024)
            ):
                downloaded += len(data)
                f.write(data)
                done = int(width * downloaded / total)
                progress.write(
                    "\r{}{}| {:.0e}B".format("•" * done, " " * (width - done), total)
                )
                progress.flush()

    progress.write("\n")
    print("Saved", fname)
    print("Completed in {:,.1f} seconds".format(time() - start))
    return fname
