from flask import Flask, request, jsonify
from schema_handler import process_schema  # Import the function from schema_handler.py

app = Flask(__name__)

# Define the POST route
@app.route('/getSchema', methods=['POST'])
def get_schema():
    # Get the JSON payload from the request
    data = request.get_json()

    # Extract 'formContext' from the payload
    form_context = data.get('prompt_from_user', '')

    # Call the process_schema function to handle the logic
    response_message = process_schema(form_context)

    # Return the response as JSON
    return jsonify({"message": response_message})

if __name__ == '__main__':
    # Run the server
    app.run(debug=True)
