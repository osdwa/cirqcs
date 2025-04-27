from flake8.api import legacy as flake8
from remarks import GeneralRemark, short_path


def rate_files(paths, base_path, splash) -> GeneralRemark:
    splash.set_status("Running flake8...")
    style_guide = flake8.get_style_guide(quiet=2)
    report_obj = style_guide.check_files(paths)

    general_rem = f"Total: {report_obj.total_errors}"

    remarks = GeneralRemark()
    remarks.set_general_remark(general_rem)

    for report in report_obj._application.file_checker_manager.results:
        for remark in report[1]:
            file_name = short_path(report[0], base_path)
            r_type = remark[0]
            content = f"{remark[1]}:{remark[2]}: {remark[3]}"
            remarks.add_remark(file_name, r_type, r_type, content)

    return remarks
