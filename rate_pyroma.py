import logging
from pyroma import projectdata, ratings
from build._exceptions import BuildException
from remarks import GeneralRemark

logging.basicConfig(level=logging.WARNING, force=True)


def rate_repo(repo_path, splash) -> GeneralRemark:
    splash.set_status("Running pyroma...")
    remarks = GeneralRemark()

    try:
        data = projectdata.get_data(repo_path)
    except BuildException:
        remarks.set_general_remark("This source does not appear to be a Python project: no pyproject.toml or setup.py")
        return remarks

    rating = ratings.rate(data)
    remarks.set_general_remark(f"Score: {rating[0]}/10 - {ratings.LEVELS[rating[0]]}")
    for issue in rating[1]:
        remarks.add_remark(".", "", "N/A", str(issue))

    return remarks
