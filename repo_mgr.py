import os
import re
import stat
import shutil
import tempfile
import subprocess
import tkinter.messagebox as mb
from gui import SplashScreen, app_name


def get_temp_path(git_url: str):
    only_alpha = re.sub("[^a-zA-Z]", "-", git_url)
    return os.path.join(tempfile.gettempdir(), f"git_clone_{only_alpha[:255]}")


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def git_clone(git_url: str):
    temp_path = get_temp_path(git_url)
    command = ["git", "clone", git_url, temp_path]
    print("Cloning to:", temp_path)

    try:
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path, onerror=on_rm_error)

        process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)
        _, stderr = process.communicate()

        if process.returncode == 0:
            return temp_path
        else:
            mb.showerror("Git Error", stderr)

    except FileNotFoundError:
        mb.showerror(app_name, "You have to install git to do this!")

    return None


def recv_repo(path: str | None, splash: SplashScreen):
    splash.set_status("Receiving repository...")

    if not path:
        return None

    elif path.startswith("https://"):
        return git_clone(path)

    elif os.path.exists(path):
        return path

    else:
        mb.showerror(app_name, f"'{path}' does not exist!")
        return None
