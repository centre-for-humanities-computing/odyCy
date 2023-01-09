"""Script for parsing raw pretraining data."""

import os
import glob

import pandas as pd

from utils.parsing import process_files, TEIParser, PseudepigraphaParser

FILE_PATTERNS = {
    "perseus": "assets/pretraining/raw/perseus/**/*grc*.xml",
    "first1k": "assets/pretraining/raw/first1k/**/*grc*.xml",
    "pseudepigrapha": "assets/pretraining/raw/pseudepigrapha/**/*.xml",
}
PARSERS = {
    "perseus": TEIParser,
    "first1k": TEIParser,
    "pseudepigrapha": PseudepigraphaParser,
}
OUT_DIR = "assets/pretraining/parsed"


def join_indices(out_dir: str) -> pd.DataFrame:
    """Finds indices for all input corpora and joins them."""
    index_paths = glob.glob(os.path.join(out_dir, "**/index.csv"))
    index_dfs = (pd.read_csv(file) for file in index_paths)
    return pd.concat(index_dfs, ignore_index=True)


def main() -> None:
    print("Parsing pretraining datasets:")
    for name, pattern in FILE_PATTERNS.items():
        print(f" - {name}")
        parser = PARSERS[name]
        paths = glob.glob(pattern, recursive=True)
        dest = os.path.join(OUT_DIR, name)
        process_files(paths=paths, parser=parser, out_dir=dest)
    print("Producing joint index.")
    joint_index = join_indices(OUT_DIR)
    print("Saving.")
    joint_index.to_csv(os.path.join(OUT_DIR, "index.csv"))
    print("DONE")


if __name__ == "__main__":
    main()
