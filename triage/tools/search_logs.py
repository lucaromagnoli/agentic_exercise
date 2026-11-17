from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from triage.tools.matching import match_query


@dataclass
class LogLine:
    file_name: str
    line_number: int
    timestamp: datetime
    raw_line: str

    def __str__(self) -> str:
        return self.raw_line

    def to_record(self) -> dict[str, Any]:
        return {
            "file": self.file_name,
            "line": self.line_number,
            "text": self.raw_line,
        }


@dataclass
class LogFile:
    path: Path
    lines: list[LogLine]

    def __str__(self) -> str:
        return f"{self.path} {self.lines}"


@dataclass
class SearchResults:
    query: str
    total_matches: int
    returned: int
    truncated: bool
    results: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def from_line(line: str, number: int, log_file: Path) -> "LogLine":
    timestamp = line.split()[0]
    return LogLine(
        file_name=log_file.name,
        line_number=number,
        timestamp=datetime.fromisoformat(timestamp),
        raw_line=line,
    )


def read_log_lines(log_file: Path) -> list[LogLine]:
    lines = []
    with open(log_file, "r") as file:
        for index, line in enumerate(file, start=1):
            lines.append(from_line(line.strip(), index, log_file))
    return lines


def read_log_file(log_file: Path) -> LogFile:
    lines = read_log_lines(log_file)
    return LogFile(path=log_file, lines=lines)


def search_log_file(log_file: Path, search_term: str) -> list[LogLine]:
    log_file = read_log_file(log_file)
    return [line for line in log_file.lines if match_query(search_term, line.raw_line)]


def search_log_files(log_files: list[Path], search_term: str) -> list[LogLine]:
    log_lines = []
    for log_file in log_files:
        log_lines.extend(search_log_file(log_file, search_term))
    return sorted(log_lines, key=lambda x: x.timestamp)


def search_logs(
    log_files: list[Path], search_term: str, max_results: int = 20
) -> dict[str, Any]:
    if search_term.strip() == "":
        return {"error": "query must contain at least one term"}
    results = search_log_files(log_files, search_term)
    search_results = SearchResults(
        query=search_term,
        total_matches=len(results),
        returned=len(results[:max_results]),
        truncated=len(results) > max_results,
        results=[result.to_record() for result in results[:max_results]],
    )
    return search_results.to_dict()
