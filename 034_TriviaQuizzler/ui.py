from tkinter import *
from quiz_brain import QuizBrain


THEME_COLOR = "#375362"
PAD_X = 20
PAD_Y = 20
QUESTION_FONT = ("Arial", 15, "italic")
SCORE_FONT = ("Arial", 15, "bold")
CANVAS_WIDTH = 300


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Trivia Quizzler")
        self.window.config(padx=PAD_X, pady=PAD_Y, bg=THEME_COLOR)

        self.canvas = Canvas(width=CANVAS_WIDTH, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            text="Question text",
            width=CANVAS_WIDTH - 20,
            fill="black",
            font=QUESTION_FONT
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=PAD_Y)

        image_1 = PhotoImage(file="images/true.png")
        self.button_1 = Button(
            image=image_1,
            highlightthickness=0,
            command=self.true_pressed
        )
        self.button_1.grid(column=0, row=2)

        image_2 = PhotoImage(file="images/false.png")
        self.button_2 = Button(
            image=image_2,
            highlightthickness=0,
            command=self.false_pressed
        )
        self.button_2.grid(column=1, row=2)

        self.label_score = Label(
            text=f"Score: {self.quiz.score}",
            fg="white",
            bg=THEME_COLOR,
            font=SCORE_FONT,
            pady=PAD_Y
        )
        self.label_score.grid(column=1, row=0)

        self.get_next_question()

        self.window.mainloop()

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.canvas.itemconfig(self.question_text, text=self.quiz.next_question())
            self.label_score.config(text=f"Score: {self.quiz.score}")
        else:
            self.button_1.config(state="disabled")
            self.button_2.config(state="disabled")
            self.canvas.itemconfig(
                self.question_text,
                text=f"You've completed the quiz!\n"
                     f"Your final score is: {self.quiz.score}/{self.quiz.question_number}"
            )

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, func=self.get_next_question)
