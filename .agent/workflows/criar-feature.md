---
description: Criar nova feature seguindo EPIC → US → Tasks com TDD
---

# Workflow: Criar Feature

Este workflow guia a criação de uma nova feature do início ao fim.

## Passo 1: Planejar no Backlog

Abra `docs/backlog.md` e adicione:

```markdown
### EPIC-XXX: [Nome da Feature]

**Como** [usuário]
**Quero** [funcionalidade]
**Para** [benefício]

**User Stories**:
- [ ] US-XXX.1: [Descrição]

**Tasks**:
- [ ] TASK-XXX.1.1: Domain Layer
- [ ] TASK-XXX.1.2: Application Layer  
- [ ] TASK-XXX.1.3: Infrastructure Layer
- [ ] TASK-XXX.1.4: UI Layer
```

## Passo 2: Criar Branch

```bash
git checkout -b feature/EPIC-XXX-nome-descritivo
```

## Passo 3: TDD - Red (Testes que Falham)

**Backend:**
```bash
touch backend/tests/test_feature.py
```

**Frontend:**
```bash
touch frontend/tests/Feature.spec.js
```

## Passo 4: TDD - Green (Implementar)

Implemente seguindo as camadas:
1. Domain (entidades, regras de negócio)
2. Application (use cases, DTOs)
3. Infrastructure (repositories, APIs)
4. UI (componentes Vue)

## Passo 5: TDD - Refactor

Melhore o código:
- Remover duplicação
- Aplicar SOLID
- Adicionar documentação

## Passo 6: Commit Semântico

```bash
git commit -m "test(domain): add tests for Feature"
git commit -m "feat(domain): implement Feature entity"
git commit -m "feat(application): create UseCase"
git commit -m "feat(infrastructure): implement Repository"
git commit -m "feat(ui): add Feature component"
```

## Passo 7: Push e PR

```bash
git push origin feature/EPIC-XXX-nome-descritivo
```

Criar PR com:
- Descrição da feature
- Tasks completadas
- Testes executados
- Screenshots (se UI)

## Passo 8: Atualizar Backlog

Marcar tasks como concluídas em `docs/backlog.md`
