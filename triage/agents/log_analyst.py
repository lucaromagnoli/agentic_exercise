from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic_ai import Agent, RunContext

from triage.agents import load_prompt
from triage.agents.models import LogAnalysis
from triage.tools.search_logs import search_logs as search_logs_tool


@dataclass
class Dependencies:
    logs_dir: Path


log_analyst_agent = Agent(
    "anthropic:claude-sonnet-5-5",
    output_type=LogAnalysis,
    instructions=load_prompt("log_analyst"),
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
