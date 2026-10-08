# T24 — Notion Representation Mapping / Expressiveness Test v0.1

Status: CONDITIONAL PASS.

## 1. Source schema
Data Source: 사고 메모 연구노트
The current schema was fetched directly from the connected Notion data source.

## 2. Logical-to-Notion mapping

| Logical entity | Current Notion representation | Assessment |
|---|---|---|
| Research Object | Research Object ID + note page/body | PARTIAL |
| Research Note | One row/page with extensive metadata + body | PASS |
| Claim | Claim ID text + body | PARTIAL |
| Evidence | Evidence Mapping text + 근거 상태 + body | PARTIAL |
| Verification | 검증메모 + SARA 상태 + 인식론적 상태 | PARTIAL |
| Transformation Event | Transformation Trace text | PARTIAL |
| Relation | 연구노트 관계 / 관련 연구노트 text | PARTIAL |
| Version/Revision | 버전 + Revision Type + 이전 연구노트 | PARTIAL |
| Branch | Branch ID text | PARTIAL |
| Provenance | 생성 출처 / 원대화 참조 / 생성 일시 / 응답모델 | PARTIAL |
| D9 Gate | D9 상태 + body G1-G6 | PARTIAL |
| Taxonomy | 분류 코드 / 연구 목적 / 문서 유형 etc. | PASS for current note representation |

The architecture does not require one Notion database per logical entity; the current collapsed representation is allowed by the data model if semantics and provenance remain explicit.

## 3. Expressiveness findings

### PASS
- Existing Research Note representation can preserve document-level metadata.
- Primary Research Purpose and Document Type are directly represented.
- Note-level epistemic state is representable.
- SARA lifecycle status is representable.
- Research Object, Claim, Evidence and Transformation can be referenced through text identifiers/traces.

### PARTIAL
The following are currently text fields rather than independently structured objects:
- Claim ID
- Evidence Mapping
- Transformation Trace
- Research Object ID
- Branch ID
- Revision Type
- Relation fields

Therefore the schema can represent traceability, but queryable object-level graph semantics are not guaranteed.

## 4. D9 schema conflict

Current Notion D9 상태 options are:
- HOLD
- CANDIDATE
- PROMOTED

This conflicts with T19's proposed semantic resolution:
- NOT_APPLICABLE
- CANDIDATE
- PROMOTED

The current database therefore still contains stale HOLD terminology and has no NOT_APPLICABLE option.

This is an implementation-schema issue, not a reason to reinterpret HOLD as canonical.

For non-D9 notes, D9 applicability is currently represented operationally outside the select vocabulary rather than cleanly in the schema.

## 5. Epistemic state expressiveness

The current 인식론적 상태 select can represent note-level states but has no dedicated Claim-level property.

This is acceptable only if Claim-level state is stored in the Claim layer/body/trace with explicit Claim IDs. It must not be interpreted as automatically representing every Claim's state.

## 6. Migration implication

Before live population at scale, two implementation choices must be resolved:

A. D9 status representation:
- either add NOT_APPLICABLE and retain HOLD as explicitly non-canonical legacy/operational value,
- or create a separate D9 applicability property and redefine D9 status strictly as promotion state.

B. Claim-level representation:
- retain collapsed schema with explicit Claim ID + state encoding,
- or introduce a dedicated Claim data source/relation if queryability becomes necessary.

No schema mutation was performed.

## 7. Decision

T24 = CONDITIONAL PASS.

The current Notion schema is expressive enough for a collapsed v0.4 representation, but it is not yet a clean executable representation of the full logical graph.

Primary blockers for implementation closure:
1. stale D9 HOLD option
2. Claim-level epistemic state not independently queryable
3. Evidence/Transformation/Relation objects represented as text rather than structured relations
4. T16 Q2-Q5 query coverage remains unavailable

Next: T25 — choose the minimal schema correction path and test whether collapsed text representation is sufficient for the intended query workload before introducing separate data sources.
