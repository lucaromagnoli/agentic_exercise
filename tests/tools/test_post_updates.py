import pytest

from triage.tools.post_update import post_update


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "This is a test update",
            {"status": "posted", "channel": "#incident-updates", "characters": 21},
        ),
    ],
)
def test_post_update(text, expected):
    result = post_update(text)
    assert result == expected


def test_post_update_max_characters():
    result = post_update("This is a test update" * 100)
    assert result["status"] == "error"
    assert result["message"] == "update exceeds 600 characters"
