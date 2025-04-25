# Add embedding Property to Each Node in Neo4j

from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# 1. Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Connect to your Neo4j instance
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test2345"))

# 3. Define the function that updates embeddings for all Step nodes
def update_embeddings(tx):
    # Fetch nodeId and title for all Step nodes
    result = tx.run("MATCH (n:Step) RETURN n.nodeId AS id, n.title AS text")
    for record in result:
        text = record["text"]
        node_id = record["id"]
        if text and node_id:
            # Generate embedding from text
            embedding = model.encode(text).tolist()
            # Save it back to the node as a property
            tx.run("""
                MATCH (n:Step {nodeId: $nodeId})
                SET n.embedding = $embedding
            """, nodeId=node_id, embedding=embedding)

# 4. Run the update
with driver.session() as session:
    session.write_transaction(update_embeddings)

driver.close()
