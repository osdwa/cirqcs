from bandit.core.config import BanditConfig
from bandit.core.manager import BanditManager
from remarks import GeneralRemark, short_path


def rate_files(paths, base_path, splash) -> GeneralRemark:
    splash.set_status("Running bandit...")

    config = BanditConfig()
    manager = BanditManager(config, "file", False)
    manager.discover_files(paths)
    manager.run_tests()

    remarks = GeneralRemark()
    remarks.set_general_remark("N/A")
    for issue in manager.results:
        file_name = short_path(issue.fname, base_path)
        r_type = str(issue.test_id)
        r_type_long = f"{issue.test_id}: {issue.test}"
        content = f"{issue.linerange}: {issue.text} (Severity: {issue.severity}, Confidence: {issue.confidence})"
        remarks.add_remark(file_name, r_type, r_type_long, content)

    return remarks
