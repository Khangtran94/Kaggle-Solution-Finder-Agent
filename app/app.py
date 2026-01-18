import asyncio
import streamlit as st
from pydantic_ai import Agent

from ingest import (
    read_repo_data,
    extract_completed_competitions,
    build_vector_index,
)
from search_agent import create_search_agent
from logs import (
    log_interaction_to_file,
    load_log_file,
    evaluate_log_record,
    EvaluationChecklist,
)

# ---------------------------------------------
# App config
# ---------------------------------------------
st.set_page_config(
    page_title="Kaggle Project Search Agent",
    layout="wide",
)

st.title("🔍 Kaggle Competition Search Agent")
st.caption("Search and explore completed Kaggle competitions using an AI-powered agent.")

# ---------------------------------------------
# One-time initialization
# ---------------------------------------------
@st.cache_resource(show_spinner=True)
def initialize_agents():
    with st.spinner("Loading Kaggle competition data..."):
        project_docs = read_repo_data(
            repo_owner="Khangtran94",
            repo_name="kaggle-solutions",
            branch="gh-pages",
        )

    completed = extract_completed_competitions(project_docs)
    embedding_model, vindex = build_vector_index(completed)
    search_agent = create_search_agent(embedding_model, vindex)

    evaluation_prompt = """
    Use this checklist to evaluate the quality of an AI agent's answer (<ANSWER>) to a user question (<QUESTION>).
    We also include the entire log (<LOG>) for analysis.

    For each item, check if the condition is met.

    Checklist:

    - instructions_follow: The agent followed the user's instructions (in <INSTRUCTIONS>)
    - instructions_avoid: The agent avoided doing things it was told not to do
    - answer_relevant: The response directly addresses the user's question
    - answer_clear: The answer is clear and correct
    - answer_citations: The response includes proper citations or sources when required
    - completeness: The response is complete and covers all key aspects of the request
    - tool_call_search: Is the search tool invoked?

    Output true/false for each check and provide a short explanation for your judgment.
    """.strip()

    eval_agent = Agent(
        name="eval_agent",
        model="gpt-5-nano",
        instructions=evaluation_prompt,
        output_type=EvaluationChecklist,
    )

    return search_agent, eval_agent


search_agent, eval_agent = initialize_agents()

# ---------------------------------------------
# Session state
# ---------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

# ---------------------------------------------
# UI: Chat history
# ---------------------------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------
# UI: User input
# ---------------------------------------------
query = st.chat_input("Ask about a Kaggle project (e.g. 'Image Classification')")

if query:
    # -----------------------------
    # Show user message
    # -----------------------------
    st.session_state.chat_history.append(
        {"role": "user", "content": query}
    )
    with st.chat_message("user"):
        st.markdown(query)

    # -----------------------------
    # Run agent (NO STREAMING)
    # -----------------------------
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            result = asyncio.run(search_agent.run(query))
            answer = result.output
            st.markdown(answer)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )


    # -----------------------------
    # Logging
    # -----------------------------
    log_file = log_interaction_to_file(
        agent=search_agent,
        messages=result.new_messages(),
    )

    # -----------------------------
    # Evaluation
    # -----------------------------
    log_record = load_log_file(log_file)

    user_prompt_format = """
    <INSTRUCTIONS>{instructions}</INSTRUCTIONS>
    <QUESTION>{question}</QUESTION>
    <ANSWER>{answer}</ANSWER>
    <LOG>{log}</LOG>
    """.strip()

    evaluation = evaluate_log_record(
        eval_agent,
        log_record,
        user_prompt_format,
    )

    st.session_state.evaluations.append(evaluation)
