# main.py
import time
from typing import Dict, Union

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import PlainTextResponse

from config import CASE_TAGS
from services import WordInflector, get_word_inflector

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
def read_root() -> str:
    """Returns the content of the README.md file."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Welcome to the API."


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
