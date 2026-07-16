# ADR-017-001 - Self Improvement Expansion

## Status

Accepted

## Date

2026-07-14

---

# Context

The LLM Data Intelligence System has evolved into a cognitive agent
architecture composed of:

- Reasoning;
- Decision Intelligence;
- Planning;
- Execution;
- Autonomy;
- Memory;
- Evaluation.

V1.16 introduced the Autonomy Layer, enabling the agent to observe execution
outcomes, generate reflections, extract learning signals, propose adaptation
strategies and store autonomous memories.

The V1.16 autonomy cycle is:

```text
Execution
|
v
Observation
|
v
Reflection
|
v
Learning Signal
|
v
Adaptation Strategy
|
v
Autonomy Decision
|
v
Memory
```

This established the foundation for experience-based agent improvement.

However, V1.16 does not yet define a dedicated architectural mechanism for
turning learning signals into governed, evaluated and traceable improvements
that can influence future behavior.

---

# Problem

The system can already learn from execution outcomes, but it still lacks a
formal self-improvement capability.

Without a dedicated Self Improvement Layer, the architecture risks:

- applying behavioral changes without explicit governance;
- mixing autonomy, decision and planning responsibilities;
- treating raw learning signals as direct behavior changes;
- losing traceability between evidence, proposed improvement and future impact;
- making future behavior difficult to validate or audit;
- weakening the controlled autonomy principles established in V1.16.

The architectural problem solved by V1.17 is the gap between:

```text
Learning from experience
```

and:

```text
Safely influencing future behavior based on validated improvement decisions
```

---

# Decision

Create a new architectural capability:

```text
Self Improvement Layer
```

The Self Improvement Layer will be positioned after the Autonomy Layer and
before controlled influence on future Decision, Planning or Routing behavior.

The layer is responsible for transforming learning signals into structured
improvement proposals, evaluating those proposals, applying governance policies
and producing improvement decisions.

The V1.17 flow is:

```text
Learning Signal
|
v
Improvement Proposal
|
v
Improvement Evaluation
|
v
Improvement Policy
|
v
Improvement Decision
|
v
Improvement Memory
|
v
Controlled Future Influence
```

Self Improvement does not execute tools, does not mutate active execution and
does not replace existing V1.16 contracts.

---

# Motivation

The Self Improvement Layer is created to preserve controlled autonomy while
allowing the platform to evolve toward continuous improvement.

The motivation is to provide:

- explicit governance for behavioral improvement;
- traceability from learning evidence to improvement decisions;
- separation between learning, deciding, planning and executing;
- a safe bridge between autonomy memory and future behavior;
- validation points for before-and-after improvement measurement;
- compatibility with the existing V1.16 autonomy architecture.

Autonomy answers:

```text
What did the agent learn from its behavior?
```

Self Improvement answers:

```text
Which learned improvements are valid, safe and allowed to influence future behavior?
```

---

# Agent Autonomy Limits

The agent must not change its behavior without evidence, evaluation and a
traceable decision.

The following limits are mandatory:

- Autonomy may generate learning signals and adaptation suggestions.
- Self Improvement may evaluate and approve improvement proposals.
- Self Improvement may only produce controlled influence for future behavior.
- Self Improvement may not execute tools directly.
- Self Improvement may not alter original data.
- Self Improvement may not mutate an execution already in progress.
- Critical or high-risk improvements may require human approval.
- Existing V1.16 autonomy contracts must remain backward compatible.

---

# Responsibility Boundaries

## Autonomy

Autonomy owns:

- observation creation;
- reflection generation;
- learning signal extraction;
- adaptation strategy proposal;
- autonomy decision creation;
- autonomy memory integration.

Autonomy does not govern long-term improvement application.

## Self Improvement Layer

Self Improvement owns:

- improvement proposal generation;
- improvement evaluation;
- improvement policy enforcement;
- improvement decision creation;
- improvement traceability;
- controlled future influence generation.

Self Improvement does not execute tools or rewrite active plans.

## Decision

Decision owns:

- alternative generation;
- alternative evaluation;
- decision selection;
- confidence analysis;
- decision explanation.

Decision may consume approved improvement influence, but it must continue to
work without self-improvement input.

## Planning

Planning owns:

- execution plan creation;
- goal-driven planning;
- dynamic planning;
- replanning strategy selection.

Planning may consume approved improvement influence for future plans, but it
must not consume raw learning signals directly.

## Execution

Execution owns:

- tool execution;
- execution state;
- execution events;
- execution feedback;
- execution lifecycle coordination.

Execution must not be directly controlled by Self Improvement.

## Memory

Memory owns:

- storage of learning signals;
- storage of improvement proposals;
- storage of improvement evaluations;
- storage of improvement decisions;
- storage of improvement traces.

Memory stores experience and decisions, but it does not evaluate behavior by
itself.

## Evaluation

Evaluation owns:

- measuring execution outcomes;
- validating improvement impact;
- supporting before-and-after analysis;
- identifying regressions caused by approved improvements.

Evaluation provides evidence, but it does not approve improvements.

---

# Architectural Flow

The continuous improvement flow is:

```text
Execution Result
|
v
Observation
|
v
Reflection Result
|
v
Learning Signal
|
v
Improvement Proposal
|
v
Improvement Evaluation
|
v
Improvement Policy
|
v
Improvement Decision
|
v
Improvement Memory
|
v
Controlled Influence Signal
|
v
Future Decision / Planning / Routing
```

Integrated architecture:

```text
Agent Controller
|
v
Agent Runtime
|
v
Reasoning Layer
|
v
Decision Intelligence
|
v
Planning System
|
v
Execution Engine
|
v
Autonomy Layer
|
v
Self Improvement Layer
|
v
Memory
|
v
Evaluation
|
v
Future Behavior Improvement
```

---

# Main Components

## ImprovementProposal

Represents a structured improvement proposal derived from one or more learning
signals.

Responsibilities:

- reference source learning signals;
- describe the proposed improvement;
- identify target layer and component;
- define expected benefit;
- define estimated risk;
- preserve evidence and metadata.

## ImprovementEvaluator

Evaluates an improvement proposal.

Responsibilities:

- assess evidence quality;
- assess expected impact;
- assess risk;
- estimate confidence;
- produce recommendations;
- indicate whether the proposal is eligible for approval.

## ImprovementPolicy

Applies governance rules to evaluated proposals.

Responsibilities:

- enforce confidence thresholds;
- enforce risk limits;
- require human approval when needed;
- reject unsafe proposals;
- prevent responsibility boundary violations.

## ImprovementDecision

Represents the decision about a proposed improvement.

Responsibilities:

- approve, reject or mark a proposal for review;
- record decision reason;
- record confidence;
- indicate approval requirements;
- preserve traceability.

Initial statuses:

```text
APPROVED
REJECTED
PENDING_REVIEW
EXPERIMENTAL
ROLLED_BACK
```

## ImprovementMemory

Stores improvement lifecycle artifacts.

Responsibilities:

- store proposals;
- store evaluations;
- store decisions;
- store traces;
- allow retrieval for audit and future validation.

---

# Compatibility With V1.16

V1.17 must preserve the V1.16 architecture and contracts.

The following contracts must remain valid:

- `AutonomyEngine` evaluates execution outcomes;
- `Observation` represents observed execution state;
- `ReflectionResult` represents autonomy reflection;
- `LearningSignal` represents learned experience;
- `AdaptationStrategy` represents proposed adaptation;
- `AutonomyDecision` represents autonomy control;
- `AutonomyMemory` stores autonomy decisions and learning signals.

Self Improvement extends the architecture after learning and memory. It does
not replace the existing autonomy lifecycle.

---

# Consequences

## Positive Consequences

- Learning becomes actionable without becoming uncontrolled.
- Improvement decisions become explicit and auditable.
- Responsibility boundaries remain clear.
- Future behavior can improve based on evidence.
- Risk and confidence become part of improvement governance.
- The platform gains a stronger foundation for continuous improvement.
- V1.16 autonomy remains backward compatible.

## Negative Consequences

- The architecture gains another cognitive layer.
- New contracts and tests are required.
- Improvement evaluation introduces additional design complexity.
- Memory must store more lifecycle artifacts.
- Future behavior becomes influenced by more context, requiring careful
  observability.

---

# Risks And Controls

## Risk: Uncontrolled Behavior Change

Control:

- require improvement proposals, evaluations and decisions;
- allow only controlled future influence;
- block direct execution by Self Improvement.

## Risk: Responsibility Mixing

Control:

- keep Autonomy, Self Improvement, Decision, Planning and Execution separated;
- prevent raw learning signals from directly changing plans or decisions.

## Risk: Low Quality Learning

Control:

- evaluate evidence strength;
- require confidence thresholds;
- reject low-confidence proposals.

## Risk: High-Risk Improvement Applied Automatically

Control:

- require approval for high-risk changes;
- support `PENDING_REVIEW` decision status.

## Risk: Regression In Future Behavior

Control:

- use Evaluation to compare before-and-after outcomes;
- store improvement traces;
- support rollback semantics for future releases.

---

# Validation Strategy

Validation must cover the complete self-improvement lifecycle.

## Unit Validation

Validate:

- `ImprovementProposal`;
- `ImprovementEvaluator`;
- `ImprovementPolicy`;
- `ImprovementDecision`;
- `ImprovementMemory`.

## Integration Validation

Validate:

- learning signal to improvement proposal;
- proposal to evaluation;
- evaluation to policy decision;
- decision to memory;
- approved decision to controlled influence.

## Regression Validation

Validate:

- V1.16 autonomy tests continue passing;
- existing decision and planning flows continue working without improvement
  input;
- execution behavior is not directly changed by Self Improvement;
- existing public contracts are preserved.

## Behavioral Validation

Validate:

- repeated failures can generate improvement proposals;
- low-confidence proposals are rejected;
- high-risk proposals require review;
- approved improvements influence only future behavior;
- evaluation can measure whether an improvement produced benefit.

---

# Alternatives Considered

## Alternative 1 - Extend Autonomy To Apply Improvements Directly

Rejected.

Reason:

Autonomy should observe, reflect and learn. Direct improvement application would
mix autonomy with governance and future behavior control.

## Alternative 2 - Store Learning In Memory And Let Decision Read It Directly

Rejected.

Reason:

Raw learning signals are not validated improvement decisions. Decision should
not consume ungoverned learning as behavioral instruction.

## Alternative 3 - Implement Self Improvement As A Dedicated Layer

Accepted.

Reason:

This preserves V1.16 boundaries while creating a governed, traceable and
testable bridge between learning and future behavior improvement.

---

# Status

ADR Accepted.

Next steps:

- define Self Improvement contracts;
- implement improvement domain components;
- integrate with autonomy memory;
- expose approved influence to future Decision and Planning flows;
- validate compatibility with V1.16;
- update architecture documentation and release notes.
