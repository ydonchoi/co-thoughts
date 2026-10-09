# co-thoughts

Human-AI Co-Thinking Protocol — current baseline v2.0+++

**Languages:** [English](README.en.md) · [Documentation language guide](docs/LANGUAGE.md)

## 시작점과 배경

이 저장소는 자전적 기록에서 출발했습니다. 누적된 대화 기록에 나타나는 패턴을 살펴보고, 의사소통 과정에서 드러나는 저의 사고 과정을 구조화해 구현하려는 시도에서 시작되었습니다. 개인의 사고와 대화 패턴을 관찰하고 정리하는 작업은 점차 인간–AI 공동사고를 위한 프로토콜과 실행 규칙, 연구노트 구조 및 검증 체계를 설계하는 방향으로 확장되었습니다.

## License

This repository is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

In brief, you may copy, share, adapt, and build upon the repository's original material for **non-commercial purposes**, provided that you give appropriate attribution, link to the license, and indicate changes.

**Commercial use is not permitted under this license without separate permission from the copyright holder.**

- Full license: https://creativecommons.org/licenses/by-nc/4.0/legalcode
- License deed: https://creativecommons.org/licenses/by-nc/4.0/
- SPDX: CC-BY-NC-4.0
- See LICENSE for the repository's license notice.

Unless a file or directory explicitly states otherwise, the license applies to the original material in this repository. Third-party materials and dependencies remain subject to their respective licenses.

## Layout

- src/co_thoughts/ — runtime implementation
- protocol/ — active rules and contracts
- docs/ — architecture, contracts, research-note and testing documentation
- tests/ — executable regression tests
- archive/ — historical material
- retire/ — temporary removal-review area

## Maintenance rules

Active code belongs in src/co_thoughts/.
Canonical operational rules belong in protocol/.
Explanatory material belongs in docs/.
Executable tests belong in tests/.
Superseded material belongs in archive/.
Removal candidates belong in retire/ only temporarily.

Major directories contain local README files describing their role.

This repository is public. A folder name does not create an access-control boundary. Material that must not be public must be removed from this repository or relocated to an access-controlled repository.
