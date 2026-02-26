import os
from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from db import engine


_templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


def _get_templates():
    return _templates


Templates = Annotated[Jinja2Templates, Depends(_get_templates)]

def get_session():
    with Session(engine) as session:
        yield session
