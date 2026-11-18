
import pytest

from triage.tools.search_runbook import get_source_name

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
    return datadir / "runbook" / request.param


@pytest.fixture
def expected(request):
    return request.param


@pytest.fixture
def runbook_files(datadir):
    return [datadir / log_file for log_file in RB_FILES]


@pytest.mark.parametrize(
    "runbook_file, expected",
    [
        ("database.md", "database.md"),
        ("_archive/checkout-runbook-2024.md", "_archive/checkout-runbook-2024.md"),
    ],
    indirect=True,
)
def test_get_source_name(runbook_file, expected):
    assert get_source_name(runbook_file) == expected
