import re
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from triage.tools.common import common_error, match_query


@dataclass
class ChangeLog:
    id: str
    title: str
    text: str
    date: datetime | None = None

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "title": self.title, "text": self.text}


def iter_change_log(change_log_file: Path) -> Iterator[ChangeLog]:
    with open(change_log_file, "r") as file_handle:
        lines = file_handle.readlines()
    for line_number, line in enumerate(lines):
        if line.startswith("## CHG"):
            yield parse_change_log_entry(line_number, lines)


def find_date(text: str) -> datetime:
    lines = text.split("\n")
    for line in lines:
        if any(x in line for x in ["**Applied:**", "**Shipped:**"]):
            date_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", line)
            if date_match:
                return datetime.strptime(date_match.group(0), "%Y-%m-%d %H:%M")
    return None


def parse_change_log_entry(line_number: int, lines: list[str]) -> ChangeLog:
    code_title = lines[line_number].split("##")[1].strip()
    code, title = [x.strip() for x in code_title.split(" - ", maxsplit=1)]
    end_line_number = line_number + 1
    while end_line_number < len(lines) and not lines[end_line_number].startswith("---"):
        end_line_number += 1
    text = "".join(lines[line_number + 1 : end_line_number]).strip()
    return ChangeLog(id=code, title=title, text=text, date=find_date(text))


def match_terms(change: ChangeLog, query: str) -> bool:
    change_text = f"{change.id} {change.title} {change.text}"
    return match_query(query, change_text)


def search_changes(
    change_log_file: Path, query: str, max_results: int = 5
) -> dict[str, Any]:
    if query.strip() == "":
        return common_error()
    changes = list(iter_change_log(change_log_file))
    changes.sort(key=lambda x: x.date, reverse=True)
    results = [change.as_dict() for change in changes if match_terms(change, query)]
    return {
        "total_matches": len(results),
        "returned": len(results[:max_results]),
        "truncated": len(results) > max_results,
        "query": query,
        "results": results[:max_results],
    }
