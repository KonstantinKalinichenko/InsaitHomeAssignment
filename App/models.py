from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class QnA(db.Model):
    __tablename__ = 'questions_answers'
    __table_args__ = {'schema': 'questions_answers_schema'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'QnA {self.id}: {self.question} -> {self.answer}'
