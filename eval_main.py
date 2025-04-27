import os
import rate_flake8
import rate_pylint
import rate_bandit
import rate_vulture


def find_files(path: str, filetype: str, exclude_dirs: list[str]):
    files = []

    for dirpath, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for filename in filenames:
            if filename.endswith(filetype):
                full_path = os.path.join(dirpath, filename)
                files.append(os.path.abspath(full_path))

    return files


def rate_repo(report, path, splash):
    exclude_dirs = ["venv", ".venv", ".git", "__pycache__"]
    files = find_files(path, ".py", exclude_dirs)

    report["flake8"] = rate_flake8.rate_files(files, path, splash)
    report["pylint"] = rate_pylint.rate_files(files, path, splash)
    report["bandit"] = rate_bandit.rate_files(files, path, splash)
    report["vulture"] = rate_vulture.rate_files(files, path, splash)

    splash.destroy()
