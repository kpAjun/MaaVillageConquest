import sys

from typing import List
from pathlib import Path

from maa.resource import Resource
from maa.tasker import Tasker, LoggingLevelEnum


def check(dirs: List[Path]) -> bool:
    resource = Resource()

    # Expand any provided parent directories into their immediate child directories
    expanded: List[Path] = []
    for d in dirs:
        if d.is_dir():
            # If the directory looks like a bundle (has pipeline/model/image/etc) check it directly,
            # otherwise iterate immediate subdirectories and check each one.
            has_bundle_files = any((d / name).exists() for name in ("pipeline", "model", "image"))
            if has_bundle_files:
                expanded.append(d)
            else:
                for child in sorted(d.iterdir()):
                    if child.is_dir():
                        expanded.append(child)
        else:
            expanded.append(d)

    print(f"Checking {len(expanded)} directories...")

    for dir in expanded:
        print(f"Checking {dir}...")
        status = resource.post_bundle(dir).wait().status
        if not status.succeeded:
            print(f"Failed to check {dir}.")
            return False

    print("All directories checked.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_resource.py <directories...>")
        sys.exit(1)

    Tasker.set_stdout_level(LoggingLevelEnum.All)

    dirs = [Path(arg) for arg in sys.argv[1:]]
    if not check(dirs):
        sys.exit(1)


if __name__ == "__main__":
    main()
