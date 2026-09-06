import os
import json
import importlib
import logging
from typing import Any

from app.mcp.tool_schema import CoverageAssessmentInput, RCAAnalysisToolResult


logger = logging.getLogger(__name__)


class AzureOpenAIClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
        self._azure_client: Any = None

        try:
            openai_module = importlib.import_module("openai")
            azure_openai_cls = getattr(openai_module, "AzureOpenAI")
        except Exception:
            azure_openai_cls = None

        has_required_config = bool(self.endpoint and self.api_key and self.deployment)
        if has_required_config and azure_openai_cls is not None:
            self._azure_client = azure_openai_cls(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )
            logger.info(
                "AzureOpenAIClient initialized mode=live endpoint=%s deployment=%s api_version=%s",
                self.endpoint,
                self.deployment,
                self.api_version,
            )
        else:
            logger.info(
                "AzureOpenAIClient initialized mode=stub has_endpoint=%s has_api_key=%s deployment=%s sdk_available=%s",
                bool(self.endpoint),
                bool(self.api_key),
                self.deployment,
                azure_openai_cls is not None,
            )

    def analyze_coverage_report(self, report: CoverageAssessmentInput) -> RCAAnalysisToolResult:
        payload = report.model_dump()
        logger.info("AzureOpenAI analyze_coverage_report request=%s", payload)

        if self._azure_client is None:
            response = self._build_stub_result(report)
            logger.info("AzureOpenAI analyze_coverage_report response_mode=stub response=%s", response.model_dump())
            return response

        try:
            completion = self._azure_client.chat.completions.create(
                model=self.deployment,
                temperature=0.2,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a telecom RCA assistant. Return only valid JSON with keys: "
                            "root_cause_summary, confidence, hypotheses, recommended_actions. "
                            "confidence must be between 0.0 and 1.0."
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps(payload),
                    },
                ],
            )
            content = completion.choices[0].message.content or "{}"
            parsed = json.loads(content)

            response = RCAAnalysisToolResult(
                report_id=report.report_id,
                root_cause_summary=parsed["root_cause_summary"],
                confidence=float(parsed["confidence"]),
                hypotheses=parsed.get("hypotheses", []),
                recommended_actions=parsed.get("recommended_actions", []),
            )
            logger.info("AzureOpenAI analyze_coverage_report response_mode=live response=%s", response.model_dump())
            return response
        except Exception:
            logger.exception("Live Azure OpenAI call failed, falling back to stub result")
            response = self._build_stub_result(report)
            logger.info("AzureOpenAI analyze_coverage_report response_mode=stub_after_error response=%s", response.model_dump())
            return response

    def _build_stub_result(self, report: CoverageAssessmentInput) -> RCAAnalysisToolResult:
        # This is intentionally a lightweight stub for the POC.
        # In a real implementation, this would call Azure OpenAI with a structured tool call.
        return RCAAnalysisToolResult(
            report_id=report.report_id,
            root_cause_summary=(
                "Localized network degradation and outage conditions are the most likely cause "
                "of the coverage issue in the current serving market."
            ),
            confidence=0.89,
            hypotheses=[
                {
                    "type": "outage",
                    "description": "Regional outage or service degradation detected in the serving market.",
                    "confidence": 0.88,
                },
                {
                    "type": "coverage",
                    "description": "Subscriber is in a degraded coverage area with intermittent service quality.",
                    "confidence": 0.74,
                },
            ],
            recommended_actions=[
                "Validate network outage feed for the serving market.",
                "Confirm registration and connectivity state for the subscriber.",
                "Escalate to network operations if the issue persists beyond policy thresholds.",
            ],
        )
