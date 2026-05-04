# Prompting And LLM Guardrails

## Design Principle

The LLM is not the system of record and does not own business policy. It is used for language-heavy tasks:

- intent interpretation
- customer-facing response drafting

Structured backend facts and deterministic rules own:

- voucher existence
- balance deduction status
- campaign activity
- risk level
- escalation decision
- human review requirement

## Intent Prompt Contract

Versioned artifact: `prompts/intent_classifier_v1.md`

The Intent Agent asks the model to return one valid JSON object:

```json
{
  "intent": "one_of_the_valid_intents",
  "confidence": 0.0
}
```

Allowed intents:

- `reward_issue`
- `campaign_issue`
- `balance_issue`
- `refund_request`
- `general_support`

Production safeguards:

- parse JSON defensively
- extract JSON object if the model adds surrounding text
- reject unknown intents
- clamp confidence between `0` and `1`
- reject low-confidence classifications
- fallback to deterministic rules when model calls fail

## Response Prompt Contract

Versioned artifact: `prompts/response_agent_v1.md`

The Response Agent receives:

- customer message
- intent
- risk level
- decision
- human review reason
- backend data

The model is instructed to:

- use only provided workflow state and backend data
- never invent account facts
- never mention JSON, APIs, agents, orchestration, or workflow state
- never make unsupported promises
- never promise exact resolution times
- end with a consistent support closing

## Why Exact Text Is Not The Eval Target

LLM prose can vary. The test strategy checks stable business facts instead:

- high-risk response says balance was deducted and voucher was not created
- campaign response says campaign is visible but inactive/not redeemable
- low-risk response points to My Rewards and registered email
- no response promises refunds or exact resolution times
- no response exposes internal implementation details

## Failure Modes Considered

| Failure mode | Guardrail |
| --- | --- |
| model unavailable | deterministic fallback |
| malformed JSON | defensive parsing and fallback |
| low confidence | reject to safe default |
| hallucinated backend fact | response prompt limits source of truth |
| unsafe automation | decision agent owns policy |
| financial inconsistency | human review route |
| PII sent to model | redaction before LLM-facing state |

## Production Extensions

- prompt version registry
- offline prompt eval by scenario
- human edit-distance tracking
- PII redaction before model calls
- model gateway with logging and rate limits
- response quality scoring against backend facts
