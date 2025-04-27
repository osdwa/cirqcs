from pathlib import Path
from typing import Optional


def short_path(file_path, base_path):
    try:
        return str(Path(file_path).relative_to(base_path))
    except ValueError:
        return file_path


class Remark:
    def __init__(self, r_file: str, r_type: str, r_type_short: str, content: str):
        self.r_file = r_file
        self.r_type = r_type
        self.r_type_short = r_type_short
        self.content = content

    def get_as_text(self, show_file: bool, show_type: bool):
        text = self.content
        if show_type:
            text = f"{self.r_type_short}: {text}"
        if show_file:
            text = f"{self.r_file}: {text}"
        return text


class GeneralRemark:
    def __init__(self):
        self.general_rem = ""
        self.files: dict[str, list[Remark]] = {}

    def set_general_remark(self, general_rem: str):
        self.general_rem = general_rem

    def add_remark(self, file_name: str, r_type: str, r_type_short: str, r_content: str):
        remark = Remark(file_name, r_type, r_type_short, r_content)
        if file_name in self.files:
            self.files[file_name].append(remark)
        else:
            self.files[file_name] = [remark]

    def get_files(self, file_name: Optional[str]):
        if file_name:
            return [self.files[file_name]]
        else:
            return list(self.files.values())

    def get_all_r_types(self, file_name: Optional[str] = None):
        all_types = set()

        for file in self.get_files(file_name):
            for remark in file:
                all_types.add(remark.r_type)

        return sorted(all_types)

    def filtered(self, file_name: Optional[str] = None, r_type: Optional[str] = None):
        remarks: list[Remark] = []

        for file in self.get_files(file_name):
            if r_type:
                for remark in file:
                    if remark.r_type == r_type:
                        remarks.append(remark)
            else:
                remarks.extend(file)

        return remarks
