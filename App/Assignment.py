from flask import Flask, request, jsonify
from dotenv import load_dotenv
from App.models import db, QnA
import openai
from openai import OpenAI
import os


load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/ask_openai'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(application)
    return application


app = create_app()


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if 'question' not in data:
        return jsonify({'error': 'Question not provided'}), 400

    question = data['question']

    client = OpenAI(
        api_key=openai.api_key,
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            model='gpt-3.5-turbo'
        )
        answer = response['choices'][0]['message']['content']

        new_entry = QnA(question=question, answer=answer)
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': answer}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
