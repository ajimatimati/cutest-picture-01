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

def main():
    logging.info("Starting cutest-picture-01 entrypoint execution")
    src = Path(__file__).parent / "entry.png"
    if not src.exists() or not src.is_file():
        logging.error(f"Source file not found: {src}")
        sys.exit(1)

    src_size = src.stat().st_size
    logging.info(f"Source image validated: {src} ({src_size} bytes)")
    if src_size == 0:
        logging.error(f"Source file is empty: {src}")
        sys.exit(1)

    out_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_dir = Path(out_dir_env)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logging.error(f"Failed to create output directory {out_dir}: {e}")
        sys.exit(1)

    dst = out_dir / "entry.png"
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

    logging.info(f"Verification successful: copied {dst_size} bytes to {dst}")

if __name__ == "__main__":
    main()

