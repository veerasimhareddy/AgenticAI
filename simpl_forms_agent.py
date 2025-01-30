from flask import Flask, request, jsonify, Response
from phi.agent import Agent
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.model.openai import OpenAIChat
from typing import Dict, Any
import json
from phi.vectordb.pgvector import PgVector
from phi.vectordb.search import SearchType

from dotenv import load_dotenv
load_dotenv()

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
knowledge_base = PDFUrlKnowledgeBase(
    # Read PDF from this URL
    urls=["http://127.0.0.1:5500/packages/ui/public/rule_feed_document.pdf"],
    # Store embeddings in the `ai.recipes` table
    vector_db=PgVector(table_name="form_rules_examples", db_url=db_url, search_type=SearchType.hybrid),
)

knowledge_base.load(upsert=True, recreate=True)


form_creation_agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    description="You are an expert in creating React JSON Schema for forms.",
    instructions=[
        "Convert natural language form requirements into React JSON Schema format.",
        "Include appropriate validation rules and field types.",
        "Always return valid JSON schema that can be used with @rjsf/core library.",
        "Include proper data types, required fields, and validation patterns where applicable.",
        "Structure the response as a JSON object with 'schema' and 'uiSchema' properties.",
        "Return only the JSON object, no additional text or explanations.",
    ],
    # markdown=True
)

rules_creation_agent = Agent(
    knowledge=knowledge_base,
    model=OpenAIChat(id="gpt-3.5-turbo"),
    search_knowledge=True,
    read_chat_history=True,
    monitoring=True,
    description="You are an expert in modifying React JSON Schema forms with conditional rules.",
    instructions=[
        "Return ONLY a valid JSON object/array without any markdown formatting or code blocks",
        "Strictly Ensure not to wrap the response in ```json or any other markers",
        "The response should be directly parseable by json.loads()"
        "Modify the provided JSON Schema by adding conditional allOf rules.",
        "Preserve all existing schema properties while adding new conditions.",
        "Use correct JSON Schema syntax for dependencies and conditional rendering.",
        "Handle schema modifications as needed.",
        # "Return only the modified JSON object.",
        "Strictly Ensure the output maintains valid JSON Schema format compatible with @rjsf/core.",
    ]
)

field_identification_agent = Agent(
    knowledge=knowledge_base,
    model=OpenAIChat(id="gpt-3.5-turbo"),
    search_knowledge=True,
    read_chat_history=True,
    monitoring=True,
    description="You are an expert in React JSON Schema forms with conditional rules.",
    instructions=[
        "From the given Prompt Identify what is target_field",
        "Strictly target_field is the field path from the given Schema",
        "Strictly refer to the knowledge base and create rules/conditions using Schema and Prompt",
        "Strictly rules should be array of Objects following structure like : [{'conditions': {'and': [{field, op: 'is', value: 'enum'}]},'event': {type, params: {field}}}]",
        "Strictly always use enum values in value key of above line. Strictly do not pick from enumNames",
        "Strictly selected_field should a json object that will be picked from the given Controls with id of target_field",
        "Strictly Return ONLY a valid JSON object/array without any markdown formatting or code blocks",
        "Strictly Ensure not to wrap the response in ```json or any other markers",
        "Strictly Return only Json with target_field, rules, selected_field"
    ]
)

def generate_form_schema(prompt: str) -> str:
    """
    Generate React JSON Schema for forms based on the given prompt.
    
    Args:
        prompt (str): Natural language description of the form requirements
        
    Returns:
        str: JSON string containing the schema and uiSchema
    """
    response = form_creation_agent.run(prompt)
    
    try:
        schema_res = json.loads(response.content)
        # schema_content = schema_res;
        return schema_res
    except json.JSONDecodeError:
        # If parsing fails, return a default error schema
        error_schema = {
            "error": "Failed to generate valid schema",
            "schema": {},
            "uiSchema": {}
        }
        return json.dumps(error_schema, indent=2)

def apply_form_rules(schema: Dict[Any, Any], rule_prompt: str, controls: Dict[Any, Any]) -> Response | dict[str, str | None | Any]:
    """
    Modify existing form schema by applying conditional rules based on the prompt.
    
    Args:
        schema (Dict[Any, Any]): Existing form schema dictionary
        rule_prompt (str): Natural language description of the conditional rule
        controls (Dict[Any, Any]): Controls for the form
        
    Returns:
        Dict[Any, Any]: Modified schema with applied rules
    """
    # Combine schema and rule in a structured prompt
    combined_prompt = f"""
        Current Schema:
        {json.dumps(schema, indent=2)}

        Given Controls:
        {json.dumps(controls, indent=2)}
        
        Apply this rule:
        {rule_prompt}
        """
    
    # res = rules_creation_agent.run(combined_prompt)
    res = field_identification_agent.run(combined_prompt)
    
    try:
        # parsed_response = json.loads(response.content)
        # res = jsonify(parsed_response)
        # return res
        return Response(
            response=res.content,
            status=200,
            mimetype='application/json'
        )
    except json.JSONDecodeError:
        # If parsing fails, return the original schema
        error_schema = {
            "error": "Failed to apply rules",
            "response": res.content,
            "status" : 500
        }
        return error_schema