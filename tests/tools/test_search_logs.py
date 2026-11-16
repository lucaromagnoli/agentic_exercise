import pytest

from triage.tools.search_logs import read_log_file


@pytest.fixture
def log_file(request, datadir):
    return datadir / request.param


@pytest.mark.parametrize(
    "log_file", 
    [
        "api-gateway.log", 

    ], 
    indirect=True)
def test_read_log_file(log_file):
    log_file = read_log_file(log_file)
    