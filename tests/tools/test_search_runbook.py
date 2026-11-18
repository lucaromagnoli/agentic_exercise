import pytest

from triage.tools.search_runbook import (
    RunbookEntry,
    get_source_name,
    iter_runbook_entries,
    search_runbook,
)

RB_FILES = [
    "search-and-caching.md",
    "data-platform.md",
    "payments.md",
    "platform-operations.md",
    "_archive/checkout-runbook-2024.md",
    "database.md",
]


@pytest.fixture
def runbook_dir(data_dir):
    return data_dir / "runbook"


@pytest.fixture
def runbook_file(request, runbook_dir):
    return runbook_dir / request.param


@pytest.fixture
def runbook_files(runbook_dir):
    return [runbook_dir / log_file for log_file in RB_FILES]


@pytest.mark.parametrize(
    "runbook_file, expected",
    [(file, file) for file in RB_FILES],
    indirect=["runbook_file"],
)
def test_get_source_name(runbook_file, expected, data_dir):
    runbook_dir = data_dir / "runbook"
    assert get_source_name(runbook_file, runbook_dir) == expected


@pytest.mark.parametrize(
    "runbook_file, source",
    [(file, file) for file in RB_FILES],
    indirect=["runbook_file"],
)
def test_iter_runbook_entries(runbook_file, source):

    entries = list(iter_runbook_entries(runbook_file, source))
    assert len(entries) > 0
    assert all(isinstance(entry, RunbookEntry) for entry in entries)
    assert all(entry.source == source for entry in entries)


@pytest.mark.parametrize(
    "query, expected_total_matches, expected_returned",
    [
        ("database", 3, 3),
        ("checkout", 3, 3),
        ("payments", 2, 2),
        ("platform", 4, 3),
    ],
)
def test_search_runbook(runbook_dir, query, expected_total_matches, expected_returned):
    rb_search_results = search_runbook(runbook_dir, query)
    assert rb_search_results is not None
    assert rb_search_results["query"] == query
    assert rb_search_results["total_matches"] == expected_total_matches
    assert rb_search_results["returned"] == expected_returned
    assert all(isinstance(result, dict) for result in rb_search_results["results"])
    assert all(
        x in result
        for x in ["id", "title", "source", "text"]
        for result in rb_search_results["results"]
    )


def test_search_runbook_empty_query(runbook_dir):
    rb_search_results = search_runbook(runbook_dir, "")
    assert rb_search_results is not None
    assert rb_search_results["error"] == "query must contain at least one term"


def test_search_runbook_ordered_results(runbook_dir):
    rb_search_results = search_runbook(runbook_dir, "database")
    assert rb_search_results is not None
    assert rb_search_results["results"] == sorted(
        rb_search_results["results"], key=lambda x: x["id"]
    )
