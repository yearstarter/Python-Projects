import requests
from quiz_brain import QUESTION_AMOUNT


API_trivia = "https://opentdb.com/api.php"
params_trivia = {
    "amount": QUESTION_AMOUNT,
    # "category": 21,  # 9-general knowledge, 17-science&nature, 18-computer, 21-sport, 22-geography
    # "difficulty": "medium",  # easy/medium/hard
    "type": "boolean"}


class Question:

    def __init__(self, q_text, q_answer):
        self.text = q_text
        self.answer = q_answer


response = requests.get(url=API_trivia, params=params_trivia)
response.raise_for_status()
data = response.json()["results"]

question_bank = []
for question in data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)
