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


def parse_incident_file(incident_file: Path) -> dict[str, Any]:
    with open(incident_file, "r") as f:
        lines = f.readlines()
    return lines


def retrieve_incident_file(
    incident_id: str, incidents_dir: Path = INCIDENTS_DIR
) -> Path:
    """Retrieve the incident file from the incidents directory."""
    incident_file = incidents_dir / f"{incident_id}.md"
    if not incident_file.exists():
        raise FileNotFoundError(f"Incident file {incident_file} not found")
    return incident_file
