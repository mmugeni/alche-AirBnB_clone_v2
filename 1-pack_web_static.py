#!/usr/bin/python3
"""
Fabric script to pack web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from web_static
    Returns path or None
    """
    try:
        if not os.path.exists("versions"):
            os.mkdir("versions")

        filename = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S")
        )

        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None
