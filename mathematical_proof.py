from phi.agent import Agent
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv
load_dotenv()

task = "Prove that for any positive integer n, the sum of the first n odd numbers is equal to n squared. Provide a detailed proof."
reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True, markdown=True,
    # structured_outputs=True
)
reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)