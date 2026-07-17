# Documentation Reorganization Plan

## Proposed structure

```text
docs/
  README.md
  architecture/
    system_architecture.md
    architecture_principles.md
    adr_index.md
  capabilities/
    capabilities_overview.md
    capability_history.md
  engineering/
    development_methodology.md
    testing_strategy.md
    git_workflow.md
  ai_intelligence/
    llm_architecture.md
    rag_architecture.md
    agent_system.md
    self_improvement_layer.md
  project_management/
    roadmap.md
    backlog.md
    releases.md
  decisions/
    ADRs organized by topic
  audit/
    documentation_audit_report.md
    reorganization_plan.md
```

## Documents to merge

- [docs/archive/capabilities.md](../archive/capabilities.md) into [capabilities/capabilities_overview.md](../capabilities/capabilities_overview.md)
- [docs/architecture/architecture.md](../architecture/architecture.md) into [architecture/system_architecture.md](../architecture/system_architecture.md)
- [docs/architecture/roadmap.md](../architecture/roadmap.md) into [project_management/roadmap.md](../project_management/roadmap.md)
- [docs/current_status.md](../current_status.md) and [docs/development_log.md](../development_log.md) into a lighter set of living references plus historical links

## Documents to keep

- [README.md](../../README.md)
- [docs/glossary.md](../glossary.md)
- [docs/environment.md](../environment.md)
- [docs/api.md](../api.md)
- [docs/archive/PROJECT_CHECKPOINT.md](../archive/PROJECT_CHECKPOINT.md)
- [docs/adr](../adr)

## Documents candidates for removal only after approval

| File | Reason | Replacement | Content preserved in |
| --- | --- | --- | --- |
| docs/architecture/architecture.md | Overlaps with system_architecture.md | system_architecture.md | architecture/system_architecture.md |
| docs/archive/capabilities.md | Duplicates capability overview | capabilities/capabilities_overview.md | capabilities/capabilities_overview.md |
| docs/architecture/roadmap.md | Project management content should live in project_management | project_management/roadmap.md | project_management/roadmap.md |
| docs/architecture/agent_architecture.md | Empty or too sparse to remain as standalone doc | ai_intelligence/agent_system.md | ai_intelligence/agent_system.md |

## Safe migration plan

1. Create the consolidated structure and navigation hub.
2. Move summary content into the new canonical documents.
3. Keep all original files intact until the new structure is reviewed.
4. Update internal links to point to the new canonical documents.
5. Only archive or remove documents after explicit approval.
