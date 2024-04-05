#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers."""

from fabric.api import run, local, env, put
import os.path
from datetime import datetime

env.hosts = ['54.159.27.57', '3.89.155.109']


def do_pack():
    """generates a .tgz archive from contents of the web_static folder"""
    d = datetime.utcnow()
    file = f"versions/web_static_{d.year}{d.month}{d.day}{d.hour}\
            {d.minute}{d.second}.tgz"
    if os.path.isdir("versions") is False:
        ret = local("mkdir -p versions")
        if ret.failed is True:
            return None
    file_ret = local(f"tar -cvzf {file} web_static")
    if file_ret.failed is True:
        return None
    return file


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


def deploy():
    """Creates and distributes an archive to web servers."""
    fp = do_pack()
    if fp is None:
        return False
    return do_deploy(fp)
