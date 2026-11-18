
import os
from pathlib import Path

# Project directories
MEMBER_DIR = Path(__file__).resolve().parents[1]
SPLIT_ROOT = MEMBER_DIR.parent
REPO_ROOT = SPLIT_ROOT.parent

# Shared artifact directory
ARTIFACTS = Path(
    os.environ.get(
        "PATHSNAP_ARTIFACTS",
        SPLIT_ROOT / "artifacts"
    )
)

# Dataset directory
DATA_ROOT = Path(
    os.environ.get(
        "PATHSNAP_DATA",
        REPO_ROOT / "datasets"
    )
)

# Map the original partition names to the final repository names
PARTITION_MAP = {
    "train": "training",
    "student_test": "student_testing",
    "evaluator_test": "evaluator_testing"
}


def ART(sub: str = "") -> str:
    """Return a path inside the shared artifacts directory."""
    p = ARTIFACTS / sub
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def DATA(partition: str) -> str:
    """Return the appropriate dataset partition path."""
    folder = PARTITION_MAP.get(partition, partition)
    return str(DATA_ROOT / folder)
