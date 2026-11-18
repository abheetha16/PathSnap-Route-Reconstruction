"""Shared path settings for this member's stage of PathSnap.

All four member folders (Abhay, Abheek, Abeetha, Abhinav) read and write the SAME artifacts folder,
so each stage picks up the previous stage's outputs.
Override with environment variables:
  PATHSNAP_DATA       folder that contains train/ and student_test/   (default: <split root>/../Student folder)
  PATHSNAP_ARTIFACTS  shared artifacts folder                          (default: <split root>/artifacts)
"""
import os
from pathlib import Path

MEMBER_DIR = Path(__file__).resolve().parents[1]
SPLIT_ROOT = MEMBER_DIR.parent
ARTIFACTS = Path(os.environ.get("PATHSNAP_ARTIFACTS", SPLIT_ROOT / "artifacts"))
DATA_ROOT = Path(os.environ.get("PATHSNAP_DATA", SPLIT_ROOT.parent / "Student folder"))


def ART(sub: str = "") -> str:
    """Path inside the shared artifacts folder (parent folders are created)."""
    p = ARTIFACTS / sub
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def DATA(partition: str) -> str:
    """Path of a dataset partition folder, e.g. DATA("train")."""
    return str(DATA_ROOT / partition)
