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

### EPIC-004: Sistema de Seções em Formulários
**Status**: 🔄 Em Planejamento  
**Descrição**: Permitir organização de formulários em seções lógicas com nome, descrição e conjunto de campos agrupados

**Valor de Negócio**: Melhorar UX de formulários complexos através de agrupamento lógico de campos, facilitando compreensão e preenchimento

**Critérios de Aceitação da EPIC**:
- [ ] Admin pode criar seções com nome e descrição
- [ ] Admin pode associar campos a seções
- [ ] Admin pode reordenar seções
- [ ] Usuário vê formulários organizados em seções visuais
- [ ] Seções sem campos não aparecem no formulário

**User Stories**:
- [ ] US-004.1: Criar e Gerenciar Seções (Admin)
- [ ] US-004.2: Visualizar Formulário com Seções (Usuário)
- [ ] US-004.3: Criar Seções Inline no Form Builder (Admin)

**Tasks Técnicas**:
- [ ] TASK-004.1.1: Implementar Domain Layer - Section Entity
- [ ] TASK-004.1.2: Implementar Application Layer - Section Use Cases
- [ ] TASK-004.1.3: Implementar Infrastructure Layer - Database & Repository
- [ ] TASK-004.1.4: Implementar UI Layer - Section Management
- [ ] TASK-004.2.1: Implementar UI - Form Renderer com Seções
- [ ] TASK-004.3.1: Backend - Suporte a criação aninhada de Seções
- [ ] TASK-004.3.2: Frontend - UI de criação de Seções Inline

---

## 📝 User Stories Detalhadas

### US-004.3: Criar Seções Inline no Form Builder

**Como** administrador criando um formulário
**Quero** poder definir novas seções diretamente na tela de criação
**Para** não precisar salvar o formulário vazio, sair, criar seções e voltar

**Critérios de Aceitação**:
- [ ] Dado que estou no Form Builder, quando clico em "Adicionar Seção", então posso digitar o nome da seção
- [ ] Dado que criei uma seção inline, quando seleciono um campo, então posso atribuí-lo a essa nova seção
- [ ] Dado que salvo o formulário, quando o processo finaliza, então o formulário, as seções e as associações são persistidas corretamente


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

---

### EPIC-002: Melhorias de UX/UI
**Status**: 🔄 Em Progresso

**User Stories**:
- [ ] US-002.4: Melhorar responsividade e Acessibilidade (Mobile First & WCAG)

**Tasks Técnicas**:
- [ ] TASK-002.4.1: Implementar Menu Mobile em `App.vue` (Hamburger Menu)
- [ ] TASK-002.4.2: Transformar `PersonList` em Cards para Mobile
- [ ] TASK-002.4.3: Adicionar atributos ARIA e `lang="pt-BR"`
- [ ] TASK-002.4.4: Verificar contraste e tamanhos de fonte

### Baixa Prioridade
### EPIC-005: Tratamento de Erros e Validação
**Status**: 🔄 Em Progresso
**Descrição**: Melhorar o feedback de erros para o usuário, substituindo alerts por mensagens na interface.

**User Stories**:
- [ ] US-005.1: Exibir erros de validação e API na tela (Person Create)

### US-005.1: Exibir erros de validação e API na tela (Person Create)

**Como** usuário cadastrando uma pessoa
**Quero** ver mensagens de erro claras na tela (não em popups)
**Para** corrigir os dados sem interromper meu fluxo

**Critérios de Aceitação**:
- [ ] Dado que tento salvar com email duplicado, quando a API retorna 400, então vejo uma mensagem de erro vermelha no topo do formulário
- [ ] Dado que existem erros de validação, quando clico em salvar, então os erros aparecem próximos aos campos ou no topo
- [ ] Não devem ser usados `window.alert()`

**Tasks**:
- [ ] TASK-005.1.1: Criar componente de Alerta/Erro (UI)
- [ ] TASK-005.1.2: Refatorar PersonCreate.vue para usar estado de erro local
- [ ] TASK-005.1.3: Criar teste de componente para verificar exibição de erro


---

## 📊 Métricas

**Sprint Atual**: Sprint 2 - Form Sections  
**Velocity**: N/A  
**Burndown**: N/A

**Concluído**:
- EPIC-001: Sistema de Formulários Dinâmicos (100%)

**Em Progresso**:
- EPIC-004: Sistema de Seções em Formulários (0% - Planejamento)

**Planejado**:
- EPIC-002: Melhorias de UX/UI
- EPIC-003: Arquitetura Hexagonal

