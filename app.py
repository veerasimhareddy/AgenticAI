from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from simpl_forms_agent import *

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["*"],
        "allow_headers": ["*"]
    }
})

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response, 200
# @app.route('/getSchema', methods=['POST'])
# def get_schema():
#     data = request.get_json()
#     form_context = data.get('prompt_from_user', '')
#     response_message = generate_schema(form_context)
    # response_message = get_receipe_from_rag(form_context)
    # return json.dumps(response_message)

@app.route('/create_new_form', methods=['POST'])
def create_form_schema():
    data = request.get_json()
    prompt = data.get('prompt_from_user', '')
    schema = generate_form_schema(prompt)
    return schema

@app.route('/add_rules', methods=['POST'])
def add_rule():
    data = request.get_json()
    prompt = data.get('prompt_from_user', '')
    schema_from_user = data.get('schema', '')
    controls = data.get('controls', '')
    updated_schema = apply_form_rules(schema_from_user, prompt, controls)
    return updated_schema

if __name__ == '__main__':
    app.run(debug=True)
