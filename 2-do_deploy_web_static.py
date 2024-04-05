#!/usr/bin/python3
"""Fabfile distributes an archive to web servers."""

from fabric.api import run, env, put
import os.path

#env.hosts = ['3.89.155.109']
env.hosts = ['54.159.27.57', '3.89.155.109']


def do_deploy(archive_path):
    """Distributes an archive to web servers.

    Args:
        archive_path (str): path of the archive to distribute.
    Returns:
        False, if file does not exist at archive_path or
        if an error occurs and True, Otherwise.
    """

    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    n = file.split(".")[0]
    print(file)
    if put(archive_path, f"/tmp/{file}").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{n}/").failed is True:
        return False
    if run(f"mkdir -p /data/web_static/releases/{n}/").failed is True:
        return False
    if run(f"tar -xzf /tmp/{file} -C /data/web_static/releases/{n}/").\
            failed is True:
        return False
    if run("rm /tmp/{file}").failed is True:
        return False
    if run(f"mv /data/web_static/releases/{n}/web_static/* \
        /data/web_static/releases/{n}/").failed is True:
        return False
    if run(f"rm -rf /data/web_static/releases/{n}/web_static").failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run(f"ln -s /data/web_static/releases/{n}/ \
            /data/web_static/current").failed is True:
        return False
    return True
