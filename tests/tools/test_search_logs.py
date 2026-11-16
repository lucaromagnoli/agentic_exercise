import pytest

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
    indirect=True)
def test_read_log_file(log_file):
    log_file = read_log_file(log_file)
    assert log_file.path is not None
    assert log_file.lines is not None
    assert len(log_file.lines) > 0
    assert log_file.lines[0].timestamp is not None
    assert log_file.lines[0].service is not None
    assert log_file.lines[0].level is not None
    assert log_file.lines[0].message is not None