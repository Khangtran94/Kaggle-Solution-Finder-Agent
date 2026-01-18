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

from pydantic_ai import Agent


if __name__ == "__main__":
    print("STEP 1: Loading Kaggle competition data from GitHub...")
    project_docs = read_repo_data(
        repo_owner="Khangtran94",
        repo_name="kaggle-solutions",
        branch="gh-pages"
    )
    print("✓ STEP 1 completed")

    print("\nSTEP 2: Extracting completed competitions...")
    completed_competitions = extract_completed_competitions(project_docs)
    print(f"✓ STEP 2 completed — {len(completed_competitions)} competitions found")

    print("\nSTEP 3: Building vector index...")
    embedding_model, vindex = build_vector_index(completed_competitions)
    print("✓ STEP 3 completed")

    print("\nSTEP 4: Creating search agent...")
    query_agent = create_search_agent(embedding_model, vindex)
    print("✓ STEP 4 completed")

    print("\nSTEP 5: Running search query...")
    query = "Project about Image Classification"
    result = query_agent.run_sync(query)
    print("✓ STEP 5 completed")

    print("\nSTEP 6: Logging agent interaction...")
    log_file = log_interaction_to_file(
        agent=query_agent,
        messages=result.new_messages()
    )
    print(f"✓ STEP 6 completed — log saved to {log_file}")

    print("\nSTEP 7: Creating evaluation agent...")
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
    print("✓ STEP 7 completed")

    print("\nSTEP 8: Evaluating agent response...")
    user_prompt_format = """
    <INSTRUCTIONS>{instructions}</INSTRUCTIONS>
    <QUESTION>{question}</QUESTION>
    <ANSWER>{answer}</ANSWER>
    <LOG>{log}</LOG>
    """.strip()

    log_record = load_log_file(log_file)
    evaluation = evaluate_log_record(
        eval_agent,
        log_record,
        user_prompt_format
    )
    print("✓ STEP 8 completed")

    print("\n=== FINAL EVALUATION RESULT ===")
    print(evaluation)