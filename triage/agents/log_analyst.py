from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic_ai import Agent, RunContext

from triage.agents.models import LogAnalysis
from triage.tools.search_logs import search_logs as search_logs_tool


@dataclass
class Dependencies:
    logs_dir: Path


log_analyst_agent = Agent(
    "anthropic:claude-sonnet-5-5",
    output_type=LogAnalysis,
    instructions="""
    You are a log analyst. You are given and Incident Report. 
    Your task is to analyze the logs and identify the following:
    - The events that occurred
    - The hypotheses that were tested
    - The verdicts of the hypotheses
    - The open questions
    - The failure mode
    - The onset time of the failure
    - The evidence for the events
    - The evidence for the hypotheses
    """,
    deps_type=Dependencies,
)


@log_analyst_agent.tool()
def search_logs(
    ctx: RunContext[Dependencies], query: str, max_results: int = 20
) -> dict[str, Any]:
    """
    Search the logs for the given query.
    """
    log_files = sorted(ctx.deps.logs_dir.glob("*.log"))
    return search_logs_tool(log_files, query, max_results)
