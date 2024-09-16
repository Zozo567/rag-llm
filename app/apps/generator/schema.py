from typing import List
from app.core.schema import BaseSchema


class InGenerator(BaseSchema):
    query: str


class Reference(BaseSchema):
    link: str
    text: str
    page: int


class GeneratorSchema(BaseSchema):
    answer: str
    references: List[Reference]
