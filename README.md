# party-organiser
and experiment in FastAPI, HTMX and Tailwind
```
uv init python 3.13.0
uv python pin 3.13.0
uv add alambic==1.14
uv venv --python 3.13.0
uv sync
```

```
sqlite3
.open database.db
.tables
```

## set PYTHONPATH - macOS/Linux
export PYTHONPATH=${PWD}:$PYTHONPATH

## set PYTHONPATH - windows
set PYTHONPATH=C:\me\Courses\party_app;%PYTHONPATH


## tips
HTMX is "JavaScript for people who don't want to use JavaScript"

Tailwind CSS is a utility-first CSS framework. In a utility-first approach, each class serves a single purpose, like setting only the border color without affecting its width or style. This allows you to construct the design directly in HTML rather than using custom CSS classes that combine multiple properties.


 Alpine.js is a lightweight JavaScript framework. It only has 15 attributes (e.g., x-data), 6 properties (e.g., $el), and 2 methods (e.g., Alpine.data) as of writing. While HTMX focuses on interaction with your server, Alpine covers client-side state and operations.
 