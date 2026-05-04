# Test Generator Agent

## Mission

Generate Playwright tests from the Planner Agent output for the Streamlit AI Reward Support Workflow.

The generated tests should prove that the UI exposes the same layered workflow contract used by the backend:

Intent → Data → Risk → Decision → Response

## Target

- App URL: the local Streamlit URL used during the test run
- Primary spec location: `tests/e2e/reward-support.spec.ts`
- Page object location: `tests/e2e/pages/supportTriagePage.ts`
- Test framework: Playwright

## Generation Rules

- Generate one focused test per planner scenario.
- Use role, label, and text locators where possible.
- Keep selectors resilient to Streamlit-generated DOM changes.
- Do not assert exact trace IDs or exact latency values.
- Do not assert full LLM response text. Assert stable business facts instead.
- Wait for visible workflow output after clicking `Run Workflow`.
- Prefer checks that match the product contract:
  - selected scenario
  - intent
  - risk level
  - decision
  - human review status
  - backend API/data evidence
  - risk signals
  - intent and response mode
  - fallback visibility
  - review ticket for high-risk scenarios
  - final response facts

## Scenario Mapping

### High Risk

Select `High Risk — Balance deducted, voucher missing`.

Required assertions:
- `reward_issue`
- `high`
- `escalate_to_human`
- `True`
- `balance_deducted`
- `voucher_missing`
- `pending_review`
- response mentions deducted balance and missing voucher

### Medium Risk

Select `Medium Risk — Expired campaign still visible`.

Required assertions:
- `campaign_issue`
- `medium`
- `flag_for_review`
- `False`
- `campaign_visible`
- `campaign_inactive`
- response mentions visible campaign and inactive/not redeemable state

### Low Risk

Select `Low Risk — Voucher already issued`.

Required assertions:
- `reward_issue`
- `low`
- `auto_respond`
- `False`
- `voucher_found`
- response mentions My Rewards or registered email

## Prompt Engineering Assertions

Generated tests should avoid evaluating prose style too narrowly. Check stable safety properties instead:

- no exact refund promise
- no exact resolution-time promise
- no mention of JSON, APIs, agents, or internal workflow in customer response
- response must include the critical backend fact for the selected scenario

## Output Rules

- Include a comment with the planner step before each Playwright action or assertion block.
- Keep tests deterministic and independent.
- Do not modify application code from this agent.
- If the app text changes but the behavior is intact, prefer robust locator updates over brittle text rewrites.
