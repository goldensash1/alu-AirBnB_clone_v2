#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to your web servers"""

import os
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists

env.hosts = ['44.201.221.252', '54.209.180.94']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """Create a .tgz archive from the web_static folder."""
    try:
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(time_stamp)
        result = local("tar -cvzf {} web_static".format(archive_path), capture=True)
        if result.failed:
            return None
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute the archive to web servers and deploy it."""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path_name = "/data/web_static/releases/" + name
        
        # Upload the archive to /tmp/
        put(archive_path, "/tmp/")
        
        # Create target directory
        run("mkdir -p {}/".format(path_name))
        
        # Uncompress the archive
        run("tar -xzf /tmp/{} -C {}/".format(file_name, path_name))
        
        # Remove the archive
        run("rm /tmp/{}".format(file_name))
        
        # Move contents and remove web_static dir
        run("mv {}/web_static/* {}/".format(path_name, path_name))
        run("rm -rf {}/web_static".format(path_name))
        
        # Remove previous symlink and create new one
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(path_name))
        
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive")
        return False

    return do_deploy(archive_path)
