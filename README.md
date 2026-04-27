# AI Reward Support Workflow

This project demonstrates how an AI system can improve a real-world customer support workflow in a reward redemption system.

It focuses on handling common support cases such as missing vouchers, inactive campaigns, and user confusion.

---

## Workflow Overview

Customers contact support when something goes wrong.

Typical issues include:
- Missing voucher after balance deduction  
- Campaign visible but not active  
- User cannot find their voucher  

The goal is to:
- Understand the request  
- Check backend systems  
- Decide the correct action  
- Generate a clear response  

---

## System Design

The system is built as a decision-making workflow, not a simple chatbot.

It follows a structured flow:

1. **Intent Agent**  
   Identifies the customer’s intent from the message  

2. **Router Agent**  
   Decides which backend APIs or systems to use  

3. **Backend API Calls**  
   Fetches real data (balance, voucher, campaign)  

4. **Risk Agent**  
   Evaluates the risk level of the case  

5. **Response Agent**  
   Generates a clear and professional response  

---

## Data

The system uses both structured and unstructured data.

- **Unstructured data**: customer message  
- **Structured data**:  
  - Balance transactions  
  - Voucher records  
  - Campaign status  

All decisions are grounded in backend data.

---

## Decision Logic

The system does not rely on the LLM for decisions.

Instead:
- Rules + backend data determine outcomes  
- Risk level drives system behavior  

Risk levels:
- **Low risk** → automated response  
- **Medium risk** → response + flagged  
- **High risk** → escalated to human support  

---

## Human in the Loop

Human involvement is limited to high-risk scenarios.

This ensures:
- Safety in financial cases  
- Efficiency in simple cases  

---

## LLM Role

The LLM is used only to generate responses.

It does not:
- Make decisions  
- access business logic  

This keeps the system reliable and controllable.

---

## Tech Stack

- Python  
- Streamlit (UI)  
- LLM API (response generation)  
- Mock backend APIs  

---

## Production Vision

In a real-world system, this would connect to:

- Reward platforms  
- Voucher services  
- Campaign engines  
- CRM systems  

The orchestration layer would handle:
- API calls  
- Data validation  
- Error handling  
- Logging and monitoring  

---

## Business Impact

This system provides clear business value:

- Reduces support workload  
- Improves response time  
- Reduces operational cost  
- Allows teams to focus on complex issues  

---

## Run the App

To run the application locally:

```bash
pip install -r requirements.txt
streamlit run app.py

## Environment Setup

This project requires an API key to run.

Create a `.env` file in the root directory and add:

OPENAI_API_KEY=your_api_key_here

Make sure the `.env` file is not committed to version control.