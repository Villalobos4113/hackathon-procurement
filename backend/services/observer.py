"""Observer service for final release validation.

This module performs a deterministic audit pass over the assembled recommendation
package before it is returned to the caller.
"""

from __future__ import annotations

from typing import Any


def run_observer_check(
    recommendation: dict[str, Any],
    escalations: list[dict[str, Any]],
    shortlist: list[dict[str, Any]],
    audit_trail: dict[str, Any] | None = None,
    agent_opinions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return an observer report used as a final release gate.

    The observer is intentionally deterministic. It does not replace the
    explainer or specialist agents. It validates that the final package is
    internally coherent and safe to release.
    """
    audit_trail = audit_trail or {}
    agent_opinions = agent_opinions or []

    findings: list[dict[str, Any]] = []
    recommended_supplier_id = None
    if shortlist:
        recommended_supplier_id = shortlist[0].get("supplier_id")

    blocking_escalations = [e for e in escalations if e.get("blocking")]
    if blocking_escalations and recommendation.get("status") in {"proceed", "can_proceed"}:
        findings.append({
            "type": "blocking_escalation_conflict",
            "severity": "critical",
            "message": "Recommendation indicates proceed while blocking escalations are still open.",
        })

    for esc in escalations:
        if not esc.get("escalate_to"):
            findings.append({
                "type": "missing_escalation_target",
                "severity": "high",
                "message": f"Escalation {esc.get('rule', 'unknown')} is missing an explicit human target.",
            })

    if recommended_supplier_id:
        evaluated_ids = set(audit_trail.get("supplier_ids_evaluated", []))
        if evaluated_ids and recommended_supplier_id not in evaluated_ids:
            findings.append({
                "type": "recommended_supplier_not_in_audit_scope",
                "severity": "critical",
                "message": "Recommended supplier is not present in the audited supplier list.",
            })

    if shortlist and not agent_opinions:
        findings.append({
            "type": "no_agent_participation_visible",
            "severity": "medium",
            "message": "Shortlist exists but no agent opinions are visible in the response payload.",
        })

    status = "pass" if not any(f["severity"] in {"critical", "high"} for f in findings) else "review_required"

    return {
        "status": status,
        "findings": findings,
        "release_ready": status == "pass",
        "recommended_action": (
            "release_final_package" if status == "pass" else "return_to_supervisor"
        ),
    }
