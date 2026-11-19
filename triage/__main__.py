import pprint
from dotenv import load_dotenv
import logfire

from triage import INCIDENTS_DIR, LOGS_DIR
from triage.agents.log_analyst import Dependencies, log_analyst_agent
from triage.orchestrator import parse_incident_file

load_dotenv()


dependencies = Dependencies(
    logs_dir=LOGS_DIR,
)

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()

result = log_analyst_agent.run_sync(
    parse_incident_file(INCIDENTS_DIR / "INC-2043.md").to_prompt(),
    deps=dependencies,
)
pprint.pprint(result)
