from pathlib import Path

VENV_LOCATION: Path = Path(".venv")
PYTHON_VERSION: str | None = None
PROJECTS: list[Path] = []
DEV_DEP_GROUPS = ["dev", "test"]
PIPELINE_DEP_GROUPS = ["pipeline", "test"]
