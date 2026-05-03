cat > testing/context/app-context.md <<'EOF'
# App Context

This is a Streamlit application for an AI-driven reward support workflow.

Local URL:
http://localhost:8501

The app simulates customer support automation for reward redemption issues.

Main user flow:
1. Select a demo backend scenario.
2. Review or edit the customer message.
3. Click "Run AI Workflow".
4. View the generated customer response.
5. View the agent/API trace.

Core workflow:
Intent Agent → Router Agent → Backend APIs → Risk Agent → Response Agent

Risk behavior:
- High Risk: balance deducted but voucher missing → escalate to human support.
- Medium Risk: campaign visible but inactive → flag campaign display issue.
- Low Risk: voucher already issued → auto response with voucher guidance.

Important:
The LLM is used only for response generation.
Business decisions are made by deterministic rules and structured backend data.
EOF

cat > testing/test-objectives.md <<'EOF'
# Test Objectives

The AI testing agent should autonomously explore and validate the Streamlit app.

Primary goals:
1. Discover the main UI flow.
2. Identify the available risk scenarios.
3. Generate a test plan.
4. Generate Playwright tests.
5. Run the tests.
6. Heal fragile selectors or assertions if failures occur.

Required scenarios:
- High Risk
- Medium Risk
- Low Risk

Validation rules:
- Do not rely on exact LLM wording.
- Use semantic validation.
- Confirm that a customer response is displayed.
- Confirm that the response meaning matches the selected scenario.
- Confirm that the workflow trace is available after execution.

Expected semantic signals:
- High Risk: balance deducted, voucher missing, escalation/support.
- Medium Risk: campaign inactive/expired, cannot redeem, display issue, balance unaffected.
- Low Risk: voucher issued, My Rewards, email/inbox/spam guidance.
EOF

cat > testing/agents/planner-agent.md <<'EOF'
# Planner Agent

You are the Planner Agent for AI-driven Playwright testing.

Your responsibilities:
1. Read the app context.
2. Explore the application using Playwright.
3. Identify critical user journeys.
4. Create a clear Markdown test plan.

Inputs:
- testing/context/app-context.md
- testing/test-objectives.md
- Running app at http://localhost:8501

Output:
- specs/reward-support-workflow.md

Rules:
- Do not write code yet.
- Focus on user intent, workflow behavior, and expected outcomes.
- Include positive paths and risk-based behavior.
- Do not assert exact generated LLM text.
- Prefer semantic expectations.
EOF

cat > testing/agents/generator-agent.md <<'EOF'
# Generator Agent

You are the Generator Agent for AI-driven Playwright testing.

Your responsibilities:
1. Read the generated test plan from specs/reward-support-workflow.md.
2. Generate Playwright tests.
3. Save the tests to tests/generated/reward-support.spec.ts.

Rules:
- Use Playwright Test with TypeScript.
- Use robust selectors where possible.
- Prefer role, label, and visible text selectors.
- Avoid brittle CSS selectors unless necessary.
- Do not assert exact LLM wording.
- Use semantic regular expressions for generated responses.
- Cover High Risk, Medium Risk, and Low Risk scenarios.

The app should be available at:
http://localhost:8501
EOF

cat > testing/agents/healer-agent.md <<'EOF'
# Healer Agent

You are the Healer Agent for AI-driven Playwright testing.

Your responsibilities:
1. Run the generated Playwright tests.
2. Inspect failures.
3. Determine whether the failure is caused by:
   - brittle selector
   - timing issue
   - overly strict assertion
   - real application bug
4. Repair tests when appropriate.
5. Report real application bugs separately.

Rules:
- Do not hide real product bugs by weakening tests too much.
- Prefer fixing selectors before changing assertions.
- Prefer semantic assertions over exact wording.
- Keep tests readable and maintainable.
- Save fixed tests to tests/generated/reward-support.spec.ts.
EOF

cat > testing/README.md <<'EOF'
# AI-Driven Testing Layer

This folder defines the AI-driven testing layer for the AI Reward Support Workflow project.

The goal is not only to write Playwright tests manually, but to use AI agents to plan, generate, run, and heal browser tests.

## Agent Model

Planner Agent:
- Explores the app.
- Creates a test plan.
- Saves the plan under specs/.

Generator Agent:
- Converts the plan into Playwright tests.
- Saves generated tests under tests/generated/.

Healer Agent:
- Runs tests.
- Fixes brittle selectors and weak assertions.
- Separates real app bugs from test issues.

## Workflow

1. Start the app:

```bash
streamlit run app/main.py