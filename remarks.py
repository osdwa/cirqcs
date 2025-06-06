from pathlib import Path
from typing import Optional


def short_path(file_path, base_path):
    try:
        return str(Path(file_path).relative_to(base_path))
    except ValueError:
        return file_path


class Remark:
    def __init__(self, r_file: str, r_type: str, r_type_long: str, content: str):
        self.r_file = r_file
        self.r_type = r_type
        self.r_type_long = r_type_long
        self.content = content

    def get_as_text(self, show_file: bool, show_type: bool):
        text = self.content
        if show_type:
            text = f"{self.r_type}: {text}"
        if show_file:
            text = f"{self.r_file}: {text}"
        return text


class GeneralRemark:
    def __init__(self):
        self.general_rem = ""
        self.remarks: list[Remark] = []
        self.files = set()

    def set_general_remark(self, general_rem: str):
        self.general_rem = general_rem

    def add_remark(self, file_name: str, r_type: str, r_type_long: str, r_content: str):
        remark = Remark(file_name, r_type, r_type_long, r_content)
        self.files.add(file_name)
        self.remarks.append(remark)

    def get_remarks_for_file(self, file_name: Optional[str]):
        if file_name:
            return [remark for remark in self.remarks if remark.r_file == file_name]
        else:
            return self.remarks

    def get_all_r_long_types(self, file_name: Optional[str] = None):
        all_types = set()

        for remark in self.get_remarks_for_file(file_name):
            all_types.add(remark.r_type_long)

        return sorted(all_types)

    def filtered(self, file_name: Optional[str] = None, r_type_long: Optional[str] = None):
        remarks: list[Remark] = []

        for remark in self.remarks:
            name_match = (not file_name) or remark.r_file == file_name
            type_match = (not r_type_long) or remark.r_type_long == r_type_long
            if name_match and type_match:
                remarks.append(remark)

        return remarks
