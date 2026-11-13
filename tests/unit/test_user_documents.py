import hashlib
import json

import pytest

from conversation_verification import run_plan
from test_sara_v3_integration import (
    USER_CLAIM, Backend, RecordingSARA, envelope, request, runtime, sara_result, verify,
)
from user_documents import load_user_document, load_user_documents

CITES = "https://doi.org/10.1000/example.1"
OTHER = "https://doi.org/10.1000/other.2"
PARAGRAPH = ("Household transmission after universal masking was measured in a cluster randomized trial "
             "across 240 households over eight weeks of weekly testing. ")
TEXT = PARAGRAPH * 8


def pdf_bytes(lines):
    """A minimal one-page PDF with a text layer, one line per entry."""
    stream = "BT /F1 10 Tf 40 800 Td 12 TL " + " ".join(
        "(" + line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ") '" for line in lines) + " ET"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{offset:010d} 00000 n \n" for offset in offsets).encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


def _pdf_supported():
    try:
        import pypdf  # noqa: F401
        return True
    except ImportError:
        return False


needs_pypdf = pytest.mark.skipif(not _pdf_supported(), reason="pypdf is an optional dependency")


@pytest.fixture
def files(tmp_path):
    paths = {}
    paths["txt"] = tmp_path / "paper.txt"
    paths["txt"].write_text(TEXT, encoding="utf-8")
    paths["md"] = tmp_path / "notes.md"
    paths["md"].write_text("# Title\n\n" + TEXT, encoding="utf-8")
    paths["html"] = tmp_path / "page.html"
    paths["html"].write_text(f"<html><head><title>x</title><style>p{{}}</style></head><body>"
                             f"<script>var secret=1</script><p>{TEXT}</p></body></html>", encoding="utf-8")
    paths["cp949"] = tmp_path / "korean.txt"
    paths["cp949"].write_bytes(("가구 내 전파 연구 결과입니다. " * 60).encode("cp949"))
    paths["pdf"] = tmp_path / "paper.pdf"
    paths["pdf"].write_bytes(pdf_bytes([PARAGRAPH] * 8))
    paths["scan"] = tmp_path / "scan.pdf"
    paths["scan"].write_bytes(pdf_bytes([]))
    return paths


# -- loading ------------------------------------------------------------------------------------
@pytest.mark.parametrize("kind, media", [("txt", "text/plain"), ("md", "text/markdown"), ("html", "text/html"),
                                         pytest.param("pdf", "application/pdf", marks=needs_pypdf)])
def test_supported_files_are_read_and_digested(files, kind, media):
    doc = load_user_document(files[kind], cites=CITES)
    assert doc["media_type"] == media and "Household transmission" in doc["text"]
    assert doc["sha256"] == hashlib.sha256(doc["text"].encode("utf-8")).hexdigest()
    assert doc["file_name"] == files[kind].name and doc["chars"] == len(doc["text"])
    if kind == "html":
        assert "secret" not in doc["text"] and "<p>" not in doc["text"]
    if kind == "pdf":
        assert doc["pages"] == 1


def test_korean_text_in_cp949_is_decoded(files):
    assert "가구 내 전파" in load_user_document(files["cp949"], cites=CITES)["text"]


@pytest.mark.parametrize("change, code", [
    ({"path": "missing.pdf"}, "USER_DOCUMENT_NOT_FOUND"),
    ({"cites": "http://doi.org/10.1/x"}, "USER_DOCUMENT_CITES_INVALID"),
    ({"cites": "https://user:pw@doi.org/x"}, "USER_DOCUMENT_CITES_INVALID"),
    ({"cites": "https://doi.org/x#frag"}, "USER_DOCUMENT_CITES_INVALID"),
])
def test_bad_paths_and_citations_are_refused(files, change, code):
    item = {"path": files["txt"], "cites": CITES, **change}
    with pytest.raises(ValueError, match=code):
        load_user_document(item["path"], cites=item["cites"])


@needs_pypdf
def test_scanned_pdf_and_unsupported_types_are_refused(files, tmp_path):
    with pytest.raises(ValueError, match="USER_DOCUMENT_TEXT_TOO_SHORT"):
        load_user_document(files["scan"], cites=CITES)
    image = tmp_path / "figure.png"
    image.write_bytes(b"\x89PNG")
    with pytest.raises(ValueError, match="USER_DOCUMENT_TYPE_UNSUPPORTED"):
        load_user_document(image, cites=CITES)
    broken = tmp_path / "broken.pdf"
    broken.write_bytes(b"not a pdf at all")
    with pytest.raises(ValueError, match="PDF_UNREADABLE"):
        load_user_document(broken, cites=CITES)


def test_pdf_without_pypdf_is_reported(files, monkeypatch):
    import builtins
    real = builtins.__import__

    def fake(name, *args, **kwargs):
        if name.startswith("pypdf"):
            raise ImportError(name)
        return real(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake)
    with pytest.raises(ValueError, match="PDF_SUPPORT_UNAVAILABLE"):
        load_user_document(files["pdf"], cites=CITES)


def test_the_same_file_for_the_same_source_is_loaded_once(files):
    loaded = load_user_documents([{"path": files["txt"], "cites": CITES, "claim_refs": ["A"]},
                                  {"path": files["txt"], "cites": CITES, "claim_refs": ["B"]},
                                  {"path": files["txt"], "cites": OTHER}])
    assert len(loaded) == 2 and loaded[0]["claim_refs"] == ["A", "B"]
    with pytest.raises(ValueError, match="USER_DOCUMENTS_INVALID"):
        load_user_documents({"path": files["txt"]})


# -- plan ----------------------------------------------------------------------------------------
def setup(sara=None, **claims):
    sara = sara or RecordingSARA()
    rt = runtime(Backend(), sara)
    rt.run(request(user_claims=claims.get("user_claims", USER_CLAIM)))
    return rt, sara


@needs_pypdf
def test_preview_lists_each_document_without_its_text(files):
    rt, sara = setup()
    docs = [{"path": files["pdf"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}]
    plan = rt.plan_conversation_verification("CONV-1", user_documents=docs)
    [summary] = plan["preview"]["user_documents"]
    assert summary["file_name"] == "paper.pdf" and summary["cites"] == CITES and summary["calls"] == 1
    assert summary["document"] == "D1" and summary["media_type"] == "application/pdf"
    assert plan["preview"]["document_chars_to_sara"] == summary["chars"]
    assert plan["preview"]["document_excerpt_chars_per_claim_max"] == 30_000
    assert "Household transmission" not in json.dumps(plan)
    assert sara.turns == []  # previewing sends nothing


def test_a_changed_file_needs_a_new_confirmation(files):
    rt, _ = setup()
    docs = [{"path": files["txt"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}]
    plan = rt.plan_conversation_verification("CONV-1", user_documents=docs)
    assert plan["plan_id"] != rt.plan_conversation_verification("CONV-1")["plan_id"]
    files["txt"].write_text(TEXT + " Edited after the preview.", encoding="utf-8")
    with pytest.raises(PermissionError, match="VERIFICATION_PLAN_NOT_CONFIRMED"):
        rt.verify_conversation("CONV-1", confirmation=plan["plan_id"], user_documents=docs)


def test_documents_attach_by_claim_or_by_the_url_a_claim_cites(files):
    claims = [{"id": "U1", "text": "Masks cut transmission.", "source_urls": [CITES]}]
    rt, sara = setup(user_claims=claims)
    by_url = [{"path": files["txt"], "cites": CITES}]
    plan, result = verify(rt, user_documents=by_url)
    user_batch = [t for t in sara.turns if t.get("user_documents")]
    assert len(user_batch) == 1 and user_batch[0]["claim_candidates"][0]["text"] == "Masks cut transmission."
    [sent] = user_batch[0]["user_documents"]
    assert set(sent) == {"id", "cites", "text", "sha256"} and sent["id"] == "D1"
    assert sent["sha256"] == hashlib.sha256(sent["text"].encode("utf-8")).hexdigest()
    assert all("user_documents" not in t for t in sara.turns if t is not user_batch[0])
    report = [b for b in result["batches"] if b["role"] == "USER"][0]
    assert report["sent_scope"]["user_documents"] == ["D1"]


@pytest.mark.parametrize("docs, code", [
    (lambda f: [{"path": f["txt"], "cites": OTHER}], "USER_DOCUMENT_NOT_ATTACHED"),
    (lambda f: [{"path": f["txt"], "cites": CITES, "claim_refs": ["TURN-9:USER:U1"]}],
     "USER_DOCUMENT_CLAIM_REF_NOT_RECORDED"),
])
def test_documents_that_would_go_nowhere_are_refused(files, docs, code):
    rt, _ = setup()
    with pytest.raises(ValueError, match=code):
        rt.plan_conversation_verification("CONV-1", user_documents=docs(files))


def test_a_document_outside_the_selection_is_refused(files):
    rt, _ = setup()
    docs = [{"path": files["txt"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}]
    with pytest.raises(ValueError, match="USER_DOCUMENT_NOT_ATTACHED"):
        rt.plan_conversation_verification("CONV-1", claim_refs=["TURN-1:ASSISTANT:C1"], user_documents=docs)


def test_more_than_five_documents_for_one_call_are_refused(files, tmp_path):
    rt, _ = setup()
    docs = []
    for n in range(6):
        path = tmp_path / f"d{n}.txt"
        path.write_text(TEXT + f" copy {n}", encoding="utf-8")
        docs.append({"path": path, "cites": f"{CITES}{n}", "claim_refs": ["TURN-1:USER:U1"]})
    with pytest.raises(ValueError, match="USER_DOCUMENTS_PER_CALL_EXCEEDED"):
        rt.plan_conversation_verification("CONV-1", user_documents=docs)


def test_run_refuses_documents_other_than_the_planned_ones(files):
    rt, _ = setup()
    docs = load_user_documents([{"path": files["txt"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}])
    plan = rt._plan("CONV-1", None, None, docs)[0]
    other = load_user_documents([{"path": files["md"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}])
    with pytest.raises(ValueError, match="USER_DOCUMENTS_DO_NOT_MATCH_PLAN"):
        run_plan(plan, rt.sara_v3_connection, other)


# -- results -------------------------------------------------------------------------------------
class DocumentSARA(RecordingSARA):
    """Reports each sent document as MATCHED and asks for one more source per claim."""

    def __call__(self, turn, timeout_seconds):
        self.turns.append(json.loads(json.dumps(turn)))
        envelopes = []
        for item in turn["claim_candidates"]:
            env = envelope(item["id"], status="PARTIALLY_VERIFIED")
            env["user_documents"] = [{"id": d["id"], "cites": d["cites"], "sha256": d["sha256"], "identity": "MATCHED",
                                      "reason_code": None, "title_score": 1.0, "abstract_score": 0.92}
                                     for d in turn.get("user_documents", [])]
            env["user_documents"].append({"id": "D9", "sha256": "0" * 64, "identity": "MATCHED"})  # not ours
            for d in turn.get("user_documents", []):  # our id, but not the document this plan sent
                env["user_documents"].append({"id": d["id"], "sha256": "f" * 64, "identity": "UNMATCHED"})
            env["full_text_requests"] = [{"url": OTHER, "title": "Other trial", "access_level": "ABSTRACT"},
                                         {"url": "javascript:alert(1)", "title": "bad"}]
            envelopes.append(env)
        return sara_result(*envelopes)


@needs_pypdf
def test_results_map_document_verdicts_to_files_and_collect_requests(files):
    rt, _ = setup(sara=DocumentSARA())
    docs = [{"path": files["pdf"], "cites": CITES, "claim_refs": ["TURN-1:USER:U1"]}]
    _, result = verify(rt, user_documents=docs)
    user = [c for c in result["claim_results"] if c["role"] == "USER"][0]
    assert user["user_documents"] == [{"document": "D1", "file_name": "paper.pdf", "cites": CITES,
                                       "identity": "MATCHED", "title_score": 1.0, "abstract_score": 0.92}]
    assert user["full_text_requests"] == [{"url": OTHER, "title": "Other trial", "access_level": "ABSTRACT"}]
    [request_entry] = result["full_text_requests"]
    assert request_entry["url"] == OTHER and set(request_entry["claim_refs"]) == {
        c["claim_ref"] for c in result["claim_results"]}
    assert result["verification_status"] == "UNVERIFIED" and result["is_evidence"] is False


def test_results_without_documents_still_carry_an_empty_request_list():
    rt, _ = setup()
    _, result = verify(rt)
    assert result["full_text_requests"] == []
    assert all("user_documents" not in c for c in result["claim_results"])
