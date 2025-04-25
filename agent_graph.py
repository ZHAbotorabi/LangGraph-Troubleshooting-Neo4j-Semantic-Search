from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from typing import TypedDict
import json
import os
import numpy as np

# === Define LangGraph state schema ===
class GraphState(TypedDict):
    query: str
    node_id: str
    article: str
    script: str
    procedure: list

# === Load data.json for articles and scripts ===
with open("data.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# === Connect to Neo4j ===
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test2345"))

# === Cypher query to fetch path from Neo4j ===
def get_procedure_path(start_id):
    query = """
    MATCH path = (n:Step {nodeId: $start})-[:NEXT*]->(m)
    RETURN nodes(path) AS steps
    """
    with driver.session() as session:
        result = session.run(query, start=start_id)
        steps = result.single()
        if steps:
            return [node["title"] for node in steps["steps"]]
        return []

# === New: Semantic Search using Neo4j-stored embeddings ===
def get_most_similar_node(query_embedding):
    with driver.session() as session:
        result = session.run("""
            MATCH (n:Step)
            WHERE n.embedding IS NOT NULL
            RETURN n.nodeId AS id, n.title AS text, n.embedding AS embedding
        """)
        max_score = -1
        best = {"id": "", "text": ""}
        for record in result:
            emb = np.array(record["embedding"])
            score = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
            if score > max_score:
                max_score = score
                best = {
                    "id": record["id"],
                    "text": record["text"]
                }
        return best

# === New: Fetch article and script from local JSON ===
def get_article_and_script(node_id):
    article_text = ""
    script_text = ""
    for item in documents:
        if item["type"] == "article" and item["id"] == f"{node_id}-article":
            article_text = item["text"]
        elif item["type"] == "script" and item["id"] == f"{node_id}-script":
            script_text = item["text"]
    return article_text, script_text

# === Node 1: Semantic Search ===
def semantic_match(state):
    query = state["query"]
    query_embedding = model.encode(query)
    result = {"query": query, "node_id": "", "article": "", "script": "", "procedure": []}

    best = get_most_similar_node(query_embedding)

    result["node_id"] = best["id"]
    result["article"], result["script"] = get_article_and_script(best["id"])

    return result

# === Node 2: Fetch Procedure Path ===
def fetch_procedure(state):
    node_id = state.get("node_id")
    if node_id:
        state["procedure"] = get_procedure_path(node_id)
    return state

# === Node 3: Build Final Answer ===
def build_answer(state):
    return {
        "procedure": state.get("procedure"),
        "article": state.get("article"),
        "script": state.get("script")
    }

# === Build LangGraph ===
graph = StateGraph(GraphState)
graph.add_node("SemanticMatch", RunnableLambda(semantic_match))
graph.add_node("GetProcedure", RunnableLambda(fetch_procedure))
graph.add_node("BuildAnswer", RunnableLambda(build_answer))

graph.set_entry_point("SemanticMatch")
graph.add_edge("SemanticMatch", "GetProcedure")
graph.add_edge("GetProcedure", "BuildAnswer")
graph.set_finish_point("BuildAnswer")

# === Save graph structure to PNG before compile ===
#graph.get_graph().get_diagram().write_png("static/langgraph_structure.png")

# === Compile the graph ===
app = graph.compile()

# === Run Locally ===
if __name__ == "__main__":
    question = input("Ask a question: ")
    result = app.invoke({
        "query": question,
        "node_id": "",
        "article": "",
        "script": "",
        "procedure": []
    })
    print("\nAnswer:")
    print("Procedure:", result["procedure"])
    print("Article:", result["article"])
    print("Script:", result["script"])
