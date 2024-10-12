from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

db = SQLAlchemy()


class QnA(db.Model):
    __tablename__ = 'questions_answers'
    __table_args__ = {'schema': 'questions_answers_schema'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'QnA {self.id}: {self.question} -> {self.answer}'


def create_schema(engine, schema_name):
    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema_name}'")
        )
        schema_exists = result.scalar()

        if not schema_exists:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema_name}'))


def create_app():
    application = Flask(__name__)
    application.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@host.docker.internal:5433/ask_openai'
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
            model="gpt-3.5-turbo",
        )
        answer = response.choices[0].message.content

        new_entry = QnA(question=question, answer=answer)
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': answer}), 200


if __name__ == "__main__":
    with app.app_context():
        create_schema(db.engine, 'questions_answers_schema')
        db.create_all()

    app.run(debug=True, port="5000", host='0.0.0.0')
