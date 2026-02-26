import os
from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates


_templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


def _get_templates():
    return _templates


Templates = Annotated[Jinja2Templates, Depends(_get_templates)]
