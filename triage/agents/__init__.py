from dotenv import load_dotenv

from triage import PROMPTS_DIR

load_dotenv()


def load_prompt(name: str) -> str:
    with open(PROMPTS_DIR / f"{name}.md", "r") as f:
        return f.read()
