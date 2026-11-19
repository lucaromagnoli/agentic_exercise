from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from triage import INCIDENTS_DIR


@dataclass
class Incident:
    id: str
    title: str
    raised_at: datetime
    raised_by: str
    severity: str
    affected_services: str
    report: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_prompt(self) -> str:
        return f"""
        # Incident {self.id}
        {self.title}
        {self.raised_at}
        {self.severity}
        {self.affected_services}
        {self.report}
        """


def retrieve_incident_file(
    incident_id: str, incidents_dir: Path = INCIDENTS_DIR
) -> Path:
    """Retrieve the incident file from the incidents directory."""
    incident_file = incidents_dir / f"{incident_id}.md"
    if not incident_file.exists():
        raise FileNotFoundError(f"Incident file {incident_file} not found")
    return incident_file


def parse_incident_file(incident_file: Path) -> Incident:
    with open(incident_file, "r") as f:
        lines = f.readlines()
    incident_prefix = "# INC"
    raised_prefix = "- **Raised:**"
    raised_by_prefix = "- **Raised by:**"
    severity_prefix = "- **Severity:**"
    affected_services_prefix = "- **Affected services:**"
    report_prefix = "## Report"
    for line_number, line in enumerate(lines):
        if line.startswith(incident_prefix):
            parts = [
                p.strip()
                for p in line.replace("# ", "").strip().split(" - ", maxsplit=1)
            ]
            id_, title = "-".join(parts[0:1]), "-".join(parts[1:])
        elif line.startswith(raised_prefix):
            raised_at = datetime.strptime(
                line.split(raised_prefix)[1].strip(), "%Y-%m-%d %H:%M UTC"
            ).replace(tzinfo=UTC)
        elif line.startswith(raised_by_prefix):
            raised_by = line.split(raised_by_prefix)[1].strip()
        elif line.startswith(severity_prefix):
            severity = line.split(severity_prefix)[1].strip()
        elif line.startswith(affected_services_prefix):
            affected_services = line.split(affected_services_prefix)[1].strip()
        elif line.startswith(report_prefix):
            report = "".join(lines[line_number + 1 :]).strip()
            break
    return Incident(
        id=id_,
        title=title,
        raised_at=raised_at,
        raised_by=raised_by,
        severity=severity,
        affected_services=affected_services,
        report=report,
    )
