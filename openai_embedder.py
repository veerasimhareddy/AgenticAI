from phi.agent import AgentKnowledge
from phi.vectordb.pgvector import PgVector
from phi.embedder.openai import OpenAIEmbedder
from dotenv import load_dotenv
load_dotenv()
from phi.storage.workflow.postgres import PgWorkflowStorage;

embeddings = OpenAIEmbedder().get_embedding("Knowledge Document Knowledge Base.The DocumentKnowledgeBase reads local docs files, converts them into vector embeddings and loads them to a vector databse.")

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:1]}")
print(f"Dimensions: {len(embeddings)}")

# Example usage:
knowledge_base = AgentKnowledge(
    vector_db=PgVector(
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        table_name="openai_embeddings",
        embedder=OpenAIEmbedder(),
    ),
    num_documents=2,
)
