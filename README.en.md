# co-thoughts

**Human–AI Co-Thinking Protocol — current baseline v2.0+++**

- [한국어 README](README.md)
- [Documentation language guide](docs/LANGUAGE.md)

## Origin and Background

This repository began as an autobiographical record. It started with an effort to examine patterns in my accumulated conversation history and to structure and implement the thinking processes that emerge during communication. Over time, observing and organizing these personal thinking and dialogue patterns expanded into the design of protocols and execution rules for human–AI co-thinking, along with research-note structures and verification practices.

## License

This repository is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

You may copy, share, adapt, and build upon the repository's original material for **non-commercial purposes**, provided that you give appropriate attribution, link to the license, and indicate changes. **Commercial use is not permitted without separate permission from the copyright holder.**

- [Full license](https://creativecommons.org/licenses/by-nc/4.0/legalcode)
- [License deed](https://creativecommons.org/licenses/by-nc/4.0/)
- SPDX: CC-BY-NC-4.0
- See [LICENSE](LICENSE) for the repository's license notice.

Unless a file or directory explicitly states otherwise, the license applies to the original material in this repository. Third-party materials and dependencies remain subject to their respective licenses.

## Repository layout

- `src/co_thoughts/` — runtime implementation
- `protocol/` — active rules and contracts
- `docs/` — architecture, contracts, research-note, and testing documentation
- `tests/` — executable regression tests
- `archive/` — historical material
- `retire/` — temporary removal-review area

## Maintenance rules

- Active code belongs in `src/co_thoughts/`.
- Canonical operational rules belong in `protocol/`.
- Explanatory material belongs in `docs/`.
- Executable tests belong in `tests/`.
- Superseded material belongs in `archive/`.
- Removal candidates belong in `retire/` only temporarily.

Major directories contain local README files describing their role.

This repository is public. A folder name does not create an access-control boundary. Material that must not be public must be removed from this repository or relocated to an access-controlled repository.
