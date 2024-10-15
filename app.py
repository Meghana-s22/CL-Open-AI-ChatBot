from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple rule-based responses
def generate_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hi there! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! Thanks for asking."
    elif "bye" in user_input:
        return "Goodbye! Have a great day."
    else:
        return "I'm not sure how to respond to that. Can you ask me something else?"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = generate_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
