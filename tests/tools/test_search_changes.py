import pytest

from triage.tools.search_changes import iter_change_log


@pytest.fixture
def change_log_file(datadir):
    return datadir / "change-log.md"


def test_parse_change_log(change_log_file):
    changes = list(iter_change_log(change_log_file))
    assert len(changes) == 11
    for chg in changes:
        assert "id" in chg
        assert "title" in chg
        assert "text" in chg
        if chg["id"] == "CHG-1026":
            assert chg["title"] == "Quarterly runbook review"
            assert chg["text"].startswith("- **Applied:** ")
