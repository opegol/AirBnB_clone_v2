#!/usr/bin/python3
"""Fabric script  to delete out-of-date archives."""

from fabric.api import *
import os

env.hosts = ['54.159.27.57', '3.89.155.109']


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): The number of the archives to keep.

    If number is 0 or 1, it keeps only the most recent archive. If
    number is 2, it keeps the most recent and second most recent archives,
    etc.
    """
    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    acvs = sorted(os.listdir("versions"))
    [acvs.pop() for i in range(number)]
    with lcd("versions"):
        for a in acvs:
            local(f"rm ./{a}")

    with cd("/data/web_static/releases"):
        acvs = sudo("ls -tr").split()
        acvs = [a for a in acvs if a.find("web_static") != -1]
        [acvs.pop() for i in range(number)]
        for a in acvs:
            run(f"rm -rf ./{a}")
