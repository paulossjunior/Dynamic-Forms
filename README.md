# Sistema de Formulários Dinâmicos

Sistema completo de formulários dinâmicos com backend Python (FastAPI) e frontend Vue 3, permitindo criação de campos personalizados em tempo de execução sem necessidade de migrações de banco de dados.

## 🚀 Características

- **Campos Dinâmicos**: Crie novos campos personalizados sem alterar o schema do banco de dados
- **Templates de Formulários**: Monte formulários reutilizáveis combinando campos existentes
- **Validação Configurável**: Defina regras de validação (obrigatório, comprimento mín/máx, valor mín/máx) por formulário
- **Interface Moderna**: UI construída com Vue 3, Tailwind CSS e Headless UI
- **API RESTful**: Backend FastAPI com documentação automática (Swagger)
- **Armazenamento Eficiente**: Dados dinâmicos armazenados como JSON no SQLite

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd formularioi_dinamico
```

### 2. Instale as dependências

Use o Makefile para instalar todas as dependências automaticamente:

```bash
make install
```

Ou instale manualmente:

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## 🚀 Executando a Aplicação

### Modo Desenvolvimento (Recomendado)

Execute backend e frontend simultaneamente:

```bash
make dev
```

Isso iniciará:
- Backend: http://localhost:8001
- Frontend: http://localhost:5173
- API Docs: http://localhost:8001/docs

### Executar Separadamente

**Backend:**
```bash
make backend
```

**Frontend:**
```bash
make frontend
```

## 📖 Guia de Uso

### 1. Criar Campos Personalizados

1. Acesse `/admin` (Admin Fields)
2. Preencha o formulário:
   - **Label**: Nome amigável do campo (ex: "Departamento")
   - **Key Name**: Identificador único (ex: "department")
   - **Field Type**: Selecione o tipo (text, number, select, multiselect, checkbox, radio)
   - **Options**: Para campos select/multiselect, adicione opções separadas por vírgula
   - **Validation Rules**: Configure regras de validação (opcional)
3. Clique em **Create Field**

**Tipos de Campo Suportados:**
- `text`: Campo de texto simples
- `number`: Campo numérico
- `select`: Lista suspensa (seleção única)
- `multiselect`: Lista suspensa (seleção múltipla)
- `checkbox`: Caixa de seleção
- `radio`: Botões de opção

### 2. Criar Templates de Formulário

1. Acesse `/builder` (Form Builder)
2. Defina:
   - **Form Name**: Nome do template (ex: "Cadastro de Desenvolvedor")
   - **Description**: Descrição opcional
3. Selecione os campos desejados da lista
4. Para cada campo selecionado, marque **"Required?"** se for obrigatório neste formulário
5. Clique em **Create Template**

> **Nota**: A configuração "Required" é específica do formulário. Um mesmo campo pode ser obrigatório em um formulário e opcional em outro.

### 3. Cadastrar Pessoas

1. Acesse `/create` (New Person)
2. Selecione um **Form Template** (opcional)
3. Preencha os campos fixos:
   - Name
   - Email
4. Preencha os campos dinâmicos do template selecionado
5. Clique em **Save Person**

**Validação em Tempo Real:**
- Campos obrigatórios são marcados com asterisco vermelho (*)
- Mensagens de erro aparecem abaixo dos campos inválidos
- O formulário não será enviado até que todas as validações sejam atendidas

### 4. Visualizar Dados

Acesse `/` (People List) para ver todos os registros cadastrados com seus dados fixos e personalizados.

## 🏗️ Arquitetura

### Backend (FastAPI + SQLite)

**Estrutura de Diretórios:**
```
backend/
├── main.py              # Aplicação FastAPI principal
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── database.py          # Configuração do banco de dados
└── sql_app.db          # Banco de dados SQLite
```

**Modelos de Dados:**

1. **CustomFieldDefinition**: Metadados dos campos personalizados
   - `entity_type`: Tipo de entidade (ex: "person")
   - `key_name`: Identificador único do campo
   - `label`: Rótulo exibido
   - `field_type`: Tipo do campo (text, number, select, etc.)
   - `options`: Opções para campos select (JSON)
   - `validation_rules`: Regras de validação (JSON)

2. **FormDefinition**: Templates de formulários
   - `name`: Nome do template
   - `description`: Descrição

3. **FormFields**: Associação entre formulários e campos
   - `form_id`: ID do formulário
   - `field_id`: ID do campo
   - `is_required`: Se o campo é obrigatório neste formulário
   - `order`: Ordem de exibição

4. **Person**: Entidade principal
   - `name`: Nome (campo fixo)
   - `email`: Email (campo fixo)
   - `custom_data`: Dados dinâmicos (JSON armazenado como TEXT)

**Abordagem Híbrida EAV-JSONB:**
- Metadados dos campos armazenados em tabelas relacionais (EAV)
- Valores dos campos armazenados como JSON na coluna `custom_data`
- Melhor performance para consultas e flexibilidade para dados dinâmicos

### Frontend (Vue 3 + Vite)

**Estrutura de Diretórios:**
```
frontend/
├── src/
│   ├── components/
│   │   └── DynamicForm/
│   │       └── FormRenderer.vue    # Renderizador dinâmico de campos
│   ├── views/
│   │   ├── AdminFields.vue         # Gerenciamento de campos
│   │   ├── FormBuilder.vue         # Criação de templates
│   │   ├── PersonCreate.vue        # Cadastro de pessoas
│   │   └── PersonList.vue          # Listagem de pessoas
│   ├── router.js                   # Configuração de rotas
│   ├── main.js                     # Ponto de entrada
│   └── App.vue                     # Layout principal
├── package.json
└── vite.config.js
```

**Tecnologias:**
- **Vue 3**: Framework reativo
- **Vite**: Build tool e dev server
- **Vue Router**: Roteamento
- **Axios**: Cliente HTTP
- **Tailwind CSS v4**: Estilização
- **Headless UI**: Componentes acessíveis
- **Heroicons**: Ícones

**Componente Principal:**

`FormRenderer.vue` renderiza dinamicamente campos baseado nas definições do backend:
- Suporta todos os tipos de campo
- Validação em tempo real
- Indicadores visuais de campos obrigatórios
- Mensagens de erro contextuais

## 🔌 API Reference

### Campos Personalizados

**Criar Campo**
```http
POST /api/fields/
Content-Type: application/json

{
  "entity_type": "person",
  "key_name": "department",
  "label": "Departamento",
  "field_type": "select",
  "options": ["Engineering", "HR", "Sales"],
  "validation_rules": {},
  "is_active": true
}
```

**Listar Campos**
```http
GET /api/fields/{entity_type}
```

### Formulários

**Criar Template**
```http
POST /api/forms/
Content-Type: application/json

{
  "name": "Developer Profile",
  "description": "Form for developer onboarding",
  "fields": [
    {
      "field_id": 1,
      "is_required": true
    },
    {
      "field_id": 2,
      "is_required": false
    }
  ]
}
```

**Listar Templates**
```http
GET /api/forms/
```

**Obter Template Específico**
```http
GET /api/forms/{form_id}
```

### Pessoas

**Criar Pessoa**
```http
POST /api/people/
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@example.com",
  "custom_data": {
    "department": "Engineering",
    "bio": "Senior developer with 10 years of experience"
  }
}
```

**Listar Pessoas**
```http
GET /api/people/
```

## 🧪 Validação

O sistema suporta as seguintes regras de validação:

- **required**: Campo obrigatório (configurado por formulário)
- **min**: Valor mínimo (para campos numéricos)
- **max**: Valor máximo (para campos numéricos)
- **minLength**: Comprimento mínimo (para campos de texto)
- **maxLength**: Comprimento máximo (para campos de texto)

**Exemplo de Regras:**
```json
{
  "required": true,
  "minLength": 10,
  "maxLength": 500
}
```

## 🛠️ Comandos Úteis (Makefile)

```bash
make install    # Instala todas as dependências
make dev        # Executa backend e frontend
make backend    # Executa apenas o backend
make frontend   # Executa apenas o frontend
make clean      # Remove arquivos temporários e cache
```

## 📁 Estrutura de Dados

### Exemplo de Registro Completo

```json
{
  "id": 1,
  "name": "Maria Santos",
  "email": "maria@example.com",
  "custom_data": {
    "department": "Engineering",
    "remote": "Yes",
    "bio": "Full-stack developer specializing in Vue and Python",
    "skills": ["Vue", "Python", "FastAPI", "SQLite"]
  }
}
```

## 🔒 Segurança

- Validação de dados no backend via Pydantic
- Sanitização de inputs
- CORS configurado (ajustar para produção)
- Validação de tipos de campo

## 🚧 Desenvolvimento

### Adicionar Novo Tipo de Campo

1. **Backend** (`models.py`): O tipo já é flexível via string
2. **Frontend** (`FormRenderer.vue`): Adicione novo case no switch do tipo de campo

### Estender Validações

1. **Backend** (`schemas.py`): Adicione novos campos ao schema de validação
2. **Frontend** (`PersonCreate.vue`): Implemente lógica de validação no método `validate()`

## 📝 Licença

Este projeto é fornecido como está, para fins educacionais e de demonstração.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através do repositório.
