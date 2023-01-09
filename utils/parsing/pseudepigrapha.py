from typing import Iterable, List, Optional, TypeVar

from lxml import etree

from utils.parsing._parse import Parser, Document
from utils.text import remove_punctuation

T = TypeVar("T")


def unique(iterable: Iterable[T]) -> List[T]:
    """Turns iterable into the list of its unique elements."""
    return list(set(iterable))


def get_versions(book: etree.Element) -> List[etree.Element]:
    """Returns all versions of the book."""
    tree = etree.ElementTree(book)
    # Matches all version elements
    versions = tree.xpath("version")
    return versions


def _normalize(text: Optional[str]) -> Optional[str]:
    # propagate nones
    if text is None:
        return None
    text = remove_punctuation(text, keep_sentences=False)
    text = text.strip()
    return text


def get_language(version: etree.Element) -> str:
    """Extracts language from document."""
    version_language = version.get("language")
    version_tree = etree.ElementTree(version)
    # Matches the language attribute of all ms tags
    manuscript_languages = version_tree.xpath("//ms/@language")
    manuscript_languages = unique(manuscript_languages)
    # I checked and there is always only one language, so doing this is fine
    if manuscript_languages:
        manuscript_language = manuscript_languages[0]
    else:
        manuscript_language = ""
    if version_language:
        return version_language
    else:
        return manuscript_language


def get_text(version: etree.Element) -> str:
    """Extracts textual content from a version of the book."""
    version_tree = etree.ElementTree(version)
    texts = version_tree.xpath("//reading/text()")
    text = "\n".join(texts)
    return text


def get_id(version: etree.Element, book: etree.Element) -> str:
    """Extracts file ID from book."""
    book_id = book.get("filename", "")
    version_title = version.get("title", "")
    version_title = _normalize(version_title)
    return f"pseudepigrapha_{book_id}-{version_title}"


class PseudepigraphaParser(Parser):
    def parse_file(self, file: str) -> Iterable[Document]:
        """Parses the file into an iterable of documents"""
        tree = etree.parse(file)
        # Matches first book element in the parse tree (there's only one)
        book = tree.xpath("/book")[0]
        book_tree = etree.ElementTree(book)
        # Matches all verison elements in the tree under book
        versions = book_tree.xpath("version")
        for version in versions:
            language = get_language(version)
            doc: Document = {
                "id": get_id(version=version, book=book),
                "text": get_text(version=version),
            }
            # NOTE: Questionable solution, consider moving filtering up
            # a couple of levels.
            if language == "Greek":
                yield doc
