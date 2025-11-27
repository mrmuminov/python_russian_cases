# main.py
import time
from typing import Dict, Union

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from markdown2 import Markdown

from config import CASE_TAGS
from services import WordInflector, get_word_inflector

app = FastAPI()
markdowner = Markdown()

# Add CORS middleware to allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    """Returns the content of the README.md file."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return markdowner.convert(f.read())
    except FileNotFoundError:
        return "<h1>Welcome to the API</h1>"


@app.get("/{case}")
def inflect_word(
        case: str,
        q: str = Query(..., description="The word to inflect."),
        inflector: WordInflector = Depends(get_word_inflector),
) -> Dict[str, Union[str, float, Dict[str, str]]]:
    """
    Inflects a word to a given case or all cases.
    """
    start = time.perf_counter()

    if case == "all":
        result = inflector.all_inflect(q)
    elif case in CASE_TAGS:
        result = inflector.inflect(q, case)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid case. Valid values are: all, {', '.join(CASE_TAGS)}",
        )

    end = time.perf_counter()

    return {"result": result, "time": end - start}
