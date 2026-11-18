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


def get_source_name(runbook_file: Path) -> bool:
    """Get the source name of a runbook file, relative to the runbook directory."""
    runbook_index = runbook_file.parts.index("runbook")
    return "/".join(runbook_file.parts[runbook_index + 1 :])


def iter_runbook_entries(runbook_file: Path) -> Iterator[RunbookEntry]:
    for section in iter_sections(runbook_file):
        source = get_source_name(runbook_file)
        yield RunbookEntry(
            id=section.id,
            title=section.title,
            source=source,
            text=section.text,
        )
