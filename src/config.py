from pathlib import Path
from typing import Final

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent.parent
    QUESTION_ANSWER_HEADING: Final = (
        ("A", "A)"),
        ("B", "B)"),
        ("C", "C)"),
        ("D", "D)"),
        ("E", "E)"),
    )
    FILE_WITH_TEST: Final = "test.js"


settings = Settings()
