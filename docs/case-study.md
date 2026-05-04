# Case Study: AI Support Triage Console

## Summary

Customer support teams spend a lot of time investigating repetitive reward redemption issues. The hard part is not writing a polite answer. The hard part is deciding what can be safely automated, what needs backend validation, and what must remain in human review.

This project designs a production-style AI workflow for that problem. It uses an LLM for language tasks, deterministic rules for business decisions, simulated backend APIs for grounding, and a human review path for high-risk cases.

## Workflow Chosen

The workflow is reward support triage:

1. A customer reports a voucher or campaign issue.
2. The system classifies the message intent.
3. The system calls the relevant backend APIs.
4. The system evaluates risk from structured facts.
5. The system chooses the business action.
6. High-risk cases route through a dedicated human review node.
7. The system drafts the support response.

## Data Used

### Unstructured Data

- customer support message
- generated customer response
- audit log explanations

### Structured Data

- balance transaction status
- voucher existence and delivery status
- campaign visibility and active state
- risk level
- decision outcome
- human review status
- trace ID and step latency

The key design choice is that the LLM never has to guess whether a voucher exists. That comes from the backend data layer.

## Agent Design

### Intent Agent

Classifies messages into supported intents such as `reward_issue`, `campaign_issue`, `balance_issue`, `refund_request`, and `general_support`.

Production judgment:
- validate JSON output
- clamp confidence between `0` and `1`
- reject low-confidence LLM results
- fallback to deterministic rules when the model or network is unavailable

### Data Agent

Routes the workflow to the required backend APIs:
- Balance API
- Voucher API
- Campaign API

Production judgment:
- track `required_apis`
- separate data retrieval from decision making
- make backend evidence visible in the UI

### Risk Agent

Converts backend facts into risk level and risk signals.

Examples:
- `balance_deducted` + `voucher_missing` -> high risk
- `campaign_visible` + `campaign_inactive` -> medium risk
- `voucher_found` -> low risk

Production judgment:
- keep risk rules explicit
- output explainable `risk_signals`
- preserve a human-readable review reason

### Decision Agent

Applies business policy:
- low risk -> `auto_respond`
- medium risk -> `flag_for_review`
- high risk -> `escalate_to_human`

Production judgment:
- the LLM does not own policy decisions
- every decision has a reason
- high-risk financial inconsistencies stay in human review

### Response Agent

Writes the final customer-facing message.

Production judgment:
- only use provided workflow state and backend facts
- do not expose APIs, JSON, agents, or internal orchestration
- do not promise exact resolution times
- fallback templates exist for all core paths

## Human-In-The-Loop

The system keeps humans in the loop when:

- balance was deducted but voucher was not created
- refund or financial policy exception is requested
- backend data is missing or inconsistent
- intent is uncertain

The simulated production behavior is a `review_ticket` with:

- ticket ID
- priority
- status
- reason
- assigned queue

In a real deployment this would integrate with Zendesk, Salesforce Service Cloud, Intercom, Jira Service Management, or an internal queue.

## Conditional LangGraph Routing

The LangGraph workflow is intentionally not just a linear chain. After the Decision Agent, the graph routes based on state:

```text
Decision Agent
  ├─ requires_human_review = true  -> Human Review Agent -> Response Agent
  └─ requires_human_review = false -> Response Agent
```

This mirrors a real production pattern: the model-assisted workflow can automate low-risk cases while preserving review gates for financial or policy-sensitive cases.

## Production Architecture

In production, this would become:

- frontend: internal support console
- orchestration: LangGraph or durable workflow engine
- LLM gateway: model routing, prompt versioning, content safety, logging
- data integrations: reward ledger, voucher service, campaign service, CRM
- storage: workflow runs, audit logs, review tickets, prompt versions
- monitoring: latency, fallback rate, escalation rate, agent edit rate, decision accuracy
- security: RBAC, PII redaction, tenant isolation, audit retention

## Evaluation Strategy

The current eval checks:

- intent accuracy
- risk accuracy
- decision accuracy

Production eval would add:

- larger historical ticket set
- adversarial and ambiguous messages
- regression tests per policy change
- response quality scoring
- hallucination checks against backend facts
- human edit distance on drafted responses

## Business Impact

What gets faster:
- support triage
- backend investigation
- first response drafting

What gets cheaper:
- repetitive voucher lookup cases
- manual campaign issue investigation
- support agent time spent writing standard responses

What gets better:
- consistent policy decisions
- auditability
- escalation quality
- customer response clarity

Why it would get adopted:
- it augments support agents instead of replacing them
- it is grounded in backend facts
- it keeps sensitive cases in human review
- it produces observable decisions that managers can trust

## What I Would Build Next

1. Persist workflow runs and review tickets.
2. Add real CRM/ticketing integration.
3. Add PII redaction before LLM calls.
4. Add a prompt registry with prompt versions and eval history.
5. Add Playwright E2E tests for all three scenarios.
6. Add production dashboards for fallback rate, latency, escalation rate, and review outcomes.
