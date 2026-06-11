from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    image = data.get('image')  # base64 image
    
    messages = [{"role": "user", "content": []}]
    if message:
        messages[0]['content'].append({"type": "text", "text": message})
    if image:
        messages[0]['content'].append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image}"}
        })
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return jsonify({'reply': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
