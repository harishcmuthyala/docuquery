"""LangGraph agent with ReAct (Reasoning + Acting)"""

from typing import TypedDict, List
import logging
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
import re

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    question: str
    vectorstore: any
    all_chunks: List
    answer: str
    reasoning_steps: List[str]
    actions_taken: List[str]
    search_queries: List[str]


def create_react_agent():
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.0, groq_api_key=os.getenv("GROQ_API_KEY"))
    
    def reason(state: AgentState) -> AgentState:
        prompt = f"""Analyze if this question should be divided into sub-questions for better search results.

Question: "{state['question']}"

ONLY divide if the question explicitly asks about TWO OR MORE distinct things:
- Explicit comparisons: "Compare X vs Y", "X versus Y", "difference between X and Y"
- Multiple explicit items: "What are X and Y", "Tell me about X and Y"
- Connected by "and" where X and Y are clearly different topics

Do NOT divide if:
- The question is about a single concept (even if it has multiple words)
- The question can be answered with one search
- Dividing would make the sub-questions less clear

Examples:
- "Compare Q1 vs Q4 revenue" → DIVIDE (explicit comparison)
- "What are risks and mitigations" → DIVIDE (two distinct topics)
- "What is the decoder stack" → NO DIVISION (single concept)
- "How does attention work" → NO DIVISION (single concept)

If dividing, create EXACTLY 2 complete sub-questions.

Format:
Decision: DIVIDE or NO DIVISION
Reasoning: [explain]
Question 1: [only if DIVIDE]
Question 2: [only if DIVIDE]"""

        reasoning = llm.invoke([HumanMessage(content=prompt)]).content
        
        # Initialize and append to reasoning steps
        if "reasoning_steps" not in state or state["reasoning_steps"] is None:
            state["reasoning_steps"] = []
        state["reasoning_steps"].append(reasoning)
        
        # Initialize search_queries
        if "search_queries" not in state or state["search_queries"] is None:
            state["search_queries"] = []
        
        # Check if division is needed
        needs_division = "decision: divide" in reasoning.lower() and "no division" not in reasoning.lower()
        
        if needs_division:
            # Extract sub-questions
            extracted = []
            for i in [1, 2]:
                match = re.search(rf'question {i}:?\s*["\']?([^"\'\n]+)["\']?', reasoning, re.IGNORECASE)
                if match:
                    q = match.group(1).strip().strip('"\'')
                    if q and len(q) > 3:  # Basic validation
                        extracted.append(q)
            
            if len(extracted) == 2:
                state["search_queries"].extend(extracted)
                logger.info(f"Divided into 2 sub-questions")
            else:
                # Fallback: use original question
                logger.warning(f"LLM said DIVIDE but extracted {len(extracted)} questions, using original")
                state["search_queries"].append(state["question"])
        else:
            # No division: use original question
            state["search_queries"].append(state["question"])
        
        return state
    
    def act(state: AgentState) -> AgentState:
        from retrieval.retriever import query as retrieve_chunks
        
        if "actions_taken" not in state or state["actions_taken"] is None:
            state["actions_taken"] = []
        
        all_chunks = []
        num_queries = len(state["search_queries"])
        top_k = 5 if num_queries == 1 else 3
        
        for query in state["search_queries"]:
            try:
                chunks = retrieve_chunks(state["vectorstore"], query, top_k=top_k)
                all_chunks.extend(chunks)
                state["actions_taken"].append(f"Searched '{query}' → {len(chunks)} chunks")
            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")
                state["actions_taken"].append(f"Search failed for '{query}'")
        
        seen = set()
        deduplicated = []
        for chunk in all_chunks:
            if chunk.chunk.chunk_id not in seen:
                seen.add(chunk.chunk.chunk_id)
                deduplicated.append(chunk)
        
        state["all_chunks"] = deduplicated
        state["actions_taken"].append(f"Total: {len(deduplicated)} unique chunks")
        return state
    
    def generate(state: AgentState) -> AgentState:
        from generation.llm import format_context
        
        context = format_context(state["all_chunks"])
        queries = state.get("search_queries", [])
        
        if len(queries) > 1:
            prompt = f"""Answer by merging sub-question results.

Question: "{state['question']}"
Sub-questions: {', '.join(queries)}
Context: {context}

Provide comprehensive answer."""
        else:
            prompt = f"""Answer directly.

Question: "{state['question']}"
Context: {context}

Provide clear answer."""
        
        state["answer"] = llm.invoke([HumanMessage(content=prompt)]).content
        return state
    
    workflow = StateGraph(AgentState)
    workflow.add_node("reason", reason)
    workflow.add_node("act", act)
    workflow.add_node("generate", generate)
    
    workflow.set_entry_point("reason")
    workflow.add_edge("reason", "act")
    workflow.add_edge("act", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()


def run_react_agent(question: str, vectorstore) -> tuple[str, List[str], List[str]]:
    agent = create_react_agent()
    result = agent.invoke({
        "question": question,
        "vectorstore": vectorstore,
        "all_chunks": [],
        "answer": "",
        "reasoning_steps": [],
        "actions_taken": [],
        "search_queries": []
    })
    return result["answer"], result["reasoning_steps"], result["actions_taken"]


def run_agent(question: str, vectorstore) -> str:
    answer, _, _ = run_react_agent(question, vectorstore)
    return answer
