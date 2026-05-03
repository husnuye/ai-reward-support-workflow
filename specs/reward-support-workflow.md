# AI Reward Support Workflow Test Plan

## Overview
This test plan covers the AI Reward Support Workflow Streamlit application, which demonstrates an AI-driven customer support system for reward redemption issues. The application uses multiple agents to process customer inquiries and generate appropriate responses based on risk assessment.

## Test Scope
- **In Scope**: UI functionality, workflow execution, scenario handling, response generation, agent trace display
- **Out of Scope**: Backend API implementation, LLM accuracy, actual customer data processing

## Test Environment
- **Application URL**: http://localhost:8502
- **Browser**: Chrome (via Playwright)
- **Test Framework**: Playwright
- **Validation Approach**: Semantic validation (no reliance on exact LLM wording)

## UI Structure Analysis

### Main Components Identified:
1. **Header Section**: "AI Reward Support Workflow" title and subtitle
2. **Workflow Steps Panel** (Left sidebar):
   - Lists 5 agent steps: Intent Agent, Router Agent, Backend APIs, Risk Agent, Response Agent
   - Shows system status as "Operational"
   - Displays "Simulated APIs + LLM response agent"
3. **Main Content Area** (Right side):
   - Scenario selection dropdown ("Demo backend state")
   - Customer message textarea
   - "Run AI Workflow" button
   - Dynamic response display area
   - Agent/API trace expandable sections

## Test Scenarios

### TS-001: Page Load and Initial State
**Objective**: Verify the application loads correctly and displays expected initial state

**Preconditions**:
- Application is running at http://localhost:8502

**Steps**:
1. Navigate to http://localhost:8502
2. Wait for page to fully load

**Expected Results**:
- Page title displays "AI Reward Support Workflow"
- Header shows "AI Reward Support Workflow" and subtitle
- Left panel shows all 5 workflow steps
- System status shows "● Operational"
- Scenario dropdown is visible with a default selection
- Customer message textarea is visible with default text
- "Run AI Workflow" button is visible and enabled
- No response or trace sections are initially displayed

### TS-002: Scenario Selection - High Risk
**Objective**: Verify high risk scenario selection and associated behavior

**Preconditions**:
- Application is loaded (TS-001 passed)

**Steps**:
1. Click on the scenario dropdown
2. Select "High Risk — Balance deducted, voucher missing (Balance transaction exists, but voucher record is missing.)"
3. Verify the selection is applied

**Expected Results**:
- Dropdown closes after selection
- Selected scenario text is displayed
- Customer message textarea updates to: "My balance was deducted but my flight voucher was not created."

### TS-003: Scenario Selection - Medium Risk
**Objective**: Verify medium risk scenario selection and associated behavior

**Preconditions**:
- Application is loaded (TS-001 passed)

**Steps**:
1. Click on the scenario dropdown
2. Select "Medium Risk — Expired campaign still visible (Campaign is visible but inactive in backend.)"
3. Verify the selection is applied

**Expected Results**:
- Dropdown closes after selection
- Selected scenario text is displayed
- Customer message textarea updates to: "I can still see the flight voucher campaign, but I can't redeem it."

### TS-004: Scenario Selection - Low Risk
**Objective**: Verify low risk scenario selection and associated behavior

**Preconditions**:
- Application is loaded (TS-001 passed)

**Steps**:
1. Click on the scenario dropdown
2. Select "Low Risk — Voucher already issued (Voucher exists and is available to the user.)"
3. Verify the selection is applied

**Expected Results**:
- Dropdown closes after selection
- Selected scenario text is displayed
- Customer message textarea updates to: "I redeemed a $500 flight voucher, but I can't find it."

### TS-005: High Risk Workflow Execution
**Objective**: Verify complete workflow execution for high risk scenario

**Preconditions**:
- High risk scenario is selected (TS-002 passed)

**Steps**:
1. Click "Run AI Workflow" button
2. Wait for workflow completion
3. Expand all agent trace sections

**Expected Results**:
- Button shows loading state during execution
- Customer response section appears with professional response
- Response acknowledges the balance deduction issue
- Response mentions escalation to support team
- Agent trace shows all 5 steps executed
- Risk assessment shows "high" risk level
- Action shows "escalate"
- At least one trace section shows ticket creation

### TS-006: Medium Risk Workflow Execution
**Objective**: Verify complete workflow execution for medium risk scenario

**Preconditions**:
- Medium risk scenario is selected (TS-003 passed)

**Steps**:
1. Click "Run AI Workflow" button
2. Wait for workflow completion
3. Expand all agent trace sections

**Expected Results**:
- Button shows loading state during execution
- Customer response section appears with professional response
- Response explains campaign expiration
- Response mentions display issue will be corrected
- Agent trace shows all 5 steps executed
- Risk assessment shows "medium" risk level
- Action shows "flag_campaign_display_issue"

### TS-007: Low Risk Workflow Execution
**Objective**: Verify complete workflow execution for low risk scenario

**Preconditions**:
- Low risk scenario is selected (TS-004 passed)

**Steps**:
1. Click "Run AI Workflow" button
2. Wait for workflow completion
3. Expand all agent trace sections

**Expected Results**:
- Button shows loading state during execution
- Customer response section appears with professional response
- Response confirms voucher exists
- Response provides guidance on finding the voucher
- Agent trace shows all 5 steps executed
- Risk assessment shows "low" risk level
- Action shows "auto_respond"

### TS-008: Custom Message Input
**Objective**: Verify ability to modify customer message

**Preconditions**:
- Application is loaded (TS-001 passed)

**Steps**:
1. Click in the customer message textarea
2. Clear existing text
3. Type custom message: "I need help with my rewards balance"
4. Click "Run AI Workflow" button
5. Wait for workflow completion

**Expected Results**:
- Textarea accepts input
- Custom message is processed
- Workflow executes successfully
- Response addresses the custom message content

### TS-009: Agent Trace Expandability
**Objective**: Verify agent trace sections can be expanded and collapsed

**Preconditions**:
- Any workflow has been executed (TS-005, TS-006, or TS-007 passed)

**Steps**:
1. Locate agent trace sections
2. Click to expand each trace section
3. Verify content is displayed
4. Click to collapse sections
5. Verify content is hidden

**Expected Results**:
- All trace sections start collapsed
- Clicking expands sections to show JSON data
- Clicking again collapses sections
- Content is properly formatted JSON

### TS-010: Response Display Validation
**Objective**: Verify response display formatting and content structure

**Preconditions**:
- Any workflow has been executed (TS-005, TS-006, or TS-007 passed)

**Steps**:
1. Locate customer response section
2. Examine response content and formatting

**Expected Results**:
- Response is displayed in a styled card/box
- Response contains appropriate acknowledgment
- Response provides clear explanation
- Response includes next steps or resolution
- Response ends with professional closing
- No technical jargon (APIs, JSON, etc.) is exposed

## Test Data Requirements

### Default Scenario Messages:
- **High Risk**: "My balance was deducted but my flight voucher was not created."
- **Medium Risk**: "I can still see the flight voucher campaign, but I can't redeem it."
- **Low Risk**: "I redeemed a $500 flight voucher, but I can't find it."

### Custom Test Messages:
- Balance inquiry: "How much is in my rewards balance?"
- Voucher status: "Where can I find my voucher?"
- Campaign question: "Why can't I redeem this offer?"

## Success Criteria
- All test scenarios pass without errors
- UI elements are properly accessible and functional
- Workflow execution completes within reasonable time (< 30 seconds)
- Responses are contextually appropriate for each scenario
- Agent traces show complete execution of all 5 agents
- Risk assessments match expected levels for each scenario

## Risk Assessment
- **High**: Interface elements not accessible, workflow fails to execute
- **Medium**: Response content doesn't match scenario expectations, trace display issues
- **Low**: Minor UI styling issues, performance concerns

## Test Execution Notes
- Tests should be run in sequence due to state dependencies
- Allow time for LLM response generation (may take 5-10 seconds)
- Use semantic validation rather than exact text matching for responses
- Capture screenshots on failures for debugging
- Reset application state between test runs if needed