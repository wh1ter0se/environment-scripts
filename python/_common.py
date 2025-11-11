import os
import re
import subprocess


class UvVersionInfo:
    major: int | None
    minor: int | None
    micro: int | None

    _stdout: bytes

    def __init__(self, stdout: bytes) -> None:
        # Store stdout
        self._stdout = stdout
        output = self._stdout.decode("utf-8").strip()

        # Match `uv X.Y.Z` optionally followed by `(hash YYYY-MM-DD)`
        pattern = r"^uv\s+(\d+)\.(\d+)\.(\d+)(?:\s+\(\S+\s+\d{4}-\d{2}-\d{2}\))?$"
        match = re.match(pattern, output)

        if match:
            self.major, self.minor, self.micro = map(int, match.groups())
        else:
            self.major = self.minor = self.micro = None

    def __str__(self) -> str:
        if None in (self.major, self.minor, self.micro):
            return "\tUnable to extract uv version information"
        return f"\tVersion: {self.major}.{self.minor}.{self.micro}"


def must_pass(value: bool) -> None:
    """Exit the program if the value is False."""
    if not value:
        print("[-] Exiting...")
        exit(1)


def format_prefix(prefix: str | None) -> str:
    """Format the prefix for logging."""
    if prefix is None:
        return "\t"
    return f"[{prefix}] "


def run_cmd(
    cmd: str | list[str],
    check: bool = False,
    stdout: int = subprocess.PIPE,
    stderr: int = subprocess.PIPE,
    shell: bool = False,
) -> subprocess.CompletedProcess:
    """Run a command and return the completed process."""
    return subprocess.run(
        cmd,
        check=check,
        stdout=stdout,
        stderr=stderr,
        shell=shell,
    )


def user_is_running_windows() -> bool:
    """Check if the user is running Windows."""
    return os.name == "nt"


def get_uv_version(prefix: str | None = None) -> UvVersionInfo | None:
    """Check if uv is installed."""
    print(format_prefix(prefix) + "Checking uv version...")
    try:
        # Check the version
        version_check_subproc = run_cmd(
            cmd=["uv", "--version"],
            check=True,
        )
        print("\tFound uv version")
        version = UvVersionInfo(stdout=version_check_subproc.stdout)
        print(str(version))
        return version
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tNo installations of uv found")
        return None
