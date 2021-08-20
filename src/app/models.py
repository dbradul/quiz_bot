from pydantic import BaseModel, Field


class Test(BaseModel):
    id: int
    title: str
    state: str


class TestResult(BaseModel):
    questions_count: int
    current_order_number: int
    # 'test',
    # 'user',
    state: int
    get_state_display: str


class Question(BaseModel):
    order_number: int


class Choice(BaseModel):
    text: str
    is_correct: bool


class User(BaseModel):
    rating: float
    username: str
