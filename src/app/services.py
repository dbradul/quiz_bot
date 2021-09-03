from collections import Generator

from app.fetchers import TestModelFetcher, TestResultFetcher, QuestionModelFetcher
from app.models import TestResult


class TestRunner(Generator):
    NEXT = 'NEXT'
    FINISH = 'FINISH'

    def __init__(self, call, test_id):
        self.test = TestModelFetcher(call.user).get_object(test_id)
        self.call = call
        self.current_step = 0
        self.num_correct_answers = 0
        self.num_incorrect_answers = 0
        self.points = 0
        self._callbacks = {}

    def send(self, choice=None):
        if choice is not None:
            self.current_step += 1
            self.num_correct_answers += int(choice.is_correct)
            self.num_incorrect_answers += 1 - int(choice.is_correct)

        if self.current_step < self.test.questions_count:
            question_detail = QuestionModelFetcher(self.call.user).get_object(self.current_question.id)
            self.call_callback(self.NEXT, question_detail)

        else:
            self.points = max(0, self.num_correct_answers - self.num_incorrect_answers)
            test_result = TestResult(
                state=TestResult.State.FINISHED.value,
                current_order_number=self.current_step,
                num_correct_answers=self.num_correct_answers,
                num_incorrect_answers=self.num_incorrect_answers,
            )
            test_result = TestResultFetcher(self.call.user).post_object(
                parent_id=self.test.id,
                obj=test_result
            )

            self.call_callback(self.FINISH, test_result)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    @property
    def questions_count(self):
        return len(self.test.questions)

    @property
    def current_question(self):
        assert self.current_step < self.test.questions_count, 'Current step >= questions count, is count=0?'
        return self.test.questions[self.current_step]

    def add_callback(self, tag, func):
        self._callbacks[tag] = func
        return self

    def call_callback(self, tag, *args):
        func = self._callbacks.get(tag)
        if func:
            func(self.call, self, *args)

    def run(self):
        next(self)
