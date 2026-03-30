#!/usr/bin/python3
"""
Fabric script to deploy archive
"""

from fabric.api import env, run, put
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Deploys archive to web servers
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
