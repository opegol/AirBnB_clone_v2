#!/usr/bin/python3
"""Fabric script to generate a .tgz archive
    from the contents of the web_static folder.
"""

from fabric.api import local
import os.path
from datetime import datetime


def do_pack():
    """generates a .tgz archive from contents of the web_static folder"""
    d = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(d.year,
                                                         d.month,
                                                         d.day,
                                                         d.hour,
                                                         d.minute,
                                                         d.second)
    # file = f"versions/web_static_\
    #        {d.year}{d.month}{d.day}{d.hour}{d.minute}{d.second}.tgz"
    if os.path.isdir("versions") is False:
        ret = local("mkdir -p versions")
        if ret.failed is True:
            return None
    file_ret = local(f"tar -cvzf {file} web_static")
    if file_ret.failed is True:
        return None
    return file
