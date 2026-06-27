"""
Excel Formula Generator
A bilingual translator between plain English and Excel formulas.

Customisations beyond starter:
- Domain selector (General vs Finance & Accounting) that biases AI toward audit/accounting formulas
- Spreadsheet Helper mode: describe your data layout, get multiple formula recommendations
- Session history of last 5 queries
- Error handling for empty input and API failures
"""

import streamlit as st
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

# Load API key from .env in same folder as this file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Excel Formula Generator", page_icon="📊", layout="wide")
st.title("Excel Formula Generator")
st.caption("Built for finance and accounting professionals. Translate plain English to formulas, explain formulas, or get suggestions for your spreadsheet structure.")

if not API_KEY:
    st.error("No API key found. Check your .env file contains GOOGLE_API_KEY=your-key")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Initialise session state for query history
if "history" not in st.session_state:
    st.session_state.history = []


def add_to_history(mode, query, result):
    """Keep the last 5 queries in session state."""
    st.session_state.history.insert(0, {"mode": mode, "query": query, "result": result})
    st.session_state.history = st.session_state.history[:5]


def call_gemini(prompt):
    """Wrapper around Gemini call with error handling."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        st.error(f"Something went wrong calling the API: {e}")
        return None


# ---- Domain selector (top-level setting) ----
domain = st.radio(
    "Domain",
    ["General", "Finance & Accounting"],
    horizontal=True,
    help="Finance mode biases formulas toward what auditors, accountants, and analysts actually use (SUMIFS, XLOOKUP, XIRR, NPV, etc.)",
)

domain_context = ""
if domain == "Finance & Accounting":
    domain_context = """
The user is a finance or accounting professional (auditor, accountant, analyst, or consultant).
Prefer formulas they actually use in practice: SUMIFS, COUNTIFS, XLOOKUP, INDEX/MATCH, XIRR, NPV, IRR, PMT,
SUMPRODUCT, IFERROR-wrapped lookups, conditional formatting logic, pivot-table-style aggregations.
When relevant, mention audit considerations (e.g., why VLOOKUP is brittle, why SUMIFS beats SUMIF for multi-criteria).
Use realistic examples involving accounts, ledgers, revenue, expenses, dates, or GL codes."""

st.divider()

# ---- Mode selector ----
mode = st.radio(
    "What do you want to do?",
    ["English → Formula", "Formula → English", "Spreadsheet Helper"],
    horizontal=True,
)

# ---- Mode 1: English → Formula ----
if mode == "English → Formula":
    user_input = st.text_area(
        "Describe what you want",
        placeholder="Sum revenue in column D where the GL code in column A starts with '4' and the date in column B is in Q1 2025",
        height=100,
    )
    if st.button("Generate formula", type="primary"):
        if not user_input.strip():
            st.warning("Please describe what you want first.")
        else:
            with st.spinner("Thinking..."):
                prompt = f"""{domain_context}

You are an Excel formula expert. The user wants: {user_input}

Reply in exactly this format:
FORMULA: <the Excel formula, starting with =>
EXPLANATION: <2-3 sentences explaining how it works in plain English>"""

                output = call_gemini(prompt)
                if output:
                    if "FORMULA:" in output and "EXPLANATION:" in output:
                        formula = output.split("FORMULA:")[1].split("EXPLANATION:")[0].strip()
                        explanation = output.split("EXPLANATION:")[1].strip()
                        st.subheader("Formula")
                        st.code(formula, language="excel")
                        st.subheader("How it works")
                        st.write(explanation)
                        add_to_history(mode, user_input, formula)
                    else:
                        st.write(output)
                        add_to_history(mode, user_input, output[:200])

# ---- Mode 2: Formula → English ----
elif mode == "Formula → English":
    user_input = st.text_area(
        "Paste an Excel formula",
        placeholder="=SUMIFS(D:D, A:A, \">=\"&DATE(2025,1,1), A:A, \"<=\"&DATE(2025,3,31), B:B, \"REVENUE\")",
        height=100,
    )
    if st.button("Explain formula", type="primary"):
        if not user_input.strip():
            st.warning("Please paste a formula first.")
        else:
            with st.spinner("Thinking..."):
                prompt = f"""{domain_context}

Explain this Excel formula in plain English for a finance professional.
Break it down step by step. Then give one realistic example of when you'd use it.

Formula: {user_input}"""

                output = call_gemini(prompt)
                if output:
                    st.write(output)
                    add_to_history(mode, user_input, output[:200])

# ---- Mode 3: Spreadsheet Helper (the headline new feature) ----
else:
    st.markdown("Describe your spreadsheet layout and what you want to calculate. You'll get **three** different formula approaches with trade-offs.")

    col1, col2 = st.columns(2)
    with col1:
        structure = st.text_area(
            "Your spreadsheet structure",
            placeholder="Column A: Date\nColumn B: GL account code\nColumn C: Description\nColumn D: Amount (USD)\nRows 2-5000: transactions for FY2025",
            height=150,
        )
    with col2:
        goal = st.text_area(
            "What you want to calculate",
            placeholder="Total expenses (GL codes starting with 5) by month, with a check for any duplicate transactions over $10,000",
            height=150,
        )

    if st.button("Suggest formulas", type="primary"):
        if not structure.strip() or not goal.strip():
            st.warning("Please fill in both the structure and the goal.")
        else:
            with st.spinner("Thinking through the options..."):
                prompt = f"""{domain_context}

The user has this spreadsheet structure:
{structure}

They want to: {goal}

Suggest 3 different formula approaches. For each, use exactly this format:

OPTION <N>: <short name, e.g. "SUMIFS approach">
FORMULA: <the actual Excel formula>
TRADE-OFF: <one sentence on when this approach is best and what its weakness is>

After the 3 options, add:
RECOMMENDATION: <one paragraph picking the best option for this specific user and explaining why, considering audit/review requirements if relevant>"""

                output = call_gemini(prompt)
                if output:
                    st.markdown(output)
                    add_to_history(mode, goal[:60], "3 options generated")

# ---- Sidebar: session history ----
with st.sidebar:
    st.header("Recent queries")
    if not st.session_state.history:
        st.caption("Your recent queries will appear here.")
    else:
        for i, item in enumerate(st.session_state.history, 1):
            with st.expander(f"{i}. {item['mode']}"):
                st.caption("Query:")
                st.write(item["query"])
                st.caption("Result:")
                st.code(item["result"], language="excel")

    st.divider()
    st.caption("Built by [your name] · ICAEW student · [LinkedIn link]")