import pytest

from triage.tools.search_changes import iter_change_log, search_changes


@pytest.fixture
def change_log_file(datadir):
    return datadir / "change-log.md"


def test_parse_change_log(change_log_file):
    changes = list(iter_change_log(change_log_file))
    assert len(changes) == 11
    for chg in changes:
        assert hasattr(chg, "id")
        assert hasattr(chg, "title")
        assert hasattr(chg, "text")
        assert hasattr(chg, "date")


def test_parse_change_log_entry(change_log_file):
    changes = list(iter_change_log(change_log_file))
    assert len(changes) == 11
    found = False
    for chg in changes:
        if chg.id == "CHG-1026":
            found = True
            break
    assert found
    assert chg.title == "Quarterly runbook review"
    assert chg.text.startswith("- **Applied:** ")


@pytest.mark.parametrize(
    "query, expected_results",
    [
        ("Quarterly runbook review", 1),
        ("db.pool.max", 2),
    ],
)
def test_search_changes(change_log_file, query, expected_results):
    changes = search_changes(change_log_file, query)
    assert changes["total_matches"] == expected_results
    assert changes["returned"] == expected_results
