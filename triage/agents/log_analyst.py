from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Evidence(BaseModel):
    log_file: str
    log_line: int
    when: datetime
    message: str


class LogEvent(BaseModel):
    when: datetime
    description: str
    service: str
    evidence: list[Evidence]


class Hypothesis(BaseModel):
    verdict: Literal["supported", "refuted", "inconclusive"]
    evidence: list[Evidence]


class LogAnalysis(BaseModel):
    events: list[LogEvent]
    failure_mode: str
    onset_time: datetime
    hypothesis_tested: list[Hypothesis]
    open_questions: list[str]

    def analyze(self) -> list[LogEvent]:
        return self.events
