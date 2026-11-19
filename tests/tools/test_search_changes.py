import pytest

from triage.tools.search_changes import iter_change_log, search_changes


@pytest.fixture
def change_log_file(data_dir):
    return data_dir / "changes" / "change-log.md"


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
    "query, expected_total_matches, expected_returned, expected_truncated",
    [
        ("Quarterly runbook review", 1, 1, False),
        ("db.pool.max", 2, 2, False),
    ],
)
def test_search_changes(
    change_log_file,
    query,
    expected_total_matches,
    expected_returned,
    expected_truncated,
):
    changes = search_changes(change_log_file, query)
    assert changes["total_matches"] == expected_total_matches
    assert changes["returned"] == expected_returned
    assert changes["truncated"] == expected_truncated


def test_search_changes_empty_query(change_log_file):
    changes = search_changes(change_log_file, "")
    assert changes["error"] == "query must contain at least one term"


def test_search_changes_truncation(change_log_file):
    changes = search_changes(change_log_file, "checkout", max_results=2)
    assert changes["total_matches"] == 4
    assert changes["returned"] == 2
    assert changes["truncated"] is True


def test_search_changes_order(change_log_file):
    changes = search_changes(change_log_file, "db.pool.max")
    ids = [chg["id"] for chg in changes["results"]]
    assert ids == ["CHG-1044", "CHG-1042"]
