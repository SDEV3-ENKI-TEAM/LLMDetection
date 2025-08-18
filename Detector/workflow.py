from langgraph_node import (
    search_similar_logs,
    llm_judgment,
    final_decision,
    save_final_decision_to_chroma,
    TraceState,
    retriever,
)
from langgraph.graph import StateGraph, END

def build_workflow():
    workflow = StateGraph(TraceState)

    workflow.add_node("SimilaritySearch", search_similar_logs)
    workflow.add_node("LLMJudgment", llm_judgment)
    workflow.add_node("Decision", final_decision)
    workflow.add_node("SaveToChroma", save_final_decision_to_chroma)

    workflow.set_entry_point("SimilaritySearch")
    workflow.add_edge("SimilaritySearch", "LLMJudgment")
    workflow.add_edge("LLMJudgment", "Decision")
    workflow.add_edge("Decision", "SaveToChroma")
    workflow.add_edge("SaveToChroma", END)

    return workflow.compile(), retriever
