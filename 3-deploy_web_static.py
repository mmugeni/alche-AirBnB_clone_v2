#!/usr/bin/python3
"""
Full deployment script
"""

from fabric.api import env, local, run, put
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """
    Packs web_static into archive
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


def do_deploy(archive_path):
    """
    Deploys archive
    """
    if not os.path.exists(archive_path):
        return False

    filename = archive_path.split("/")[-1]
    folder = "/data/web_static/releases/" + filename.replace(".tgz", "")

    try:
        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        return True
    except Exception:
        return False


def deploy():
    """
    Full deployment process
    """
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)
