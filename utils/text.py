"""Utilities for text manipulation"""
import string


def remove_xml_refs(raw_xml: str):
    """removes 'xml:' references from the document for easier processing"""
    return raw_xml.replace("xml:", "")


PUNCT = "\"#$%&'()*+,-/:<=>@[\\]^_`{|}~"


def remove_punctuation(text: str, keep_sentences: bool) -> str:
    """
    Replaces all punctuation from the text with spaces
    except for dots, exclamation marks and question marks.

    Parameters
    ----------
    text: str
        Text to alter
    keep_sentences: bool
        Specifies whether the normalization should keep sentence borders or not
        (exclamation marks, dots, question marks)

    Returns
    ----------
    text: str
        New string without punctuation
    """
    if keep_sentences:
        punctuation = PUNCT
    else:
        punctuation = string.punctuation
    return text.translate(str.maketrans(punctuation, " " * len(punctuation)))


def only_dots(text: str) -> str:
    """
    Exchanges all question marks and exclamation marks in the text for dots.

    Parameters
    ----------
    text: str
        Text to alter

    Returns
    ----------
    text: str
        New string containing only dots
    """
    return text.translate(str.maketrans({"?": ".", "!": ".", ";": "."}))


def remove_digits(text: str) -> str:
    """
    Removes all digits from the text.

    Parameters
    ----------
    text: str
        Text to alter

    Returns
    ----------
    text: str
        New string without digits
    """
    return text.translate(
        str.maketrans(string.digits, " " * len(string.digits))
    )
