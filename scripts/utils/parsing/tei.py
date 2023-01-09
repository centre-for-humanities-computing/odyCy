"""Utilities for parsing texts from Perseus"""
from typing import Tuple

from lxml import etree

from utils.parsing._parse import Parser, Document


def get_text(tree: etree.ElementTree) -> str:
    """Extracts the contents of all text elements from the tree except for
    notes.
    """
    # matches all elements, that are descendants of the "text" element
    # but are not note elements or descendants of a note element
    # in short it basically just ignores notes, cause we don't want
    # to have them in the output
    texts = tree.xpath(
        """//
            *[local-name() = 'text']//
            *[not(local-name() = 'note') and
              not(ancestor::*[local-name() = 'note'
            ])
        ]/text()"""
    )
    texts = [text.strip() for text in texts if text]
    text = "\n".join(texts)  # join_lines(texts)
    # text = remove_double_linebreaks(text)
    return text


def get_id(path: str) -> str:
    """Get Perseus ID of file given its path."""
    file_name = path.split("/")[-1]
    perseus_id = file_name[: file_name.find(".xml")]
    return f"perseus_{perseus_id}"


class TEIParser(Parser):
    """Parser for TEI files."""

    @staticmethod
    def parse_file(file: str) -> Tuple[Document]:
        """Parses file into a document"""
        tree = etree.parse(file)
        doc: Document = {
            "id": get_id(path=file),
            "text": get_text(tree=tree),
        }
        return (doc,)
