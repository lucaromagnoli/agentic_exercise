import pytest
from datetime import datetime
from triage.tools.search_logs import read_log_file


@pytest.fixture
def log_file(request, datadir):
    return datadir / request.param


@pytest.mark.parametrize(
    "log_file",
    [
        "api-gateway.log",
        "checkout-service.log",
        "payments-worker.log",
        "platform-events.log",
        "postgres.log",
        "recon-worker.log",
        "search-service.log",
    ],
    indirect=True,
)
def test_read_log_file(log_file):
    log_file = read_log_file(log_file)
    assert log_file.path is not None
    assert log_file.lines is not None
    assert len(log_file.lines) > 0
    first_line = log_file.lines[0]
    assert isinstance(first_line.timestamp, datetime)
    assert isinstance(first_line.line_number, int)
    assert isinstance(first_line.raw_line, str)
