# Universal Multi-Agent Validation Flow

This revision makes the multi-agent team mandatory across all meaningful paths, including marketplace, bundled demand, supplier discovery, and strategic orchestration.

## Design principle

The multi-agent team is no longer a branch used only for complex cases.
It is now a **mandatory control layer** with two checkpoints:

1. **Intake triage checkpoint**
   Validates extraction quality, completeness, category interpretation, and early risk signals.

2. **Pre-release validation checkpoint**
   Validates pricing, capacity, policy fit, compliance posture, risk, and recommendation coherence before any PO, shortlist, or recommendation can be released.

That means direct marketplace pricing is still fast, but it is never unvalidated.

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

    %% Intake
    A[Unstructured Request<br/>email, chat, portal, multilingual]:::intake --> B[Generative Front Door<br/>normalize, translate, extract fields]:::aiLogic
    B --> C[Orchestration Supervisor Agent<br/>always-on controller, route selection,<br/>agent assignment, escalation watchpoints]:::complex

    %% Mandatory intake validation
    C --> D[Multi-agent Validation Squad<br/>intake triage: risk, compliance,<br/>commercial, category validation]:::complex
    D --> E{Complete enough<br/>and confidence acceptable?}:::aiLogic

    E -- No --> F[Kickback to requester<br/>or human clarification<br/>Trigger: ER-001]:::human
    E -- Yes --> G[Policy + Taxonomy Mapping<br/>category, threshold, restrictions]:::aiLogic

    %% Main routing
    G --> H{Marketplace Eligibility Gate<br/>standard item, low risk,<br/>below threshold, known specs?}:::aiLogic

    %% Marketplace lane
    H -- Yes --> I{Approved supplier / catalog<br/>available?}:::aiLogic
    I -- Yes --> J{Bundle opportunity exists?}:::aiLogic
    J -- Yes --> K{Can hold window apply<br/>without breaking SLA?}:::aiLogic
    K -- Yes --> L[Volume Aggregation Queue<br/>hold and consolidate demand]:::market
    K -- No --> O[Direct marketplace pricing]:::market
    J -- No --> O

    L --> L2{Bundled volume exceeds<br/>supplier monthly capacity?}:::aiLogic
    L2 -- Yes --> U[Dynamic Escalation Engine<br/>route to exact human title<br/>ER-006 → Sourcing Excellence Lead]:::human
    L2 -- No --> P[Match pricing tiers<br/>optimize volume discount]:::market
    O --> P

    %% Discovery branch
    I -- No --> Q[Supplier Discovery Trigger<br/>no approved supplier or catalog hit]:::complex
    Q --> R[Discovery Agent<br/>search alternates, form candidate set,<br/>prepare onboarding case]:::complex
    R --> S[Risk + Compliance Agents<br/>missing-data-aware provisional posture]:::complex
    S --> T[Onboarding + Compliance Procedure<br/>registration, documents, controls]:::complex
    T --> T2{Candidate viable enough<br/>for controlled comparison?}:::complex
    T2 -- No --> U
    T2 -- Yes --> V[Discovery candidate package<br/>pricing, risk, ESG, geography]:::complex

    %% Strategic lane
    H -- No --> W[Strategic Orchestration Intake]:::complex
    W --> X[Complex case package<br/>pricing, risk, ESG, geography]:::complex

    %% Universal mandatory validation layer before release/execution
    P --> Y[Multi-agent Validation Squad<br/>mandatory pre-release validation across all lanes]:::complex
    V --> Y
    X --> Y
    U --> Y

    Y --> Z{Needs exception,<br/>override, rework, or escalation?}:::complex
    Z -- Yes --> U
    Z -- No --> AA{Auto-approve threshold met?}:::aiLogic

    %% Release outcomes
    AA -- Yes --> AB[Auto-generate PO / final release package<br/>zero-touch only after multi-agent validation]:::market
    AA -- No --> AC[Lightweight approval routing<br/>human sign-off after multi-agent validation]:::human
    AC --> AB

    %% Final observer / auditor
    AB --> AD[Observer / Audit Agent<br/>cross-check consistency, evidence,<br/>rules, escalations, generated report]:::audit
    AD --> AE{Observer passes?}:::audit
    AE -- No --> AF[Return to supervisor<br/>for evidence gap closure / re-run]:::complex
    AF --> Y
    AE -- Yes --> AG[Execution handoff / auditable outcome]:::audit

    %% Audit log
    B --> AH[Audit log<br/>reason codes, rules, decisions, evidence]:::audit
    C --> AH
    D --> AH
    G --> AH
    L2 --> AH
    P --> AH
    R --> AH
    S --> AH
    T --> AH
    X --> AH
    Y --> AH
    U --> AH
    AB --> AH
    AD --> AH
    AG --> AH
```

## What changed

### 1. The multi-agent squad is now mandatory twice
- **At intake**, before the system even accepts the request as actionable
- **Before release/execution**, regardless of whether the case came from marketplace pricing, bundling, discovery, escalation, or strategic sourcing

### 2. Marketplace is no longer a bypass
In the previous version, direct marketplace pricing could reach approval logic without passing through the full multi-agent team.
Now both:
- `Direct marketplace pricing`
- `Volume aggregation / pricing tier match`

must pass through the same **mandatory pre-release validation squad**.

### 3. Discovery and escalation also converge into the same validation layer
Even when the system escalates or discovers a new supplier, the case still returns into the universal multi-agent validation checkpoint before it can move toward approval or execution.

## Implementation intent for the repo

This should translate into the backend as:

- `pipeline.py`
  - run a first multi-agent pass right after extraction
  - run a second multi-agent validation pass after lane-specific preparation and before recommendation/approval routing

- `orchestrator.py`
  - stop being treated as only the complex-case engine
  - become the universal validation and synthesis layer for every path

- `observer.py`
  - remain the final release gate after the universal multi-agent validation layer

## Simple rule to keep in mind

**No PO, no shortlist, no release package, and no human approval handoff should occur unless the multi-agent team has validated the case first.**
