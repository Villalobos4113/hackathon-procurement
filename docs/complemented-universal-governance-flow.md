# Complemented Universal Governance Flow

This version merges the **universal multi-agent validation architecture** with the **governance and decision-quality flow**.

## What this adds

Relative to the universal validation flow, this version introduces:

- a **Deterministic Constraint Snapshot** early in the process
- a **Decision Workspace** where hard rules and agent outputs are fused
- a **Critic Agent** to challenge assumptions and evidence quality
- a **Judge Agent** to resolve conflicts and set final routing/ranking
- a **Reviewer Agent** to score trace quality and consistency
- a **Feedback Learning Loop** to calibrate critic and judge behavior over time

## Key design principle

The multi-agent team remains **mandatory across all processes**.
Nothing can move to PO, approval routing, supplier onboarding outcome, or escalation handoff unless it has passed through:

1. intake triage validation
2. lane-specific preparation
3. universal pre-release multi-agent validation
4. governance review by critic, judge, and reviewer

## Complemented Mermaid flow

```mermaid
graph TD
    classDef intake fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef ai fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef det fill:#f1f8e9,stroke:#689f38,stroke-width:2px;
    classDef agent fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef gov fill:#ede7f6,stroke:#673ab7,stroke-width:2px;
    classDef human fill:#ffebee,stroke:#f44336,stroke-width:2px;
    classDef audit fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px;

    %% Intake
    A[Unstructured Request<br/>email, chat, portal, multilingual]:::intake
      --> B[Generative Front Door<br/>normalize, translate, extract fields]:::ai
      --> C[Deterministic Constraint Snapshot<br/>taxonomy, policy, thresholds, restrictions,<br/>required fields, SLA]:::det
      --> D[Orchestration Supervisor Core<br/>always-on controller, route selection,<br/>watchpoints, re-run ownership]:::agent

    %% Mandatory intake validation
    D --> E[Multi-Agent Validation Squad<br/>mandatory intake triage:<br/>historical, risk, value, strategic]:::agent
    D --> F[Critic Agent<br/>challenge assumptions, evidence, bias,<br/>missing-data confidence]:::gov

    C --> G[Decision Workspace<br/>hard constraints + agent outputs combined]:::ai
    E --> G
    F --> G

    G --> H{Complete enough<br/>and confidence acceptable?}:::ai
    H -- No --> I[Kickback to requester<br/>or human clarification<br/>Trigger: ER-001]:::human
    H -- Yes --> J{Marketplace eligible?<br/>standard item, low risk,<br/>below threshold, known specs?}:::ai

    %% Catalog lane
    J -- Yes --> K{Approved supplier / catalog available?}:::ai
    K -- Yes --> L[Catalog Evaluation Module<br/>fit, pricing, spec match, supplier quality]:::agent
    L --> M{Bundle opportunity?}:::ai
    M -- Yes --> N[Demand Aggregation / Volume Optimization Module]:::agent
    M -- No --> O[Direct Fulfillment Recommendation Module]:::agent

    %% Discovery lane
    K -- No --> P[New Supplier Discovery Module<br/>find candidates, evaluate fit,<br/>exploratory risk on sparse data]:::agent
    P --> Q[Supplier Evaluation + Provisional Onboarding Module]:::agent

    %% Strategic lane
    J -- No --> R[Strategic Orchestration Module<br/>complex case packaging,<br/>pricing, risk, ESG, geography]:::agent

    %% Universal mandatory pre-release validation
    N --> S[Universal Multi-Agent Validation Layer<br/>mandatory pre-release validation<br/>across all lanes]:::agent
    O --> S
    Q --> S
    R --> S

    %% Governance and approval
    S --> T[Threshold / Approval Module<br/>deterministic enforcement + agentic scrutiny]:::agent
    T --> U{Blocking issue from deterministic rules?}:::det
    U -- Yes --> V[Escalation / Human Review Path<br/>route to exact human title]:::human
    U -- No --> W[Judge Agent<br/>de-bias orchestrator, resolve conflicts,<br/>set final ranking and routing]:::gov
    V --> W

    W --> X[Reviewer Agent<br/>score decision quality, consistency,<br/>trace completeness]:::gov
    X --> Y[Feedback Learning Loop<br/>critic and judge calibration memory]:::gov

    %% Final audit gate
    Y --> Z[Observer / Audit Agent<br/>cross-check consistency, evidence,<br/>rules, escalations, generated package]:::audit
    Z --> AA{Observer passes?}:::audit
    AA -- No --> AB[Return to supervisor<br/>for evidence gap closure / re-run]:::agent
    AB --> S
    AA -- Yes --> AC[Final Output<br/>PO / approval route / escalation / onboarding]:::ai

    %% Audit log
    B --> AD[Audit Log<br/>rules, evidence, agent opinions, critic findings,<br/>judge rulings, reviewer feedback]:::audit
    C --> AD
    E --> AD
    F --> AD
    G --> AD
    L --> AD
    N --> AD
    O --> AD
    P --> AD
    Q --> AD
    R --> AD
    S --> AD
    T --> AD
    V --> AD
    W --> AD
    X --> AD
    Y --> AD
    Z --> AD
    AC --> AD
```

## Why this works better

### 1. The second flow now strengthens, not replaces, universal validation
Your earlier requirement remains intact:
- the multi-agent squad is present at intake
- the multi-agent squad is present again before release
- no lane bypasses it

### 2. The critic, judge, and reviewer now have clean roles
- **Critic** questions assumptions before the workflow hardens
- **Judge** arbitrates after deterministic enforcement and escalation signals are known
- **Reviewer** checks whether the final decision is actually high quality and auditable

### 3. Decision quality is separated from execution speed
Catalog and marketplace flows can stay fast, but they still go through:
- decision workspace
- universal validation
- judge/reviewer governance
- observer gate

### 4. Deterministic and agentic controls are clearly separated
- deterministic layer decides hard constraints and blocking rules
- agentic layer evaluates nuance, tradeoffs, sparse data, and strategic fit
- governance layer challenges and resolves the final decision

## Recommended language for presentation

A simple way to explain this architecture is:

> Every request enters through a generative front door, is grounded by deterministic procurement constraints, challenged by a multi-agent team and critic, routed through the right fulfillment lane, then forced back through a universal validation and governance stack before any PO, approval, escalation, or onboarding outcome is released.

## Suggested implementation mapping

- `extractor.py`
  - front door normalization and extraction
- `rule_engine.py`
  - deterministic constraint snapshot and blocking rules
- `orchestrator.py`
  - always-on multi-agent squad and synthesis
- `supplier_discovery.py`
  - new supplier discovery and provisional onboarding path
- `observer.py`
  - final audit gate
- future modules to add:
  - `critic_agent.py`
  - `judge_agent.py`
  - `reviewer_agent.py`
  - `decision_workspace.py`
  - `learning_loop.py`
