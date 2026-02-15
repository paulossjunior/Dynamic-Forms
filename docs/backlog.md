# Backlog - Dynamic Forms System

## 🎯 EPICs em Andamento

### EPIC-001: Sistema de Formulários Dinâmicos ✅
**Status**: Concluído  
**Descrição**: Implementar sistema completo de formulários dinâmicos com campos personalizáveis

**Valor de Negócio**: Permitir criação de formulários sem necessidade de alteração de código

**User Stories Concluídas**:
- [x] US-001.1: Criar campos dinâmicos (Admin)
- [x] US-001.2: Criar templates de formulários
- [x] US-001.3: Preencher formulários com validação
- [x] US-001.4: Visualizar dados em lista
- [x] US-001.5: Dashboard com analytics

---

### EPIC-002: Melhorias de UX/UI
**Status**: Planejado  
**Descrição**: Melhorar experiência do usuário com componentes Nuxt UI e design aprimorado

**Valor de Negócio**: Aumentar satisfação do usuário e reduzir erros de preenchimento

**User Stories**:
- [ ] US-002.1: Redesign da tabela People List com badges
- [ ] US-002.2: Adicionar feedback visual para ações
- [ ] US-002.3: Implementar modo escuro
- [ ] US-002.4: Melhorar responsividade mobile

---

### EPIC-003: Arquitetura Hexagonal
**Status**: Planejado  
**Descrição**: Refatorar aplicação para seguir padrões de arquitetura hexagonal

**Valor de Negócio**: Melhorar manutenibilidade, testabilidade e escalabilidade do sistema

**User Stories**:
- [ ] US-003.1: Separar camadas Domain, Application e Infrastructure (Backend)
- [ ] US-003.2: Implementar Ports e Adapters
- [ ] US-003.3: Adicionar testes unitários com TDD
- [ ] US-003.4: Documentar arquitetura

---

## 📝 User Stories Detalhadas

### US-002.1: Redesign da tabela People List com badges

**Como** administrador do sistema  
**Quero** visualizar os dados dinâmicos como badges coloridos  
**Para** identificar rapidamente as informações de cada pessoa

**Critérios de Aceitação**:
- [ ] Dado que estou na página People List, quando visualizo a tabela, então vejo badges coloridos para cada campo dinâmico
- [ ] Dado que um campo tem múltiplos valores, quando visualizo, então vejo múltiplos badges em verde
- [ ] Dado que um campo tem valor único, quando visualizo, então vejo um badge azul
- [ ] Dado que uma pessoa não tem dados dinâmicos, quando visualizo, então vejo "No custom data" em cinza

**Tasks**:
- [ ] TASK-002.1.1: Criar componente Badge reutilizável
- [ ] TASK-002.1.2: Atualizar PersonList.vue para usar badges
- [ ] TASK-002.1.3: Adicionar testes de componente
- [ ] TASK-002.1.4: Atualizar documentação

---

### US-003.1: Separar camadas Domain, Application e Infrastructure

**Como** desenvolvedor  
**Quero** ter o código organizado em camadas hexagonais  
**Para** facilitar manutenção e testes

**Critérios de Aceitação**:
- [ ] Dado que estou no backend, quando navego na estrutura, então vejo pastas domain/, application/ e infrastructure/
- [ ] Dado que estou na camada domain, quando verifico dependências, então não vejo imports de infrastructure
- [ ] Dado que estou testando domain, quando executo testes, então não preciso de banco de dados

**Tasks**:
- [ ] TASK-003.1.1: Criar estrutura de pastas hexagonal
- [ ] TASK-003.1.2: Mover entidades para domain/
- [ ] TASK-003.1.3: Criar use cases em application/
- [ ] TASK-003.1.4: Implementar repositories como adapters
- [ ] TASK-003.1.5: Definir ports (interfaces)
- [ ] TASK-003.1.6: Atualizar testes

---

## 🐛 Bugs e Melhorias

### Alta Prioridade
- [x] BUG-001: Erro ao salvar pessoa com email duplicado - ✅ Resolvido
  - Solução: Mensagem de erro em português implementada

### Média Prioridade
- [ ] IMPROVE-001: Adicionar paginação na lista de pessoas
- [ ] IMPROVE-002: Implementar busca/filtro na People List
- [ ] IMPROVE-003: Adicionar exportação de dados (CSV/Excel)

### Baixa Prioridade
- [ ] IMPROVE-004: Adicionar campo de busca no Dashboard
- [ ] IMPROVE-005: Melhorar performance de queries com índices

---

## 📊 Métricas

**Sprint Atual**: N/A  
**Velocity**: N/A  
**Burndown**: N/A

**Concluído**:
- EPIC-001: Sistema de Formulários Dinâmicos (100%)

**Em Progresso**:
- Nenhum

**Planejado**:
- EPIC-002: Melhorias de UX/UI
- EPIC-003: Arquitetura Hexagonal
