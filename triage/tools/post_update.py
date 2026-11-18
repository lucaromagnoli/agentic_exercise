from typing import Any

from triage.tools import PROJECT_ROOT

OUTDIR = PROJECT_ROOT / "out"
LOGFILENAME = "comms.log"


def post_update(text: str, max_characters: int = 600) -> dict[str, Any]:
    """Post update to the logfile."""
    if len(text) > max_characters:
        return {
            "status": "error",
            "message": f"update exceeds {max_characters} characters",
        }
    OUTDIR.mkdir(parents=True, exist_ok=True)
    logfile = OUTDIR / LOGFILENAME
    with open(logfile, "a") as f:
        f.write(text + "\n")

    return {"status": "posted", "channel": "#incident-updates", "characters": len(text)}
