"""Context memory extraction for chatbot."""

import re
from typing import Dict


def extract_memory_from_text(text: str) -> Dict[str, float]:
    memory: Dict[str, float] = {}
    salary_match = re.search(r"(salary|income)\D*(\d+(?:\.\d+)?)", text.lower())
    expense_match = re.search(r"(expense|spend)\D*(\d+(?:\.\d+)?)", text.lower())
    savings_match = re.search(r"(saving|save)\D*(\d+(?:\.\d+)?)", text.lower())

    if salary_match:
        memory["salary"] = float(salary_match.group(2))
    if expense_match:
        memory["expenses"] = float(expense_match.group(2))
    if savings_match:
        memory["savings"] = float(savings_match.group(2))

    return memory

