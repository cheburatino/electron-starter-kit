from datetime import date
from logic.abc.logic_element import LogicElement
from logic.element.person.repository import PersonRepository


class Person(LogicElement):
    _repository_class = PersonRepository
    
    first_name: str
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = None
