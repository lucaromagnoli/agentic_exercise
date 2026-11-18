from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from triage.tools.common import iter_sections


@dataclass
class RunbookEntry:
    id: str
    title: str
    source: str
    text: str


@dataclass
class SearchRunbookResult:
    query: str
    total_matches: int
    returned: int
    results: list[RunbookEntry]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def get_source_name(runbook_file: Path, runbook_dir: Path) -> bool:
    """Get the source name of a runbook file, relative to the runbook directory."""
    return runbook_file.relative_to(runbook_dir).as_posix()


def iter_runbook_entries(runbook_file: Path, source: str) -> Iterator[RunbookEntry]:
    for section in iter_sections(runbook_file):
        yield RunbookEntry(
            id=section.id,
            title=section.title,
            source=source,
            text=section.text,
        )
