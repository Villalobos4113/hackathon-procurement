# Routing and Escalation Matrix

This matrix translates the refined flow into explicit routing logic.

## Primary routing matrix

| Condition | Primary route | Required agents | Output |
|---|---|---|---|
| Missing critical info or low extraction confidence | Clarification | Supervisor | Kickback to requester, ER-001 |
| Standard item, low risk, below threshold, known specs, approved supplier exists | Marketplace | Supervisor | Auto-pricing or lightweight approval |
| Standard item but no approved supplier or catalog hit | Supplier discovery | Supervisor, Discovery, Risk | Candidate onboarding case or escalation |
| Non-standard item, threshold-sensitive, high-risk, multi-country, exception-heavy | Strategic orchestration | Supervisor, Risk, Compliance, Commercial | Auditable shortlist |
| Shortlist produced | Observer check | Observer | Release or return for rework |

## Dynamic escalation targeting matrix

| Rule / trigger | Trigger condition | Human target | Blocking |
|---|---|---|---|
| ER-001 | Missing critical fields, clarification required, or budget insufficient | Requester Clarification | Yes |
| ER-002 | Preferred supplier is restricted | Procurement Manager | Yes |
| ER-003 | High-value threshold exceeded | Head of Strategic Sourcing | No |
| ER-004 | No compliant supplier or no viable candidate after discovery | Head of Category | Yes |
| ER-005 | Data residency or security/compliance gap | Security and Compliance Review | Yes |
| ER-006 | Bundled or requested volume exceeds capacity | Sourcing Excellence Lead | No |
| ER-007 | Marketing / influencer governance case | Marketing Governance Lead | No |
| ER-008 | Regional registration or country compliance issue | Regional Compliance Lead | No |

## Supplier discovery sub-process matrix

| Discovery event | Agent action | Decision |
|---|---|---|
| No approved supplier found | Discovery agent opens candidate search | Start onboarding case |
| Candidate has incomplete master data | Risk agent labels as provisional and lists evidence gaps | Continue only with disclosure |
| Candidate fails mandatory onboarding controls | Supervisor routes to ER-004 or ER-005 | Stop and escalate |
| Candidate passes enough checks for controlled comparison | Send to strategic orchestration | Include discovery context in final rationale |

## Observer release matrix

| Observer check | Failure outcome | Pass outcome |
|---|---|---|
| Structured facts and narrative disagree | Return to supervisor for re-run | Continue |
| Blocking escalation missing from recommendation | Return to supervisor for correction | Continue |
| Missing evidence for recommended supplier | Return to supervisor for evidence gap closure | Continue |
| Exact escalation target missing | Return to supervisor for correction | Continue |
| Audit package complete and coherent | Release final package | Final recommendation issued |
