from typing import List

from pydantic import BaseModel, Field


class CoverageAssessmentInput(BaseModel):
    report_id: str = Field(..., min_length=1)
    subscriber_id: str = Field(..., min_length=1)
    coverage_status: str = Field(..., min_length=1)
    service_availability: str = Field(..., min_length=1)
    outage_detected: bool
    serving_market: str = Field(..., min_length=1)
    roaming_state: str = Field(..., min_length=1)
    registration_state: str = Field(..., min_length=1)
    observations: List[str] = Field(default_factory=list)
    notes: str | None = None


class RCAHypothesis(BaseModel):
    type: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)


class RCAAnalysisToolResult(BaseModel):
    report_id: str = Field(..., min_length=1)
    root_cause_summary: str = Field(..., min_length=1)
    confidence: float = Field(..., ge=0.0, le=1.0)
    hypotheses: List[RCAHypothesis] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
