from pathlib import Path

_DIR = Path(__file__).parent

def _load(name: str) -> str:
    return (_DIR / f"{name}.md").read_text(encoding="utf-8")

def system_prompt_materi(payload: dict) -> str:
    return _load("system_prompt_materi")

def system_prompt_pilgan(payload: dict) -> str:
    return _load("system_prompt_pilgan")

def system_prompt_essay(payload: dict) -> str:
    return _load("system_prompt_essay")