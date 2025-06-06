from repo_mgr import recv_repo
from eval_main import rate_repo
from gui import PathChooser, SplashScreen, Application, app_name


if __name__ == "__main__":
    repo_url = PathChooser(None, title=app_name).result

    splash = SplashScreen()
    data_path = recv_repo(repo_url, splash)

    if data_path:
        report = rate_repo(data_path, splash)
    else:
        report = {}

    splash.destroy()
    app = Application()
    app.update_content(report, repo_url)
    app.mainloop()
