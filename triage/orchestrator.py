from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from triage import INCIDENTS_DIR


@dataclass
class Incident:
    raised_at: datetime
    raised_by: str
    severity: str
    affected_services: list[str]
    report: str


def retrieve_incident_file(
    incident_id: str, incidents_dir: Path = INCIDENTS_DIR
) -> Path:
    """Retrieve the incident file from the incidents directory."""
    incident_file = incidents_dir / f"{incident_id}.md"
    if not incident_file.exists():
        raise FileNotFoundError(f"Incident file {incident_file} not found")
    return incident_file


def parse_incident_file(incident_file: Path) -> dict[str, Any]:
    with open(incident_file, "r") as f:
        lines = f.readlines()
    raised_prefix = "- **Raised:**"
    raised_by_prefix = "- **Raised by:**"
    severity_prefix = "- **Severity:**"
    affected_services_prefix = "- **Affected services:**"
    report_prefix = "## Report"
    for line_number, line in enumerate(lines):
        if line.startswith(raised_prefix):
            raised_at = datetime.strptime(
                line.split(raised_prefix)[1].strip(), "%Y-%m-%d %H:%M UTC"
            )
        elif line.startswith(raised_by_prefix):
            raised_by = line.split(raised_by_prefix)[1].strip()
        elif line.startswith(severity_prefix):
            severity = line.split(severity_prefix)[1].strip()
        elif line.startswith(affected_services_prefix):
            affected_services = line.split(affected_services_prefix)[1].strip()
        elif line.startswith(report_prefix):
            report = "".join(lines[line_number + 1 :]).strip()
            break
    return {
        "raised_at": raised_at,
        "raised_by": raised_by,
        "severity": severity,
        "affected_services": affected_services,
        "report": report,
    }
