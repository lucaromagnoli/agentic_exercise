from dataclasses import asdict, dataclass
from typing import Any


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


def search_runbook(query: str) -> dict[str, Any]:
    return SearchRunbookResult(query=query, total_matches=0, returned=0, results=[])
