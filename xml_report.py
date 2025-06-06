import base64
import xml.etree.ElementTree as Et
from xml.dom import minidom
from remarks import GeneralRemark, Remark


def to_b64(string):
    str_bytes = str(string).encode("utf-8")
    b64_bytes = base64.b64encode(str_bytes)
    return b64_bytes.decode("ansi")


def from_b64(b64_string):
    b64_bytes = b64_string.encode("ansi")
    str_bytes = base64.b64decode(b64_bytes)
    return str_bytes.decode("utf-8")


def report_to_xml(path: str, label: str, report: dict[str, GeneralRemark]):
    xml_root = Et.Element("all_remarks")
    xml_root.set("label", to_b64(label))

    for evaluator, gen_remark in report.items():
        xml_gen_remark = Et.SubElement(xml_root, "gen_remark")
        xml_gen_remark.set("evaluator", to_b64(evaluator))
        xml_gen_remark.set("comment", to_b64(gen_remark.general_rem))

        grouped: dict[str, dict[tuple[str, str], list[Remark]]] = {}
        for remark in gen_remark.remarks:
            if remark.r_file not in grouped:
                grouped[remark.r_file] = {}
            issue_t = (remark.r_type, remark.r_type_long)
            if issue_t not in grouped[remark.r_file]:
                grouped[remark.r_file][issue_t] = []
            grouped[remark.r_file][issue_t].append(remark)

        for file, issues in grouped.items():
            xml_file = Et.SubElement(xml_gen_remark, "file")
            xml_file.set("name", to_b64(file))

            for issue, remarks in issues.items():
                xml_issue = Et.SubElement(xml_file, "issue")
                xml_issue.set("type", to_b64(issue[0]))
                xml_issue.set("type_long", to_b64(issue[1]))

                for remark in remarks:
                    xml_remark = Et.SubElement(xml_issue, "remark")
                    xml_remark.text = to_b64(remark.content)

    file = open(path, "w", encoding="ansi")
    parsed = minidom.parseString(Et.tostring(xml_root))
    file.write(parsed.toprettyxml(indent="\t"))
    file.close()


def xml_to_report(path: str):
    xml_root = Et.parse(path).getroot()
    label = from_b64(xml_root.get("label"))
    report = {}

    for xml_gen_remark in xml_root.findall("gen_remark"):
        evaluator = from_b64(xml_gen_remark.get("evaluator"))
        comment = from_b64(xml_gen_remark.get("comment"))

        gen_remark = GeneralRemark()
        gen_remark.set_general_remark(comment)
        report[evaluator] = gen_remark

        for xml_file in xml_gen_remark.findall("file"):
            r_file = from_b64(xml_file.get("name"))

            for xml_issue in xml_file.findall("issue"):
                r_type = from_b64(xml_issue.get("type"))
                r_type_long = from_b64(xml_issue.get("type_long"))

                for xml_remark in xml_issue.findall("remark"):
                    content = from_b64(xml_remark.text)
                    gen_remark.add_remark(r_file, r_type, r_type_long, content)

    return label, report
