# Five-Minute Loom Script

## Goal

Record a clear five-minute walkthrough that shows product judgment, AI system design, prompt engineering discipline, and production thinking. Do not over-polish. Speak plainly.

## Screen Setup Before Recording

Open these in order before starting the Loom:

1. Browser: `http://127.0.0.1:8501`
2. IDE: `src/reward_support/orchestration/langgraph_workflow.py`
3. IDE: `src/reward_support/agents/decision_agent.py`
4. IDE: `docs/prompting.md`
5. IDE: `README.md`

Keep the app as the main screen. Only switch to code/docs when explaining architecture, prompts, or production readiness.

## Screenshot Practice Deck

Use these screenshots to rehearse the flow without rerunning the app:

| Moment | Screenshot | What to say |
|---|---|---|
| Opening | `assets/loom-01-first-screen.png` | "This is an AI support triage console. The first screen shows the main workflow: intent, risk, decision, human review, response, and timeline." |
| High-risk result | `assets/loom-02-high-risk-result.png` | "For a balance-deducted voucher-missing case, the system routes to human review instead of auto-resolving." |
| Evidence | `assets/loom-03-evidence.png` | "The decision is grounded in backend evidence: called APIs, risk signals, and review ticket data." |
| Observability | `assets/loom-04-observability.png` | "Every run has traceability: trace ID, LLM/fallback mode, fallback status, and latency per step." |
| Guardrails | `assets/loom-05-guardrails.png` | "The LLM interprets and drafts, but business decisions stay in deterministic policy and human review." |

## If OpenAI Quota Fails

If the API returns `429 insufficient_quota`, do not hide it. Say this plainly:

> I tested the real OpenAI path, and the key loads correctly, but this account is currently quota-limited. The important production behavior is that the workflow fails safe: it records the provider failure in the audit log and continues with deterministic fallback rules and response templates.

Then continue the demo in fallback mode. This is still a useful production signal because provider failure, rate limit, and quota exhaustion are real operational cases.

## 0:00 - 0:30 Problem

Screen: app first screen.

Hi Kyle, I built an AI support triage workflow for a reward redemption business.

The operational problem is common in support teams: customers report missing vouchers, expired campaigns, or balance deductions. Agents then have to read the ticket, check backend systems, decide whether the case is safe to automate, and write a response.

The point of this project is not to build a chatbot. It is to show how I would design an AI-assisted workflow that is grounded in backend data and keeps sensitive decisions in human review.

## 0:30 - 1:15 Data And Workflow

Screen: app first screen, point to the top workflow cards.

The workflow uses both unstructured and structured data.

The unstructured data is the customer message. The structured data comes from simulated backend services: Balance API, Voucher API, and Campaign API.

The key design choice is that the LLM never guesses whether a voucher exists or whether a balance was deducted. Those facts come from backend data. The LLM is used for language tasks, while business policy stays deterministic.

## 1:15 - 2:20 Agent Orchestration

Screen: briefly switch to `src/reward_support/orchestration/langgraph_workflow.py`, then back to app.

The workflow is orchestrated with LangGraph.

It has these nodes:

1. Intent Agent classifies the message using LLM plus fallback rules.
2. Data Agent calls the required backend APIs.
3. Risk Agent converts backend facts into risk signals.
4. Decision Agent applies business policy.
5. Human Review Agent runs only when the case requires review.
6. Response Agent drafts the customer-facing answer.

The important part is conditional routing. High-risk financial inconsistencies go through the Human Review Agent before a response is produced. Lower-risk cases continue directly to response generation.

## 2:20 - 3:20 Demo

Screen: app.

Select the high-risk scenario: balance deducted, voucher missing.

Click Run Workflow.

Point out:

- intent: reward issue
- risk: high
- decision: escalate to human
- human review: required
- LangGraph route includes Human Review
- timeline shows each step and mode
- review ticket is created
- evidence shows called APIs and risk signals

Then briefly switch to the medium-risk campaign case and low-risk voucher case to show that the route and decision change based on backend evidence.

## 3:20 - 4:10 Prompt And Guardrails

Screen: open `docs/prompting.md`, then app Guardrails accordion.

Explain that the system has prompt contracts and guardrails.

The Intent Agent expects strict JSON with an intent and confidence score. If the JSON is malformed, confidence is low, or the model is unavailable, it falls back to deterministic rules.

The Response Agent is grounded. It can only use workflow state and backend facts. It is instructed not to mention APIs, JSON, agents, internal workflow, refunds, or exact resolution times unless the workflow explicitly supports it.

There is also PII redaction before LLM-facing state.

## 4:10 - 4:40 Production End State

Screen: README architecture / Technical Decisions section.

In production, this would connect to real reward, voucher, campaign, and CRM systems.

I would persist workflow runs, prompt versions, review tickets, audit logs, and human edits. I would monitor fallback rate, escalation rate, latency per step, model usage, and how much agents edit the generated response.

I also added unit tests, integration tests, deterministic evals, Playwright E2E tests with a Page Object Model, and a CI workflow.

## 4:40 - 5:00 Business Impact

Screen: app result screen.

The business impact is straightforward.

Low-risk cases get faster responses. Medium-risk cases are flagged with evidence. High-risk cases are escalated with context. Support agents spend less time doing repetitive lookup work, and managers get an auditable decision trail.

This would get adopted because it does not ask the company to trust a black-box chatbot. It augments the existing support workflow with controls, evidence, and human review.

## Short Message To Send With The Loom

Hi Kyle,

Here is the Loom walkthrough: [LOOM_LINK]

I used a reward support triage workflow as the example and walked through the data, LangGraph orchestration, prompt guardrails, human-in-the-loop design, production architecture, tests, and business impact.

Thanks,
Husnuye
