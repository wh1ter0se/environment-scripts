import subprocess
from _config import PROJECTS
from _common import must_pass, format_prefix, run_cmd
from pathlib import Path


def install_projects(
    projects: list[Path] = PROJECTS,
    dependency_groups: list[str] = [],
    prefix: str | None = None,
) -> bool:
    print(format_prefix(prefix) + "Installing dependencies...")
    for path in projects:
        print(f"\tInstalling project '{path}'...")
        try:
            # Build the command
            cmd = ["uv", "pip", "install", str(path)]
            if len(dependency_groups) > 0:
                cmd.append("--group")
                cmd.extend(dependency_groups)

            # Run the command
            output = run_cmd(cmd, check=False)
            print(output.stderr.decode().strip())
            print(output.stdout.decode().strip())
            print(f"\tInstalled project '{path}'")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"\tFailed to install project '{path}': {e}")
            return False
    return True


if __name__ == "__main__":
    # Install dependencies in the virtual environment
    must_pass(install_projects(prefix="1/1"))
