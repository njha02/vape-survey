from typing import List
import os
import yaml
from dataclasses import dataclass


@dataclass
class Question:
    q_key: str
    description: str
    required: bool


@dataclass
class SelectQuestion(Question):
    choices: List[str]


@dataclass
class EmailQuestion(Question):
    pass


@dataclass
class IntegerQuestion(Question):
    pass


def load_from_yaml() -> List[Question]:
    question_file = "./questions.yaml"
    assert os.path.exists(question_file), question_file
    with open(question_file, "r") as question_def_file:
        question_def_dicts = yaml.safe_load_all(question_def_file)
        loaded_questions: List[Question] = []
        for i, q in enumerate(question_def_dicts):
            if q is None:
                raise ValueError(
                    f"Error parsing question {i} in {question_file}. Is there an extra '---'?"
                )
            elif q["type"] == "text":
                del q["type"]  # remove unexpected fields
                loaded_questions.append(Question(**q))
            elif q["type"] == "select":
                del q["type"]  # remove unexpected fields
                loaded_questions.append(SelectQuestion(**q))
            elif q["type"] == "integer":
                del q["type"]  # remove unexpected fields
                loaded_questions.append(IntegerQuestion(**q))
            elif q["type"] == "email":
                del q["type"]  # remove unexpected fields
                loaded_questions.append(EmailQuestion(**q))
            else:
                raise ValueError(f"Unknown source definition: {q}")
    return loaded_questions
