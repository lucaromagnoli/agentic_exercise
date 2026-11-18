from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Section:
    id: str
    title: str
    text: str


def match_query(query: str, text: str) -> bool:
    """Match a query against a text."""
    terms = query.split()
    if terms:
        return all(term.lower() in text.lower() for term in terms)
    return False


def common_error(
    message: str = "query must contain at least one term",
) -> dict[str, Any]:
    return {"error": message}


def iter_sections(
    file_path: Path,
    section_prefix: str,
) -> Iterator[Section]:
    with open(file_path, "r") as file_handle:
        lines = file_handle.readlines()
    for line_number, line in enumerate(lines):
        if line.startswith(section_prefix):
            yield parse_section(line_number, lines)


def parse_section(
    line_number: int,
    lines: list[str],
) -> Section:
    id_title = lines[line_number].split("##")[1].strip()
    id_, title = [x.strip() for x in id_title.split(" - ", maxsplit=1)]
    end_line_number = line_number + 1
    while end_line_number < len(lines) and not lines[end_line_number].startswith("---"):
        end_line_number += 1
    text = "".join(lines[line_number + 1 : end_line_number]).strip()
    return Section(id=id_, title=title, text=text)
