# Refined Agentic Procurement Flow

This version tightens the routing model around three principles:

1. **An agent is always in the loop** through an always-on orchestration supervisor.
2. **Approved supplier / catalog gaps trigger a supplier discovery sub-process** instead of a dead end.
3. **A final observer validates the package** before the recommendation is released.

## Mermaid flow

```mermaid
graph TD
    %% Styling
    classDef intake fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef aiLogic fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef market fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef complex fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef human fill:#ffebee,stroke:#f44336,stroke-width:2px;
    classDef audit fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px;

    %% Intake + always-on orchestration
    A[Unstructured Request<br/>email, chat, portal, multilingual]:::intake --> B[Generative Front Door<br/>normalize, translate, extract fields]:::aiLogic
    B --> C[Orchestration Supervisor Agent<br/>always-on controller, route selection,<br/>agent assignment, escalation watchpoints]:::complex
    C --> D{Complete enough<br/>and confidence acceptable?}:::aiLogic

    D -- No --> E[Kickback to requester<br/>or human clarification<br/>Trigger: ER-001]:::human
    D -- Yes --> F[Policy + Taxonomy Mapping<br/>category, threshold, restrictions]:::aiLogic

    %% Main routing
    F --> G{Marketplace Eligibility Gate<br/>standard item, low risk,<br/>below threshold, known specs?}:::aiLogic

    %% Marketplace lane
    G -- Yes --> H{Approved supplier / catalog<br/>available?}:::aiLogic
    H -- Yes --> I{Bundle opportunity exists?}:::aiLogic
    I -- Yes --> J{Can hold window apply<br/>without breaking SLA?}:::aiLogic
    J -- Yes --> K[Volume Aggregation Queue<br/>hold and consolidate demand]:::market
    J -- No --> N[Direct marketplace pricing]:::market
    I -- No --> N

    K --> K2{Bundled volume exceeds<br/>supplier monthly capacity?}:::aiLogic
    K2 -- Yes --> U[Dynamic Escalation Engine<br/>route to exact human title<br/>ER-006 → Sourcing Excellence Lead]:::human
    K2 -- No --> O[Match pricing tiers<br/>optimize volume discount]:::market
    N --> O
    O --> P{Auto-approve threshold met?}:::aiLogic
    P -- Yes --> Q[Auto-generate PO<br/>zero-touch execution]:::market
    P -- No --> R[Lightweight approval routing]:::human
    R --> Q

    %% New supplier discovery branch
    H -- No --> S[Supplier Discovery Trigger<br/>no approved supplier or catalog hit]:::complex
    S --> T[Discovery Agent<br/>search alternates, form candidate set,<br/>prepare onboarding case]:::complex
    T --> T2[Risk Agent<br/>missing-data-aware provisional risk posture]:::complex
    T2 --> T3[Onboarding + Compliance Procedure<br/>registration, documents, controls]:::complex
    T3 --> T4{Candidate viable enough<br/>for controlled comparison?}:::complex
    T4 -- No --> U
    T4 -- Yes --> V[Strategic Orchestration Intake]:::complex

    %% Orchestration lane
    G -- No --> V
    V --> W[Multi-agent squad<br/>risk, compliance, commercial, discovery context]:::complex
    W --> X[Supplier eligibility + comparison<br/>pricing, risk, ESG, geography]:::complex
    X --> Y{Needs exception,<br/>override, or escalation?}:::complex
    Y -- Yes --> U
    Y -- No --> Z[Auditable supplier shortlist<br/>ranked with transparent rationale]:::complex
    U --> Z

    %% Final observer / auditor
    Z --> AA[Observer / Audit Agent<br/>cross-check consistency, evidence,<br/>rules, escalations, generated report]:::audit
    AA --> AB{Observer passes?}:::audit
    AB -- No --> AC[Return to supervisor<br/>for evidence gap closure / re-run]:::complex
    AC --> W
    AB -- Yes --> AD[Final recommendation package<br/>approval routing + execution handoff]:::audit

    %% Always-on supervisor monitoring
    C -. monitors .-> F
    C -. monitors .-> H
    C -. monitors .-> W
    C -. monitors .-> AA

    %% Audit log
    B --> AE[Audit log<br/>reason codes, rules, decisions, evidence]:::audit
    C --> AE
    F --> AE
    K2 --> AE
    O --> AE
    Q --> AE
    T --> AE
    T2 --> AE
    T3 --> AE
    W --> AE
    X --> AE
    U --> AE
    Z --> AE
    AA --> AE
    AD --> AE
```

## What changed relative to the current design

### 1) Always-on orchestration supervisor
The supervisor is not just another optional specialist. It sits between extraction and routing and stays logically attached through the full lifecycle.

Suggested responsibilities:
- choose the primary lane: clarification, marketplace, supplier discovery, or strategic orchestration
- assign the minimum agent set for the case
- keep escalation watchpoints active
- re-run the workflow when the observer flags evidence gaps

### 2) Approved supplier unavailable now becomes a controlled sub-process
The old branch routed straight to strategic orchestration. The new branch is more explicit:
- trigger supplier discovery
- let the risk agent work with incomplete data instead of pretending certainty
- run onboarding and compliance checks before the new supplier joins comparison
- escalate if the candidate cannot be validated enough for controlled consideration

### 3) Observer / audit agent before release
This sits after shortlist generation and before final recommendation release.

Suggested checks:
- blocking escalations are reflected in the recommendation
- evidence exists for the chosen supplier and route
- pricing, policy, and escalation logic are internally consistent
- generated narrative matches the structured facts
- missing data is disclosed, not hidden

## Suggested integration points in the current repo

- `backend/services/extractor.py` remains the front door
- `backend/services/pipeline.py` should call the supervisor immediately after extraction
- `backend/services/supplier_filter.py` still handles standard eligibility filtering
- `backend/services/supplier_discovery.py` should own the new supplier branch
- `backend/services/orchestrator.py` should receive discovery context when discovery is triggered
- `backend/services/observer.py` should run after shortlist generation and before the final response is returned
- `backend/services/escalation.py` should remain deterministic and continue outputting exact human titles

## Minimal response extensions to support this

Recommended new fields for the analysis response:
- `supervisor_decision`
- `supplier_discovery_case`
- `observer_report`
- `final_release_status`

Those four additions will make the new flow visible in both the API and the frontend.
