import csv
from pathlib import Path

KB_DIR = Path(__file__).parent.resolve()


def load_csv(filename: str) -> list[dict]:
    """Load a CSV file from knowledge_base/ and return rows as dicts."""
    filepath = KB_DIR / filename
    if not filepath.exists():
        return []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_templates(discipline: str | None = None) -> list[dict]:
    """Get summary templates, optionally filtered by discipline."""
    templates = load_csv("templates.csv")
    if discipline:
        return [t for t in templates if t["discipline"].lower() == discipline.lower()]
    return templates


def get_formulations(domain: str | None = None) -> list[dict]:
    """Get ready-made formulations, optionally filtered by domain."""
    formulations = load_csv("formulations.csv")
    if domain:
        return [f for f in formulations if f["domain"].lower() == domain.lower()]
    return formulations


def get_questions(discipline: str | None = None, count: int = 8) -> list[str]:
    """Get self-check questions, optionally filtered by discipline."""
    questions = load_csv("questions.csv")
    if discipline:
        filtered = [q for q in questions if q["discipline"].lower() == discipline.lower()]
    else:
        filtered = questions

    import random
    if len(filtered) > count:
        filtered = random.sample(filtered, count)
    return [q["question_template"] for q in filtered]


def load_full_knowledge() -> dict:
    """Load all knowledge base files into a structured dict."""
    return {
        "templates": load_csv("templates.csv"),
        "formulations": load_csv("formulations.csv"),
        "questions": load_csv("questions.csv"),
    }
