import json
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.run.response import RunResponse


def process_schema(agent_resp: RunResponse) -> RunResponse:
    """
    Process the agent's response to generate a React JSON schema.

    Args:
        agent_resp (str): The raw response from the agent.

    Returns:
        dict: A dictionary representing the JSON schema.
    """
    try:
        # Attempt to parse the agent's response as JSON
        # json_schema = json.loads(agent_resp)
        json_schema: RunResponse = agent_resp
        return json_schema.content
    except json.JSONDecodeError:
        print("Error: The agent's response is not valid JSON.")
        return {}

# Initialize the OpenAI model
openai_model = OpenAIChat(id="gpt-3.5-turbo")

# Define the agent with the process_schema function as a tool
web_agent = Agent(
    name="Web Agent",
    model=openai_model,
    tools=[process_schema],
    instructions=[
        "1. Generate a JSON schema based on the provided form context. Ensure the output is strictly in JSON format without additional data",
        "2. Pass this generated JSON to the process_schema function."
    ],
    show_tool_calls=True,
    monitoring=True
)

def generate_schema(form_context: str) -> RunResponse:
    """
    Generate a React JSON schema based on the provided form context.

    Args:
        form_context (str): The user's input describing the form.

    Returns:
        dict: The generated React JSON schema.
    """
    # Run the agent with the provided form context
    agent_resp: RunResponse = web_agent.run(f"Generate a JSON schema for the following form context: {form_context}")
    # The agent will automatically utilize the process_schema tool
    return agent_resp

# Example usage
if __name__ == "__main__":
    form_description = "A user registration form with fields for username, email, and password."
    schema = generate_schema(form_description)
    print("Generated JSON Schema:", schema)
