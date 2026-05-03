#!/bin/bash
cd /Users/husnuye/ai-flight-voucher-demo
source venv/bin/activate
export OPENAI_API_KEY=sk-test-placeholder-for-testing
python -m streamlit run app/main.py --server.port 8501 --logger.level=error
