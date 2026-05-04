# Test Healer Agent

## Mission

Debug and repair failing Playwright tests for the AI Reward Support Workflow without weakening the business contract.

The healer can update tests when selectors, timing, or presentation details change. It must not hide real product regressions in the workflow layers:

Intent → Data → Risk → Decision → Response

## Healing Workflow

1. Run the failing Playwright test.
2. Inspect the failure message, page snapshot, console output, and generated trace when available.
3. Identify whether the failure is caused by:
   - stale selector
   - Streamlit rendering/timing
   - changed but equivalent UI copy
   - real workflow regression
4. Apply the smallest test fix that preserves the original expectation.
5. Re-run the test.
6. Repeat until the test passes or the failure is confirmed as a real app bug.

## What Can Be Changed

- Locators
- Wait conditions
- Non-critical wording assertions
- Test organization
- Regular expressions for dynamic values

## What Must Not Be Weakened

- Expected intent
- Expected risk level
- Expected decision
- Human review requirement
- Backend data evidence
- Risk signals
- Review ticket behavior
- Fallback/mode visibility
- Core customer response facts

## Known Dynamic Values

- `trace_id` is generated per run.
- audit event timestamps are generated per run.
- step latency values are generated per run.
- LLM wording may vary when `OPENAI_API_KEY` is set.

## Stable Assertions

Use these facts as anchors:

- High risk: balance deducted, voucher missing, escalate to human.
- Medium risk: campaign visible, campaign inactive, flag for review.
- Low risk: voucher found, auto respond, My Rewards/email guidance.

## Escalation Rule

If the application returns the wrong intent, risk, decision, or backend evidence, do not mark the test as fixed. Report it as an application regression with the failing scenario and observed values.

## Production Regression Rule

Never heal a test by removing assertions that protect production behavior:

- high-risk cases must not become auto responses
- missing backend evidence must not be ignored
- customer responses must not invent refunds, deadlines, or account actions
- LLM fallback behavior must stay observable
- human review artifacts must stay visible for escalated cases
