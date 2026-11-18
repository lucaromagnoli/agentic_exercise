from datetime import datetime

import pytest

from triage.orchestrator import parse_incident_file, retrieve_incident_file

INCIDENT_IDS = [
    "INC-2043",
    "INC-2051",
    "INC-2062",
]


@pytest.fixture
def incident_file(data_dir, request):
    return data_dir / "incidents" / request.param


@pytest.mark.parametrize(
    "incident_id",
    INCIDENT_IDS,
)
def test_retrieve_incident_file(incident_id):
    incident_file = retrieve_incident_file(incident_id)
    assert incident_file.exists()


@pytest.mark.parametrize(
    "incident_file",
    [f"{inc_id}.md" for inc_id in INCIDENT_IDS],
    indirect=True,
)
def test_parse_incident_file(incident_file):
    incident = parse_incident_file(incident_file)
    assert incident is not None


@pytest.mark.parametrize(
    "incident_file, expected",
    [
        (
            "INC-2043.md",
            {
                "raised_at": datetime(2026, 8, 12, 19, 38, 0),
                "raised_by": "Priya Raman, Customer Support Lead",
                "severity": "Sev-2",
                "affected_services": 'unclear, reported as "checkout"',
                "report": "Support started getting contacts around 19:35 UTC. Customers get an error page when they\npress Pay. It is not everyone, but it is a lot of people, and it seems to be getting worse\nrather than better. A few customers said it worked on the second or third try.\n\nOne of the engineers in the channel thinks it is the payment provider having problems\nagain, like earlier this evening. Nobody has confirmed that.\n\nWe need to know what actually broke, when it started, and what we are supposed to do\nabout it.",
            },
        )
    ],
    indirect=["incident_file"],
)
def test_parse_incident_file_fields(incident_file, expected):
    incident = parse_incident_file(incident_file)
    assert incident == expected
