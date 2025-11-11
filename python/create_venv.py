import shutil
import subprocess
from _common import must_pass, format_prefix, run_cmd
from _config import VENV_LOCATION, PYTHON_VERSION
from pathlib import Path


def remove_existing_venv(
    venv_path: Path,
    prefix: str | None,
) -> None:

    print(format_prefix(prefix) + "Searching for existing venv...")

    # Remove the existing venv
    if venv_path.exists():
        print("\tRemoving existing venv...")
        shutil.rmtree(venv_path)
        print("\tExisting venv removed")
    else:
        print("\tNo existing venv found")


def create_venv(
    venv_path: Path = VENV_LOCATION,
    version: str | None = PYTHON_VERSION,
    prefix: str | None = None,
) -> Path | None:
    """Create a virtual environment at the specified path."""
    print(format_prefix(prefix) + "Creating venv...")

    # Remove the existing venv
    if venv_path.exists():
        print("\tRemoving existing venv...")
        shutil.rmtree(venv_path)

    # Specify version if provided
    cmd = ["uv", "venv"]
    if version is not None:
        cmd.append("--python")
        cmd.append(version)
    cmd.append(str(venv_path))

    # Create the venv
    try:
        run_cmd(cmd=cmd, check=True)
        print("\tVenv created")
        return venv_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tFailed to create venv")

    return None


if __name__ == "__main__":
    # Create a virtual environment
    venv_path = create_venv(prefix="5/7")
    must_pass(venv_path is not None and venv_path.exists())
