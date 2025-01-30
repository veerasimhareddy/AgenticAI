from phi.agent import Agent
from dotenv import load_dotenv
load_dotenv()

agent = Agent(markdown=True, monitoring=True, debug_mode=True)
agent.print_response("Which model is used to generate this data? And till which you date you are trained on?")
