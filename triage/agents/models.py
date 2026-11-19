from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from anyio import Path
from pydantic import BaseModel, Field


@dataclass
class Dependencies:
    logs_dir: Path


class LogEvidence(BaseModel):
    file: str = Field(
        description="The `file` value of the search_logs result being cited, e.g. 'checkout-service.log'."
    )
    line: int = Field(
        description="The `line` value of the search_logs result being cited."
    )


class ChangeEvidence(BaseModel):
    id: str = Field(description="The ID of the change that is being cited.")


class LogEvent(BaseModel):
    time: datetime = Field(
        description="The time of the event, as returned by search_logs."
    )
    evidence: list[LogEvidence] = Field(
        description="All the evidence for the event from the log files."
    )
    description: str = Field(description="A factual description of the event.")
    service: str = Field(
        description="The service that the event is from, e.g. 'checkout-service'."
    )


class Hypothesis(BaseModel):
    claim: str = Field(description="The claim that the hypothesis is testing.")
    why: str = Field(description="How the cited evidence leads to the verdict.")
    verdict: Literal["supported", "refuted", "inconclusive"]
    evidence: list[LogEvidence]


class LogAnalysis(BaseModel):
    events: list[LogEvent]
    failure_mode: str
    onset_time: datetime | None = Field(
        description="The time of the failure, if known."
    )
    hypotheses: list[Hypothesis]
    open_questions: list[str]


class ChangeEvent(BaseModel):
    time: datetime = Field(description="The time of the event, as returned by searc.")
    evidence: list[ChangeEvidence] = Field(
        description="All the evidence for the event from the change history."
    )
    description: str = Field(description="A factual description of the event.")
    service: str = Field(
        description="The service that the event is from, e.g. 'checkout-service'."
    )


class ChangeHistory(BaseModel):
    changes: list[ChangeEvent]
    open_questions: list[str]
