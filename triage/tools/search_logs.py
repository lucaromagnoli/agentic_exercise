from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class LogLine:
    line_number: int
    timestamp: datetime
    raw_line: str

    def __str__(self) -> str:
        return self.raw_line


@dataclass
class LogFile:
    path: Path
    lines: list[LogLine]

    def __str__(self) -> str:
        return f"{self.path} {self.lines}"


def from_line(line: str, number: int) -> "LogLine":
    timestamp = line.split()[0]
    return LogLine(
        line_number=number,
        timestamp=datetime.fromisoformat(timestamp),
        raw_line=line,
    )


def read_log_lines(log_file: Path) -> list[LogLine]:
    lines = []
    with open(log_file, "r") as file:
        for index, line in enumerate(file, start=1):
            lines.append(from_line(line, index))
    return lines


def read_log_file(log_file: Path) -> LogFile:
    lines = read_log_lines(log_file)
    return LogFile(path=log_file, lines=lines)


def search_log_file(log_file: Path, search_term: str) -> list[LogLine]:
    log_file = read_log_file(log_file)
    return [line for line in log_file.lines if search_term in line.raw_line]


def search_logs(log_files: list[Path], search_term: str, max_results: int = 200) -> list[LogLine]:
    log_lines = []
    for log_file in log_files:
        log_lines.extend(search_log_file(log_file, search_term))
    return sorted(log_lines, key=lambda x: x.timestamp)[:max_results]
