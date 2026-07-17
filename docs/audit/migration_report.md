# Migration Report

## Objective

Track all documentation moves and consolidations during the reorganization process without deleting any files.

## Migration plan

| Original file | Destination file | Sections migrated | Information preserved |
| --- | --- | --- | --- |
| docs/capabilities.md | docs/capabilities/capabilities_overview.md | Capability model, current capabilities, planned capabilities | Capability definitions, status, architecture context |
| docs/architecture/architecture.md | docs/architecture/system_architecture.md | Architecture overview, evolution, component layers | Architectural intent, layered model, component responsibilities |
| docs/architecture/roadmap.md | docs/project_management/roadmap.md | Evolution phases, milestones, strategic direction | Roadmap and platform maturity narrative |
| docs/architecture/architecture-principles.md | docs/architecture/architecture_principles.md | Core principles and design guidance | Architectural principles and governance policy |
| docs/Version/VERSION_1.8.md | docs/project_management/releases.md | Version milestone details | Version history and milestone context |
| docs/Version/VERSION_0_6.md | docs/project_management/releases.md | Early roadmap and evolution context | Historical progression and early milestones |
| docs/README.md | docs/README.md | Documentation hub entry point | Documentation navigation and governance |

## Preservation rules

- No file is deleted.
- Version history remains available in its original location and in the consolidated release references.
- ADRs remain preserved and indexed centrally.
- Historical milestones from V1.7 through V1.17 remain documented and accessible.
