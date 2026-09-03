from pydantic import BaseModel
from typing import List


class TestCase(BaseModel):
    id: str
    title: str
    test_type: str
    priority: str
    preconditions: str
    steps: List[str]
    expected_result: str