from vulture import Vulture
from remarks import GeneralRemark, short_path


def rate_files(paths, base_path, splash) -> GeneralRemark:
    splash.set_status("Running vulture...")
    v = Vulture()
    v.scavenge(paths)

    remarks = GeneralRemark()

    for item in v.get_unused_code():
        file = short_path(item.filename, base_path)
        lines = f"{item.first_lineno}-{item.last_lineno}" if item.size > 1 else str(item.first_lineno)
        message = f"{lines}: {item.message} ({item.confidence}% confidence)"
        remarks.add_remark(file, "", item.typ, message)

    remarks.set_general_remark(f"Total instances: {len(remarks.remarks)}")
    return remarks
