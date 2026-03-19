"""Supplier discovery service scaffold.

This service is invoked when no approved supplier or catalog item is available.
It prepares a controlled candidate evaluation case instead of treating the flow
as a dead end.
"""

from __future__ import annotations

from typing import Any


def build_supplier_discovery_case(
    request: dict[str, Any],
    excluded_suppliers: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    excluded_suppliers = excluded_suppliers or []

    return {
        "triggered": True,
        "reason": "no_approved_supplier_or_catalog_hit",
        "request_summary": {
            "category_l1": request.get("category_l1"),
            "category_l2": request.get("category_l2"),
            "quantity": request.get("quantity"),
            "currency": request.get("currency"),
            "delivery_countries": request.get("delivery_countries", []),
            "required_by_date": request.get("required_by_date"),
        },
        "discovery_actions": [
            "search_candidate_suppliers",
            "request_supplier_master_data",
            "request_onboarding_documents",
            "run_provisional_risk_assessment",
            "run_compliance_precheck",
        ],
        "known_gaps": [
            e.get("exclusion_reason") for e in excluded_suppliers if e.get("exclusion_reason")
        ],
        "provisional_status": "pending_candidate_evaluation",
    }


def evaluate_discovery_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Simple deterministic viability screen for a newly discovered supplier."""
    missing = []
    required_fields = [
        "supplier_name",
        "service_regions",
        "contract_status",
        "data_residency_supported",
    ]
    for field in required_fields:
        if candidate.get(field) in (None, "", []):
            missing.append(field)

    viable = len(missing) == 0 and candidate.get("contract_status") in {"active", "pending_onboarding"}

    return {
        "viable_for_controlled_comparison": viable,
        "missing_fields": missing,
        "risk_posture": "provisional" if missing else "known",
        "recommended_route": (
            "strategic_orchestration" if viable else "escalate_or_complete_onboarding"
        ),
    }
