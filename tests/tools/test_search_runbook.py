
import pytest

from triage.tools.search_runbook import RunbookEntry, get_source_name, iter_runbook_entries

RB_FILES = [
    "search-and-caching.md",
    "data-platform.md",
    "payments.md",
    "platform-operations.md",
    "_archive/checkout-runbook-2024.md",
    "database.md",
]


@pytest.fixture
def runbook_file(request, datadir):
    return datadir / request.param


@pytest.fixture
def expected(request):
    return request.param


@pytest.fixture
def source(request):
    return request.param


@pytest.fixture
def runbook_files(datadir):
    return [datadir / log_file for log_file in RB_FILES]


@pytest.mark.parametrize(
    "runbook_file, expected",
    [(file, file) for file in RB_FILES],
    indirect=True,
)
def test_get_source_name(runbook_file, expected, datadir):
    assert get_source_name(runbook_file, datadir) == expected


@pytest.mark.parametrize(
    "runbook_file, source",
    [(file, file) for file in RB_FILES],
    indirect=True,
)
def test_iter_runbook_entries(runbook_file, source):

    entries = list(iter_runbook_entries(runbook_file, source))
    assert len(entries) > 0
    assert all(isinstance(entry, RunbookEntry) for entry in entries)
    assert all(entry.source == source for entry in entries)