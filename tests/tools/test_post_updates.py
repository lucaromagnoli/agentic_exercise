import pytest

from triage.tools.post_update import LOGFILENAME, post_update


@pytest.fixture
def delete_log_file(datadir):
    return datadir / "out" / LOGFILENAME


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is a test update",
            {"status": "posted", "channel": "#incident-updates", "characters": 21},
        ),
    ],
)
def test_post_update(text, expected, delete_log_file):
    result = post_update(text, log_file=delete_log_file)
    assert result == expected


def test_post_update_max_characters(delete_log_file):
    result = post_update("This is a test update" * 100, log_file=delete_log_file)
    assert result["error"] == "update exceeds 600 characters"
