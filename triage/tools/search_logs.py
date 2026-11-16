from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class LogLine:
    timestamp: datetime
    level: str
    message: str
    service: str

    def __str__(self) -> str:
        return f"{self.timestamp} {self.service} {self.level} {self.message}"


@dataclass
class LogFile:
    path: Path
    lines: list[LogLine]

    def __str__(self) -> str:
        return f"{self.path} {self.lines}"


def from_line(line: str) -> "LogLine":
    timestamp, service, level, message = line.strip().split(maxsplit=3)
    return LogLine(
        timestamp=datetime.fromisoformat(timestamp), service=service, level=level, message=message
    )


def read_log_lines(log_file: Path) -> list[LogLine]:
    lines = []
    with open(log_file, "r") as file:
        for line in file:
            lines.append(from_line(line))
    return lines


def read_log_file(log_file: Path) -> LogFile:
    lines = read_log_lines(log_file)
    return LogFile(path=log_file, lines=lines)
