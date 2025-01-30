from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.embedder.openai import OpenAIEmbedder
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.lancedb import LanceDb, SearchType
from dotenv import load_dotenv
load_dotenv()
# Create a knowledge base from a PDF
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    # Use LanceDB as the vector database
    vector_db=LanceDb(
        table_name="recipes",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=OpenAIEmbedder(model="text-embedding-3-small"),
    ),
)
# Comment out after first run as the knowledge base is loaded
knowledge_base.load()

receipe_agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    # Add the knowledge base to the agent
    knowledge=knowledge_base,
    instructions=["Strictly return the response in JSON", "Send this received JSON "],
    show_tool_calls=True,
    markdown=True,
)
# receipe_agent.print_response("How do I make chicken and galangal in coconut milk soup", stream=True)

def modify_json(prompt_res):
    print("prompt_res")

def get_receipe_from_rag(form_context):
    agent_resp = receipe_agent.run(form_context)
    res_cont =  agent_resp.content
    return  res_cont
