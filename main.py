from eval_main import rate_repo
from threading import Thread
from gui import PathChooser, SplashScreen, Application


if __name__ == "__main__":
    path = PathChooser(None).result
    if not path:
        exit()

    report = {}
    splash = SplashScreen()
    rate_repo(report, path, splash)

    app = Application(report, path)
    app.mainloop()
