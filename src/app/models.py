from pydantic import BaseModel, Field
from typing import List, Optional


class Choice(BaseModel):
    text: str
    is_correct: bool


class Question(BaseModel):
    text: str
    order_number: int
    choices: Optional[List[Choice]] = []


class Test(BaseModel):
    id: int
    title: str
    questions_count: int
    questions: Optional[List[Question]] = []


class TestResult(BaseModel):
    questions_count: int
    current_order_number: int
    # 'test',
    # 'user',
    state: int
    get_state_display: str


class User(BaseModel):
    rating: float
    username: str
