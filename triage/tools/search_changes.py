from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, TextIO


@dataclass
class ChangeLog:
    id: str
    title: str
    text: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def iter_change_log(change_log_file: Path) -> list[ChangeLog]:
    with open(change_log_file, "r") as file_handle:
        lines = file_handle.readlines()
    for line_number, line in enumerate(lines):
        if line.startswith("## CHG"):
            yield parse_change_log_entry(line_number, lines)


def parse_change_log_entry(line_number: int, lines: list[str]) -> dict[str, Any]:
    code_title = lines[line_number].split("##")[1].strip()
    code, title = [x.strip() for x in code_title.split(" - ", maxsplit=1)]
    end_line_number = line_number + 1
    while end_line_number < len(lines) and not lines[end_line_number].startswith("---"):
        end_line_number += 1
    text = "".join(lines[line_number + 1 : end_line_number]).strip()
    return ChangeLog(id=code, title=title, text=text).as_dict()
