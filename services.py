# services.py
import time
from typing import Dict

import pymorphy3
from fastapi import Depends

from config import CASE_TAGS

# Create a single, shared instance of the MorphAnalyzer
# This is more efficient as it avoids reloading the dictionaries on every request.
_morph_analyzer = pymorphy3.MorphAnalyzer()


def get_morph_analyzer() -> pymorphy3.MorphAnalyzer:
    """
    Returns the shared MorphAnalyzer instance.
    This function is used as a FastAPI dependency.
    """
    return _morph_analyzer


class WordInflector:
    def __init__(self, morph_analyzer: pymorphy3.MorphAnalyzer):
        self.morph = morph_analyzer

    def inflect(self, word: str, case: str) -> str:
        """Inflects a single word to a specific case."""
        if case not in CASE_TAGS:
            return word

        # The first parse result is usually the most relevant one.
        parsed_word = self.morph.parse(word)
        if not parsed_word:
            return word

        inflected_form = parsed_word[0].inflect({case})
        return inflected_form.word if inflected_form else word

    def all_inflect(self, q: str) -> Dict[str, str]:
        """Inflects a word into all available cases."""
        res = {}
        for case in CASE_TAGS:
            res[case] = self.inflect(q, case)
        return res


def get_word_inflector(
    morph: pymorphy3.MorphAnalyzer = Depends(get_morph_analyzer),
) -> WordInflector:
    """Dependency factory to get a WordInflector instance."""
    return WordInflector(morph)
