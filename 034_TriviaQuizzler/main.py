from quiz_brain import QuizBrain
from ui import QuizInterface
from question_model import question_bank


quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)
