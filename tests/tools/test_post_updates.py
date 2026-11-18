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
