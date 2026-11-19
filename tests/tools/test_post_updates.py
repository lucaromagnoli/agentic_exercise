import pytest

from triage import LOG_FILE_NAME
from triage.tools.post_update import post_update


@pytest.fixture
def log_file(tmp_path):
    return tmp_path / "out" / LOG_FILE_NAME


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is a test update",
            {"status": "posted", "channel": "#incident-updates", "characters": 21},
        ),
    ],
)
def test_post_update(text, expected, log_file):
    result = post_update(text, log_file=log_file)
    assert result == expected


def test_post_update_max_characters(log_file):
    result = post_update("This is a test update" * 100, log_file=log_file)
    assert result["error"] == "update exceeds 600 characters"
