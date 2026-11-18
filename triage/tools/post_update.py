from typing import Any

from triage.tools import PROJECT_ROOT

OUTDIR = PROJECT_ROOT / "out"


def post_update(text: str) -> dict[str, Any]:
    """Post update to the logfile."""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    logfile = OUTDIR / "update.log"
    with open(logfile, "a") as f:
        f.write(text + "\n")

    return {"status": "posted", "channel": "#incident-updates", "characters": len(text)}
