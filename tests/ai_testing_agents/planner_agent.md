# Planner Agent

## Mission

Create the test plan for the AI Reward Support Workflow before Playwright tests are generated.

The planner focuses on the product behavior, not implementation details. It should verify that the workflow behaves like the intended layered system:

| Layer | Owner | Purpose |
| --- | --- | --- |
| Intent | LLM + fallback rules | Understand the customer message |
| Data | backend APIs | Retrieve grounded backend facts |
| Risk | rules + signals | Classify safety and inconsistency level |
| Decision | rules engine | Select business action |
| Response | LLM + fallback templates | Produce a customer-facing answer |

## Inputs

- Streamlit app entry point: `app/main.py`
- Workflow service: `src/reward_support/application/workflow_service.py`
- Scenarios: `src/reward_support/config/scenarios.py`
- Eval dataset: `evals/eval_dataset.json`

## Required Test Coverage

### High Risk

Customer says balance was deducted but the flight voucher was not created.

Expected behavior:
- intent is `reward_issue`
- Balance API and Voucher API are used
- risk is `high`
- decision is `escalate_to_human`
- human review is required
- response clearly states that balance was deducted and voucher was not created

### Medium Risk

Customer sees a campaign but cannot redeem it.

Expected behavior:
- intent is `campaign_issue`
- Campaign API is used
- risk is `medium`
- decision is `flag_for_review`
- human review is not required, but review reason is shown
- response explains that the campaign is visible but inactive

### Low Risk

Customer cannot find an already issued voucher.

Expected behavior:
- intent is `reward_issue`
- Balance API and Voucher API are used
- risk is `low`
- decision is `auto_respond`
- human review is not required
- response tells the customer to check My Rewards and registered email

## Planning Rules

- Treat every scenario as independent.
- Start each scenario from a fresh app session.
- Prefer semantic checks over pixel-specific checks.
- Verify the user-visible decision summary and the observability/audit details.
- Do not require exact LLM wording except for business-critical facts.
- Include fallback-compatible expectations because the app can run without `OPENAI_API_KEY`.
- Validate production controls, not only happy-path UI behavior.
- Include checks for `intent_mode`, `response_mode`, fallback visibility, called APIs, risk signals, and review ticket behavior.
- Treat policy regressions as higher priority than visual regressions.

## Production Quality Gates

The plan should explicitly cover:

- **Grounding:** customer response must match backend evidence.
- **Policy control:** high-risk financial inconsistency must not auto-respond.
- **Fallback readiness:** workflow should still produce a safe result without an LLM key.
- **Observability:** trace ID, audit events, and modes must be visible.
- **Human review:** high-risk cases should create a review artifact.
- **Non-hallucination:** generated response must not invent refunds, deadlines, or backend facts.

## Output

The final plan should be a markdown test plan with:
- scenario title
- setup
- numbered steps
- expected results
- risk notes
