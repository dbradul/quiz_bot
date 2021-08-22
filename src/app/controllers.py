class TestRunner:

    def __init__(self, test):
        self._test = test
        self.current_step = 0
        self.num_correct_answers = 0
        self.num_incorrect_answers = 0

    def run(self):
        for question in self._test.questions:
            choice = yield question
            self.current_step += 1
            self.num_correct_answers += int(choice.is_correct)
            self.num_incorrect_answers += 1 - int(choice.is_correct)

        return max(0, self.num_correct_answers - self.num_incorrect_answers)
