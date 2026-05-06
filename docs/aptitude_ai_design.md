# Aptitude AI Design

## Objective

Add cognitive and situational evaluation to the HR interview so recruiters can assess how clearly a candidate reasons, prioritizes, and handles workplace ambiguity.

## Question design

The aptitude layer generates two question groups:

- **Reasoning-based questions**: prioritization, root-cause analysis, assumptions, trade-offs, and evidence.
- **Situational judgment scenarios**: workplace ambiguity, stakeholder communication, ethical risk, escalation, and decision clarity.

Questions are adapted by:

- **Role type**: technical roles focus on delivery, technical debt, code review, architecture, and engineering trade-offs; non-technical roles focus on clients, operations, cross-functional work, and commitments.
- **Experience level**: freshers receive project/internship scenarios; experienced candidates receive workplace ownership and stakeholder scenarios.

## Ideal answer structure

Each aptitude question carries an ideal answer rubric:

- clarify facts and constraints
- state assumptions
- compare options by impact and risk
- explain evidence used
- choose a clear action
- communicate the decision to relevant stakeholders
- document or measure the outcome when appropriate

## Logical reasoning scoring model

The model scores three dimensions:

- **Logical thinking, 45%**: assumptions, evidence, cause-effect reasoning, trade-offs, and conclusion quality.
- **Problem-solving clarity, 35%**: structured steps, sequencing, concise explanation, and actionability.
- **Situational judgment, 20%**: stakeholder awareness, risk handling, transparency, and escalation judgment.

## Scenario evaluation framework

Positive signals:

- evidence-based decision-making
- balanced urgency and ethics
- clear stakeholder communication
- structured prioritization
- risk mitigation

Risk flags:

- unsupported conclusions
- missing stakeholders
- vague or very short answers
- no trade-off discussion
- no risk mitigation
- hiding or ignoring issues

Implementation lives in `zecpath_hiring.ai.hr_interview.aptitude_evaluator`.
