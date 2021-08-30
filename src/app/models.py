from enum import Enum

from pydantic import BaseModel
from typing import List, Optional


class Choice(BaseModel):
    text: str
    is_correct: bool


class Question(BaseModel):
    id: int
    text: str
    order_number: int
    choices: Optional[List[Choice]] = []


class Test(BaseModel):
    id: int
    title: str
    questions_count: int
    questions: Optional[List[Question]] = []


class TestResult(BaseModel):
    class State(Enum):
        NEW = 0
        FINISHED = 1

    id: Optional[int]
    questions_count: Optional[int]
    current_order_number: int
    num_correct_answers: int
    num_incorrect_answers: int
    state: int
    get_state_display: Optional[str]


class User(BaseModel):
    username: str
    jwt_token: Optional[str] = ''
    rating: Optional[float]
