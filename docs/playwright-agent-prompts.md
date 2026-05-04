# Major Playwright Agent Prompts

Use these prompts when running a Playwright test agent with limited quota. They intentionally focus on major production workflows instead of many small UI checks.

## Planner Agent Prompt

Create a concise Playwright E2E test plan for the AI Support Triage Console.

Scope only the three major production scenarios:

1. High risk: balance deducted and voucher missing.
2. Medium risk: campaign visible but inactive.
3. Low risk: voucher already issued.

For each scenario, validate only major business behavior:

- selected scenario and customer message
- intent
- risk
- decision
- human review requirement
- called APIs
- risk signals
- review ticket for high-risk only
- customer response includes the critical backend fact
- no internal JSON/API/agent/workflow language in the customer response

Also validate production signals once:

- LangGraph orchestration visible
- Policy Guardrails visible
- Trace ID visible
- intent mode, response mode, fallback used visible

Do not create pixel-level tests. Do not check exact LLM prose except for stable business facts.

## Generator Agent Prompt

Generate Playwright tests using the existing Page Object Model:

- spec: `tests/e2e/reward-support.spec.ts`
- page object: `tests/e2e/pages/supportTriagePage.ts`

Update the existing files only. Do not create a new spec file, a new page object file, or a duplicate test suite unless explicitly asked.

Add or update only major workflow tests. Keep one test per scenario. Use semantic selectors and page object methods. Do not duplicate low-level selectors inside the spec file.

The tests should be resilient to Streamlit DOM changes and should not assert dynamic values like trace IDs or latency.

## Healer Agent Prompt

Repair failing Playwright tests without weakening production behavior.

Work only in the existing Playwright files unless the user explicitly asks for a new file:

- `tests/e2e/reward-support.spec.ts`
- `tests/e2e/pages/supportTriagePage.ts`

Allowed changes:

- update Streamlit selectors
- improve waits
- move repeated selectors into the Page Object
- use regex for dynamic text

Do not remove assertions for:

- intent
- risk
- decision
- human review
- called APIs
- risk signals
- review ticket
- customer response facts
- guardrails and observability

If the app returns the wrong business outcome, report it as an application bug instead of healing the test.
