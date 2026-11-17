import pytest

from triage.tools.matching import match_query


@pytest.mark.parametrize(
    "query, log_line, expected",
    [
        ("upstream", "upstream", True),
        ("upstream", "upstream is working", True),
        ("upstream", "apstream is not working", False),
        ("upstream", "upstream is working", True),
        ("CPU", "cpu", True),
        ("active connections", "connections active", True),
        ("", "upstream", False),
        ("  ", "upstream", False),
    ],
)
def test_match_query(query, log_line, expected):
    assert match_query(query, log_line) == expected

   