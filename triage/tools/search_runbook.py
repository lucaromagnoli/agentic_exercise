from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from triage.tools.common import common_error, iter_sections, match_query


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


def get_source_name(runbook_file: Path, runbook_dir: Path) -> str:
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


def search_runbook(
    runbook_dir: Path, query: str, max_results: int = 3
) -> dict[str, Any]:
    if query.strip() == "":
        return common_error()
    results = []
    for runbook_file in runbook_dir.rglob("*.md"):
        for entry in iter_runbook_entries(
            runbook_file, get_source_name(runbook_file, runbook_dir)
        ):
            if match_query(query, f"{entry.id} {entry.title} {entry.text}"):
                results.append(entry)
    results = sorted(results, key=lambda x: x.id)
    return SearchRunbookResult(
        query=query,
        total_matches=len(results),
        returned=len(results[:max_results]),
        results=results[:max_results],
    ).to_dict()
