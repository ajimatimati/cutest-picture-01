"""Sapphire-Eyed Cream Kitten Hugging Daisy Chick"""

__version__ = "2.0.0"

import hashlib
import logging
import os
import shutil
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def compute_sha256(file_path: Path) -> str:
    """Compute the SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def main() -> None:
    logging.info("Starting cutest-picture-01 entrypoint execution")

    src = Path(__file__).resolve().parent / "entry.png"
    if not src.exists() or not src.is_file():
        logging.error(f"Source file not found: {src}")
        sys.exit(1)

    src_size = src.stat().st_size
    if src_size == 0:
        logging.error(f"Source file is empty: {src}")
        sys.exit(1)

    src_sha256 = compute_sha256(src)
    logging.info(f"Source image validated: {src} ({src_size} bytes, sha256={src_sha256})")

    out_raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    out_path = Path(out_raw)

    if out_path.suffix or out_path.name.lower().endswith(".png"):
        dst = out_path
        out_dir = dst.parent
    else:
        out_dir = out_path
        dst = out_dir / "entry.png"

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logging.error(f"Failed to create output directory {out_dir}: {e}")
        sys.exit(1)

    try:
        shutil.copyfile(src, dst)
        logging.info(f"Copied {src} to {dst}")
    except OSError as e:
        logging.error(f"Failed to copy file to {dst}: {e}")
        sys.exit(1)

    if not dst.exists() or not dst.is_file():
        logging.error(f"Destination file does not exist: {dst}")
        sys.exit(1)

    dst_size = dst.stat().st_size
    if dst_size != src_size:
        logging.error(f"File size mismatch: src={src_size} bytes, dst={dst_size} bytes")
        sys.exit(1)

    dst_sha256 = compute_sha256(dst)
    if dst_sha256 != src_sha256:
        logging.error(f"Checksum mismatch: src={src_sha256}, dst={dst_sha256}")
        sys.exit(1)

    logging.info(
        f"Verification successful: copied {dst_size} bytes to {dst} (sha256={dst_sha256})"
    )

if __name__ == "__main__":
    main()
