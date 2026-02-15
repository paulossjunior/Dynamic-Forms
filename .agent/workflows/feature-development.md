---
description: Workflow completo para desenvolvimento de features com EPIC, US, Tasks, TDD e padrões de commit
---

# Workflow: Feature Development com EPIC, User Stories e TDD

Este workflow define o processo completo para criar novas features seguindo as melhores práticas de desenvolvimento ágil, TDD e arquitetura hexagonal.

## 📋 Fase 1: Planejamento e Documentação

### 1.1 Criar EPIC no Backlog

Crie ou atualize o arquivo `docs/backlog.md` com a nova EPIC:

```markdown
## EPIC-XXX: [Nome da EPIC]

**Descrição**: [Descrição de alto nível da funcionalidade]

**Valor de Negócio**: [Por que esta feature é importante]

**Critérios de Aceitação da EPIC**:
- [ ] Critério 1
- [ ] Critério 2

**User Stories**:
- [ ] US-XXX.1: [Título da User Story 1]
- [ ] US-XXX.2: [Título da User Story 2]
```

### 1.2 Detalhar User Stories

Para cada User Story, documente:

```markdown
### US-XXX.1: [Título da User Story]

**Como** [tipo de usuário]  
**Quero** [ação/funcionalidade]  
**Para** [benefício/objetivo]

**Critérios de Aceitação**:
- [ ] Dado [contexto], quando [ação], então [resultado esperado]
- [ ] Dado [contexto], quando [ação], então [resultado esperado]

**Definição de Pronto (DoD)**:
- [ ] Código implementado seguindo arquitetura hexagonal
- [ ] Testes unitários escritos (TDD)
- [ ] Testes de integração passando
- [ ] Documentação atualizada
- [ ] Code review aprovado
- [ ] Sem débitos técnicos

**Tasks**:
- [ ] TASK-XXX.1.1: [Descrição da task]
- [ ] TASK-XXX.1.2: [Descrição da task]
```

### 1.3 Quebrar em Tasks Técnicas

Detalhe cada task seguindo a arquitetura hexagonal:

```markdown
#### TASK-XXX.1.1: Implementar Domain Layer

**Camada**: Domain  
**Estimativa**: [XP ou horas]

**Checklist**:
- [ ] Criar entidades do domínio
- [ ] Criar value objects
- [ ] Definir regras de negócio
- [ ] Escrever testes unitários do domínio

#### TASK-XXX.1.2: Implementar Application Layer

**Camada**: Application  
**Estimativa**: [XP ou horas]

**Checklist**:
- [ ] Criar use cases
- [ ] Definir DTOs
- [ ] Definir ports (interfaces)
- [ ] Escrever testes de use cases

#### TASK-XXX.1.3: Implementar Infrastructure Layer

**Camada**: Infrastructure  
**Estimativa**: [XP ou horas]

**Checklist**:
- [ ] Implementar adapters (repositories, controllers)
- [ ] Configurar banco de dados
- [ ] Integrar com APIs externas (se necessário)
- [ ] Escrever testes de integração
```

## 🔴 Fase 2: Test-Driven Development (TDD)

### 2.1 Red Phase - Escrever Testes que Falham

**Para Backend (Python + pytest)**:

```bash
# Criar arquivo de teste
touch backend/tests/test_[feature_name].py
```

```python
# backend/tests/test_[feature_name].py
import pytest
from domain.entities import [Entity]
from application.use_cases import [UseCase]

class Test[Feature]:
    def test_should_[expected_behavior](self):
        # Arrange
        [setup]
        
        # Act
        result = [action]
        
        # Assert
        assert result == [expected]
```

**Para Frontend (Vue + Vitest)**:

```bash
# Criar arquivo de teste
touch frontend/tests/[component].spec.js
```

```javascript
// frontend/tests/[component].spec.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import [Component] from '@/components/[Component].vue'

describe('[Component]', () => {
  it('should [expected behavior]', () => {
    // Arrange
    const wrapper = mount([Component])
    
    // Act
    [action]
    
    // Assert
    expect(wrapper.text()).toContain([expected])
  })
})
```

### 2.2 Green Phase - Implementar Código Mínimo

Implemente apenas o código necessário para fazer os testes passarem:

1. **Domain Layer** (entities, value objects, domain services)
2. **Application Layer** (use cases, DTOs, ports)
3. **Infrastructure Layer** (adapters, repositories, controllers)

### 2.3 Refactor Phase - Melhorar o Código

- Remover duplicação
- Aplicar princípios SOLID
- Melhorar nomenclatura
- Adicionar documentação

## 🔄 Fase 3: Implementação com Commits Semânticos

### 3.1 Padrão de Commits (Conventional Commits)

Use o formato: `<type>(<scope>): <subject>`

**Types**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `test`: Adicionar ou modificar testes
- `refactor`: Refatoração de código
- `style`: Formatação, ponto e vírgula, etc
- `perf`: Melhoria de performance
- `chore`: Tarefas de build, configuração

**Scopes** (camadas hexagonais):
- `domain`: Camada de domínio
- `application`: Camada de aplicação
- `infrastructure`: Camada de infraestrutura
- `ui`: Interface do usuário

**Exemplos**:
```bash
git commit -m "test(domain): add unit tests for User entity"
git commit -m "feat(domain): implement User entity with validation"
git commit -m "feat(application): create CreateUser use case"
git commit -m "feat(infrastructure): implement UserRepository adapter"
git commit -m "feat(ui): add user registration form component"
git commit -m "docs(backlog): update US-001 with acceptance criteria"
```

### 3.2 Fluxo de Commits por Task

Para cada task:

```bash
# 1. Criar branch da feature
git checkout -b feature/EPIC-XXX-user-story-description

# 2. TDD Red - Escrever testes
git add tests/
git commit -m "test(domain): add failing tests for [feature]"

# 3. TDD Green - Implementar código
git add src/domain/
git commit -m "feat(domain): implement [entity/value-object]"

git add src/application/
git commit -m "feat(application): implement [use-case]"

git add src/infrastructure/
git commit -m "feat(infrastructure): implement [adapter/repository]"

# 4. TDD Refactor - Melhorar código
git add .
git commit -m "refactor(domain): improve [entity] validation logic"

# 5. Documentação
git add docs/
git commit -m "docs(backlog): mark TASK-XXX.1.1 as complete"
```

## ✅ Fase 4: Verificação e Entrega

### 4.1 Checklist de Qualidade

Antes de abrir Pull Request:

```bash
# Backend
cd backend
pytest tests/ --cov=src --cov-report=term-missing
pylint src/
black src/ --check

# Frontend
cd frontend
npm run test
npm run lint
npm run build
```

### 4.2 Pull Request

Criar PR com template:

```markdown
## EPIC-XXX: [Nome da EPIC]

### User Story
US-XXX.1: [Título da User Story]

### Descrição
[Descrição das mudanças]

### Tasks Implementadas
- [x] TASK-XXX.1.1: [Descrição]
- [x] TASK-XXX.1.2: [Descrição]

### Testes
- [x] Testes unitários (cobertura: XX%)
- [x] Testes de integração
- [x] Testes E2E (se aplicável)

### Checklist
- [x] Código segue arquitetura hexagonal
- [x] TDD aplicado (Red-Green-Refactor)
- [x] Commits seguem padrão semântico
- [x] Documentação atualizada
- [x] Sem débitos técnicos
```

### 4.3 Atualizar Backlog

Após merge:

```markdown
## EPIC-XXX: [Nome da EPIC]
- [x] US-XXX.1: [Título] - ✅ Concluída em [data]
  - [x] TASK-XXX.1.1: [Descrição]
  - [x] TASK-XXX.1.2: [Descrição]
```

## 📊 Estrutura de Arquivos

```
project/
├── docs/
│   ├── backlog.md              # EPICs, User Stories, Tasks
│   ├── architecture.md         # Diagrama hexagonal
│   └── adr/                    # Architecture Decision Records
├── backend/
│   ├── src/
│   │   ├── domain/             # Entities, Value Objects, Domain Services
│   │   ├── application/        # Use Cases, DTOs, Ports
│   │   └── infrastructure/     # Adapters, Repositories, Controllers
│   └── tests/
│       ├── unit/               # Testes de domínio e aplicação
│       └── integration/        # Testes de infraestrutura
└── frontend/
    ├── src/
    │   ├── domain/             # Business logic (se aplicável)
    │   ├── application/        # Composables, stores
    │   ├── infrastructure/     # API clients, adapters
    │   └── ui/                 # Components, views
    └── tests/
        ├── unit/
        └── e2e/
```

## 🎯 Exemplo Completo

### EPIC-001: Sistema de Autenticação

**User Story**: US-001.1: Login de usuário

**Tasks**:
1. TASK-001.1.1: Implementar entidade User (Domain)
2. TASK-001.1.2: Criar use case AuthenticateUser (Application)
3. TASK-001.1.3: Implementar UserRepository (Infrastructure)
4. TASK-001.1.4: Criar LoginForm component (UI)

**Commits**:
```bash
git commit -m "test(domain): add User entity validation tests"
git commit -m "feat(domain): implement User entity with email and password"
git commit -m "test(application): add AuthenticateUser use case tests"
git commit -m "feat(application): implement AuthenticateUser use case"
git commit -m "test(infrastructure): add UserRepository integration tests"
git commit -m "feat(infrastructure): implement UserRepository with SQLAlchemy"
git commit -m "feat(ui): add LoginForm component with validation"
git commit -m "docs(backlog): mark US-001.1 as complete"
```

## 📚 Referências

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [User Story Mapping](https://www.jpattonassociates.com/user-story-mapping/)
