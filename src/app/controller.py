from collections import Generator

class TestRunner(Generator):
# class TestRunner:

    def __init__(self, test):
        self.test = test
        self.current_step = 0
        self.num_correct_answers = 0
        self.num_incorrect_answers = 0
        self.points = 0

    def send(self, choice=None):
        if choice is not None:
            self.current_step += 1
            self.num_correct_answers += int(choice.is_correct)
            self.num_incorrect_answers += 1 - int(choice.is_correct)

        if self.current_step < self.questions_count:
            return self.test.questions[self.current_step]
        else:
            self.points = max(0, self.num_correct_answers - self.num_incorrect_answers)
            return None

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    @property
    def questions_count(self):
        return len(self.test.questions)

    @property
    def current_question(self):
        assert self.current_step < self.questions_count
        return self.test.questions[self.current_step]