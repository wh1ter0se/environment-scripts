import os
import re
import subprocess
import datetime as dt

NUM_STEPS = 3


class UvVersionInfo:
    version: str | None
    hash: str | None
    build_date: str | None

    _stdout: bytes

    def __init__(self, stdout: bytes) -> None:
        # Store stdout
        self._stdout = stdout

        # Parse the output
        output = self._stdout.decode("utf-8").strip()
        pattern = r"^uv\s+(\S+)\s+\((\S+)\s+(\d{4}-\d{2}-\d{2})\)$"
        match = re.match(pattern=pattern, string=output)
        if match is None:
            self.version = None
            self.hash = None
            self.build_date = None
            return

        # Store the fields if the regex got parsed
        self.version, self.hash, self.build_date = match.groups()

    def __str__(self) -> str:
        if self.version is None or self.hash is None or self.build_date is None:
            return "\tUnable to extract uv version information"

        return (
            f"\tVersion: {self.version}\n"
            f"\tBuild Hash: {self.hash}\n"
            f"\tBuild Date: {self.build_date}"
        )


def user_is_running_windows():
    """Check if the user is running Windows."""
    return os.name == "nt"


def uv_is_installed() -> bool:
    """Check if uv is installed."""
    try:
        # Check the version
        version_check_subproc = subprocess.run(
            args=["uv", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        print(f"[1/{NUM_STEPS}] Discovered uv installation")

        # Parse the output
        output = version_check_subproc.stdout.decode("utf-8").strip()
        pattern = r"^uv\s+(\S+)\s+\((\S+)\s+(\d{4}-\d{2}-\d{2})\)$"
        match = re.match(pattern=pattern, string=output)

        # Print the version info
        if not match:
            print("\tUnable to extract uv version information")
        else:
            version, hash_str, date_str = match.groups()
            print(f"\tVersion: {version}")
            print(f"\tBuild Hash: {hash_str}")
            print(f"\tBuild Date: {date_str}")

        return True
    except subprocess.CalledProcessError:
        print(f"[1/{NUM_STEPS}] No installations of uv discovered")
        return False


def install_uv() -> None:
    """Install uv, if not already installed."""

    # Install via curl if we can
    if not user_is_running_windows():
        print(f"[2/{NUM_STEPS}] *nix detected, installing uv via curl...")
        try:
            subprocess.run(
                args=[
                    "curl",
                    "-LsSf",
                    "https://astral.sh/uv/install.sh",
                    "|",
                    "sh",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
            )
            subprocess.run(
                args=["uv", "--version"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
            )
            print("\tSuccessfully installed uv via curl")
        except subprocess.CalledProcessError:
            print("\tFailed to install uv via curl")

    # Windows install
    print(f"[2/{NUM_STEPS}] Installing uv via pip...")
    try:
        subprocess.run(
            ["pip", "install", "uv"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
        subprocess.run(
            args=["uv", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=False,
        )
    except subprocess.CalledProcessError:
        print("\tFailed to install uv via pip.")
        raise

    # *nix install
    else:
        print(f"[2/{NUM_STEPS}] *nix detected, installing uv via curl...")
        subprocess.run(
            ["curl ", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"],
            shell=True,
        )


def update_uv() -> None:
    """Update uv to the latest version."""
    # Early exit if uv is not installed
    if not uv_is_installed():
        return

    # Windows update
    if user_is_running_windows():
        subprocess.run(["pip", "install", "--upgrade", "uv"])

    # macOS/Linux update
    else:
        subprocess.run(
            ["uv", "self-update"],
            shell=True,
        )


def setup_environment() -> None:
    """Set up the environment by installing or updating uv."""
    if not uv_is_installed():
        install_uv()
    update_uv()
