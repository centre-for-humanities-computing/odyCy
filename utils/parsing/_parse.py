"""Module for defining parsers for the project."""
import os
import pathlib
from typing import Protocol, TypedDict, Iterable

import pandas as pd
from lxml import etree


class Document(TypedDict):
    """Interface for documents."""

    id: str
    text: str


class Parser(Protocol):
    """Interface for parsers."""

    def parse_file(self, file: str) -> Iterable[Document]:
        """Turns the given file into an iterable of documents."""
        pass


def out_filename(doc: Document) -> str:
    """Creates filename for the output file."""
    return f"{doc['id']}.txt"


def process_files(paths: Iterable[str], parser: Parser, out_dir: str):
    """Parses the given file and puts it in the output folder.
    The output folder will also have an index.csv file with ids
    and information about source and destination files.

    Parameters
    ----------
    paths: iterable of str
        Paths to the files that have to be processed.
    parser: Parser
        Parser object to parse the files into documents.
    out_dir: str
        Path to output directory.

    Note
    ----
    This function doesn't stop if it encounters corrupted files,
    but lists them in a corrput_files.log file in the output directory.
    """
    # Creating directory if it doesn't exist
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    corrupt_path = os.path.join(out_dir, "corrupt_files.log")
    index_records = []
    with open(corrupt_path, "w") as f:
        f.write("")
    for path in paths:
        print(f"processing: {path}")
        try:
            docs = list(parser.parse_file(path))
            # NOTE: This error is implementation detail and should be hidden
            # by the Parser interface
        except etree.XMLSyntaxError:
            with open(corrupt_path, "a") as f:
                f.write(path + "\n")
            continue
        for doc in docs:
            out_path = os.path.join(out_dir, f"{doc['id']}.txt")
            with open(out_path, "w") as f:
                f.write(doc["text"])
            index_records.append({"source": path, "dest": out_path})
    index_df = pd.DataFrame.from_records(index_records)
    index_path = os.path.join(out_dir, "index.csv")
    index_df.to_csv(index_path, index=False)
