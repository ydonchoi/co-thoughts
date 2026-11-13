"""Load the full text of a source the user obtained themselves.

When SARA can read only an abstract, the user can supply the document (a
paywalled article, or a page whose site refuses automated clients). This
module only reads and extracts text; SARA decides whether the document is the
work it cites, by comparing it with the title and abstract it fetches itself.

Supported: PDF (with the optional ``pypdf`` package), plain text, Markdown and
HTML. A scanned PDF has no text layer and is refused rather than guessed at.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

MAX_FILE_BYTES = 50_000_000
# SARA's limits for one document's extracted text.
MIN_TEXT_CHARS = 500
MAX_TEXT_CHARS = 2_000_000
# Plan-wide bounds: every loaded text is kept in memory until the run ends.
MAX_DOCUMENTS_PER_PLAN = 20
MAX_TOTAL_TEXT_CHARS = 10_000_000
TEXT_SUFFIXES = {".txt": "text/plain", ".md": "text/markdown"}
HTML_SUFFIXES = {".html": "text/html", ".htm": "text/html"}
PDF_SUFFIX = ".pdf"
_SPACES = re.compile(r"[ \t\f\v]+")
_LINE_EDGES = re.compile(r" *\n *")
_BLANK_LINES = re.compile(r"\n{3,}")
# Whitespace shrinks in normalization, so raw text may exceed the cap somewhat; beyond
# this it is refused before any normalization work is done.
RAW_TEXT_FACTOR = 4


class _TextOnly(HTMLParser):
    _SKIP = {"script", "style", "noscript", "template", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skipping = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag in self._SKIP:
            self._skipping += 1
        elif tag in {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skipping:
            self._skipping -= 1

    def handle_data(self, data: str) -> None:
        if not self._skipping:
            self.parts.append(data)


def _decode(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("DOCUMENT_ENCODING_UNSUPPORTED")


def _pdf_text(path: Path) -> tuple[str, int]:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ValueError("PDF_SUPPORT_UNAVAILABLE") from None
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted and not reader.decrypt(""):
            raise ValueError("PDF_ENCRYPTED")
        pages: list[str] = []
        total = 0
        for page in reader.pages:
            text = page.extract_text() or ""
            total += len(text)
            # Stop at the page that crosses the bound, before keeping the rest.
            if total > MAX_TEXT_CHARS * RAW_TEXT_FACTOR:
                raise ValueError("USER_DOCUMENT_TEXT_TOO_LONG")
            pages.append(text)
    except ValueError as exc:
        if str(exc) in {"PDF_ENCRYPTED", "USER_DOCUMENT_TEXT_TOO_LONG"}:
            raise
        raise ValueError("PDF_UNREADABLE") from None
    except Exception:
        # A malformed file can fail anywhere in the parser, with any exception type;
        # report one stable code, never the parser's message.
        raise ValueError("PDF_UNREADABLE") from None
    return "\n\n".join(pages), len(pages)


def _tidy(text: str) -> str:
    # Whole-string substitutions: no per-line list is built, whatever the line count.
    text = _SPACES.sub(" ", text.replace("\r\n", "\n").replace("\r", "\n"))
    return _BLANK_LINES.sub("\n\n", _LINE_EDGES.sub("\n", text)).strip()


def _cites(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("USER_DOCUMENT_CITES_INVALID")
    try:
        parsed = urlparse(value)
        port = parsed.port
    except ValueError:
        raise ValueError("USER_DOCUMENT_CITES_INVALID") from None
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.fragment or port not in (None, 443) or any(ch.isspace() for ch in value)):
        raise ValueError("USER_DOCUMENT_CITES_INVALID")
    return value


def load_user_document(path: Any, *, cites: Any, claim_refs: Iterable[str] = ()) -> dict[str, Any]:
    """Read one file and return its extracted text with a digest of that text."""
    if not isinstance(path, (str, Path)) or not str(path).strip():
        raise ValueError("USER_DOCUMENT_PATH_INVALID")
    file = Path(path)
    if not file.is_file():
        raise ValueError("USER_DOCUMENT_NOT_FOUND")
    if file.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("USER_DOCUMENT_FILE_TOO_LARGE")
    refs = list(claim_refs)
    if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        raise ValueError("USER_DOCUMENT_CLAIM_REFS_INVALID")
    suffix = file.suffix.lower()
    pages = None
    if suffix == PDF_SUFFIX:
        raw_text, pages = _pdf_text(file)
        media_type = "application/pdf"
    elif suffix in TEXT_SUFFIXES:
        raw_text, media_type = _decode(file.read_bytes()), TEXT_SUFFIXES[suffix]
    elif suffix in HTML_SUFFIXES:
        parser = _TextOnly()
        parser.feed(_decode(file.read_bytes()))
        raw_text, media_type = "".join(parser.parts), HTML_SUFFIXES[suffix]
    else:
        raise ValueError("USER_DOCUMENT_TYPE_UNSUPPORTED")
    if len(raw_text) > MAX_TEXT_CHARS * RAW_TEXT_FACTOR:
        raise ValueError("USER_DOCUMENT_TEXT_TOO_LONG")
    text = _tidy(raw_text)
    if len(text) < MIN_TEXT_CHARS:
        # A scanned PDF or an image-only page: there is nothing to check or assess.
        raise ValueError("USER_DOCUMENT_TEXT_TOO_SHORT")
    if len(text) > MAX_TEXT_CHARS:
        raise ValueError("USER_DOCUMENT_TEXT_TOO_LONG")
    return {"file_name": file.name, "media_type": media_type, "pages": pages, "cites": _cites(cites),
            "claim_refs": list(dict.fromkeys(refs)), "text": text,
            "sha256": sha256(text.encode("utf-8")).hexdigest(), "chars": len(text)}


def load_user_documents(value: Any) -> list[dict[str, Any]]:
    """Load ``[{"path", "cites", "claim_refs"?}, ...]``; the same file and source once."""
    if value is None:
        return []
    if isinstance(value, (str, bytes, Mapping)) or not isinstance(value, Iterable):
        raise ValueError("USER_DOCUMENTS_INVALID")
    items = list(value)
    if len(items) > MAX_DOCUMENTS_PER_PLAN:
        raise ValueError("USER_DOCUMENTS_TOO_MANY")  # before any file is read
    loaded: list[dict[str, Any]] = []
    total = 0
    for item in items:
        if not isinstance(item, Mapping):
            raise ValueError("USER_DOCUMENTS_INVALID")
        refs = item.get("claim_refs", ())
        if isinstance(refs, (str, bytes)) or not isinstance(refs, Iterable):
            raise ValueError("USER_DOCUMENT_CLAIM_REFS_INVALID")
        doc = load_user_document(item.get("path"), cites=item.get("cites"), claim_refs=refs)
        same = next((d for d in loaded if d["sha256"] == doc["sha256"] and d["cites"] == doc["cites"]), None)
        if same is not None:
            same["claim_refs"] = list(dict.fromkeys(same["claim_refs"] + doc["claim_refs"]))
            continue
        total += doc["chars"]
        if total > MAX_TOTAL_TEXT_CHARS:
            raise ValueError("USER_DOCUMENTS_TOO_LARGE")
        loaded.append(doc)
    return loaded


def document_summary(doc: Mapping[str, Any]) -> dict[str, Any]:
    """What a preview shows of a document: never its text."""
    return {key: doc[key] for key in ("file_name", "media_type", "pages", "cites", "claim_refs", "sha256", "chars")}
