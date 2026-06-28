# Excel Formula Generator

A bilingual translator between plain English and Excel formulas, built for finance and accounting professionals. Powered by Google's Gemini API.

> 🔗 **Live demo:** (https:excel-formula-generator-gankaili.streamlit.app/)

---

## What it does

This app helps finance and accounting professionals work with Excel formulas in three ways:

- **English → Formula** — Describe what you need in plain English, get the Excel formula with an explanation
- **Formula → English** — Paste a confusing formula, get a step-by-step breakdown
- **Spreadsheet Helper** — Describe your data layout and goal, get three different formula approaches with trade-offs and a recommendation

A **domain toggle** at the top switches between General mode and Finance & Accounting mode. Finance mode biases the AI toward formulas auditors actually use (SUMIFS, XLOOKUP, XIRR, IFERROR-wrapped lookups) and includes audit considerations in explanations.

---

## Why I built it

I'm an ICAEW student joining a Big Four firm as a consulting associate next year. Rather than just reading about AI's impact on professional services, I wanted to build something with it. Excel is the universal language of accounting and consulting work, so making formulas more accessible — especially complex ones — felt like a meaningful first project.

This is project one in a series I'm building to develop AI fluency before joining the firm.

---

## Tech stack

- **Python + Streamlit** — rapid UI prototyping without front-end overhead
- **Google Gemini 2.5 Flash API** — generation engine (free tier)
- **python-dotenv** — secure local config management

---

## What I customised beyond the starter

The starter version did basic English-to-formula translation. I extended it with features designed specifically for finance and accounting workflows:

**Domain-aware prompts.** A toggle injects domain-specific instructions into every Gemini call. In Finance mode, the model biases toward formulas auditors actually use and mentions audit considerations (e.g., why VLOOKUP is brittle for production workbooks).

**Spreadsheet Helper mode.** Users describe their data structure (columns, row ranges, data types) and goal. The model returns three different formula approaches with explicit trade-offs and a recommendation. This mirrors how a senior consultant would think through a client's problem — not just "here's the formula" but "here are three approaches and why this one fits your situation."

**Session history.** A sidebar shows the last 5 queries, expandable to see full query and result. Useful for comparing approaches across iterations.

**Error handling.** All Gemini calls are wrapped in a single function with try/except. API failures and empty input no longer crash the app.

---

## Design decisions worth flagging

- **Provider-agnostic structure.** The Gemini API call lives in one isolated function. Swapping to Claude, GPT, or a local Ollama model is a one-function change. This reflects a real enterprise concern about vendor lock-in in AI deployments.
- **Prompt as injected context, not template.** Domain instructions are injected as runtime context rather than hardcoded into separate prompts. Adding a new domain (e.g., "Tax" or "Audit-specific") would take only a few lines.

---

## Run it locally

1. Clone this repo and `cd` into it
2. Create a virtual environment:
python -m venv venv
3. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
pip install -r requirements.txt
5. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
6. Create a `.env` file in the project root:
GOOGLE_API_KEY=your-key-here
7. Run the app:
streamlit run app.py
---

## What I learned

- Working with LLM APIs and structured prompt design — getting reliably parseable output is harder than it looks
- The difference between a generic AI tool and a domain-specific one is mostly in the prompt, not the model
- Streamlit's session state for building stateful single-page apps
- API key management and security hygiene — never commit secrets, always use `.gitignore`
- Where Gemini Flash succeeds and fails on accounting formulas (see Limitations)

---

## Limitations

- Complex array formulas occasionally have syntax errors that look correct at a glance
- The app doesn't validate formulas against an actual Excel engine — outputs should be tested before use in production workbooks
- Finance mode bias is prompt-based, not training-based, so very niche accounting standards may not be handled accurately

---

## What's next

- Deploy to Streamlit Community Cloud for a public live demo
- Add Google Sheets formula support (slightly different syntax)
- Build a small library of accounting-specific test cases to benchmark accuracy
- Add a "show me the audit risk" mode that flags formulas auditors should question

---

## About me

I'm an ICAEW student preparing to start as a consulting associate at a Big Four firm. I'm building a series of AI-powered tools to develop fluency in applied LLMs before joining.

- 💼 [LinkedIn](https://www.linkedin.com/in/gan-kai-li-a8a782317/)
- 📧 gankaili88@gmail.com
