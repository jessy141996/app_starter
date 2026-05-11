import os

from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute path to a .pdf or .docx file on disk"),
) -> str:
    """Convert a document on disk to markdown-formatted text.

    Reads a PDF or DOCX file from the given path and returns its content as
    a markdown string. This wraps the lower-level binary_document_to_markdown
    function so callers only need to provide a file path.

    When to use:
    - When you have a file path to a PDF or DOCX document and need its text content
    - When you want markdown output from a local document without handling bytes yourself

    When NOT to use:
    - When you already have the file bytes in memory (use binary_document_to_markdown instead)
    - For file types other than PDF and DOCX

    Examples:
    >>> document_path_to_markdown("/path/to/report.pdf")
    '# Report Title\\n\\nReport content...'
    >>> document_path_to_markdown("/path/to/notes.docx")
    '# Notes\\n\\n- Item 1\\n- Item 2'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path)
    ext = ext.lstrip(".").lower()

    supported = {"pdf", "docx"}
    if ext not in supported:
        raise ValueError(
            f"Unsupported file extension '.{ext}'. Supported extensions: {', '.join(sorted(supported))}"
        )

    with open(file_path, "rb") as f:
        binary_data = f.read()

    return binary_document_to_markdown(binary_data, ext)
