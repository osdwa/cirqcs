from pylint.lint import Run
from pylint.reporters import BaseReporter
from remarks import GeneralRemark, short_path


class CollectingReporter(BaseReporter):
    def __init__(self, remarks, base_path):
        super().__init__()
        self.remarks = remarks
        self.base_path = base_path

    def handle_message(self, msg):
        f_name = short_path(msg.path, self.base_path)
        r_type = str(msg.msg_id)
        r_type_long = f"{msg.msg_id}: {msg.symbol}"
        content = f"{msg.line}:{msg.column}: {msg.msg}"
        self.remarks.add_remark(f_name, r_type, r_type_long, content)

    def display_messages(self, layout):
        pass

    def _display(self, layout):
        pass


def rate_files(paths, base_path, splash) -> GeneralRemark:
    splash.set_status("Running pylint...")

    remarks = GeneralRemark()
    reporter = CollectingReporter(remarks, base_path)
    Run(paths, reporter=reporter, exit=False)

    gen_remark = f"Score: {reporter.linter.stats.global_note:.2f}/10"
    remarks.set_general_remark(gen_remark)

    return remarks
