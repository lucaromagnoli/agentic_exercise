from pydantic_ai import Agent

from triage.agents import load_prompt
from triage.agents.models import ChangeHistory, Dependencies

change_historian_agent = Agent(
    "anthropic:claude-sonnet-5-5",
    instructions=load_prompt("change_historian"),
    output_type=ChangeHistory,
    deps_type=Dependencies,
)
