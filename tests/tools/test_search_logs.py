from datetime import datetime

import pytest

from triage.tools.search_logs import (
    read_log_file,
    search_log_file,
    search_log_files,
    search_logs,
)

LOG_FILES = [
    "api-gateway.log",
    "checkout-service.log",
    "payments-worker.log",
    "platform-events.log",
    "postgres.log",
    "recon-worker.log",
    "search-service.log",
]


@pytest.fixture
def log_file(request, datadir):
    return datadir / request.param


@pytest.fixture
def log_files(datadir):
    return [datadir / log_file for log_file in LOG_FILES]


@pytest.mark.parametrize(
    "log_file",
    LOG_FILES,
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


@pytest.mark.parametrize(
    "log_file, search_term",
    [
        ("api-gateway.log", "upstream"),
        ("checkout-service.log", "database"),
        ("payments-worker.log", "provider"),
        ("platform-events.log", "deploy"),
        ("postgres.log", "connections active"),
        ("recon-worker.log", "dead letter queue"),
        ("search-service.log", "cpu"),
    ],
    indirect=["log_file"],
)
def test_search_log_file(log_file, search_term):
    log_lines = search_log_file(log_file, search_term)
    assert log_lines is not None
    assert len(log_lines) > 0
    first_line = log_lines[0]
    assert isinstance(first_line.timestamp, datetime)
    assert isinstance(first_line.line_number, int)
    assert isinstance(first_line.raw_line, str)
    assert first_line.file_name == log_file.name


@pytest.mark.parametrize(
    "search_term, expected_count",
    [
        ("upstream", 14),
        ("database", 3),
        ("provider", 5),
        ("deploy", 9),
        ("connections active", 6),
        ("dead letter queue", 1),
        ("active connections", 6),
        ("cpu", 6),
    ],
)
def test_search_log_files(search_term, expected_count, log_files):

    log_lines = search_log_files(log_files, search_term)
    assert log_lines is not None
    assert len(log_lines) == expected_count
    first_line = log_lines[0]
    assert isinstance(first_line.timestamp, datetime)
    assert isinstance(first_line.line_number, int)
    assert isinstance(first_line.raw_line, str)
    assert first_line.file_name in [log_file.name for log_file in log_files]


def test_search_logs(log_files):
    search_results = search_logs(log_files, "upstream", max_results=10)
    assert search_results is not None
    assert search_results["query"] == "upstream"
    assert search_results["total_matches"] == 14
    assert search_results["returned"] == 10
    assert search_results["truncated"] == True
    assert len(search_results["results"]) == 10
    assert all(isinstance(result, dict) for result in search_results["results"])
    assert all(
        key in result
        for key in ["file", "line", "text"]
        for result in search_results["results"]
    )


def test_search_logs_empty_query(log_files):
    search_results = search_logs(log_files, " ", max_results=10)
    assert search_results is not None
    assert search_results["error"] == "query must contain at least one term"


def test_search_logs_one_result(log_files):
    search_results = search_logs(log_files, "dead letter queue")
    assert search_results is not None
    assert search_results["query"] == "dead letter queue"
    assert search_results["total_matches"] == 1
    assert search_results["returned"] == 1
    assert search_results["truncated"] == False
    assert len(search_results["results"]) == 1
    assert search_results["results"][0]["file"] == "recon-worker.log"
    assert search_results["results"][0]["line"] == 12
    assert (
        search_results["results"][0]["text"]
        == "2026-08-05T02:31:11Z  recon-worker  WARN   dead letter queue depth rising queue=reconciliation.dlq depth=1 growth=1/15m"
    )
