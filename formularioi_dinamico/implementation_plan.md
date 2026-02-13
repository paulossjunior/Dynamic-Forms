# Arquitetura para Formulários Dinâmicos com Banco Relacional

## Visão Geral do Problema

Você possui um banco de dados relacional com entidades fixas (Pessoa, Endereço) e deseja permitir que usuários criem campos adicionais dinamicamente através de um formulário, mantendo a integridade relacional.

## Proposta de Arquitetura: Padrão EAV Híbrido

Recomendo uma abordagem **híbrida** que combina:
1. **Schema fixo** para campos obrigatórios/comuns (Pessoa, Endereço)
2. **Padrão EAV (Entity-Attribute-Value)** para campos dinâmicos customizados
3. **JSONB** (PostgreSQL) ou **JSON** (MySQL 5.7+) como alternativa moderna

---

## Opção 1: Padrão EAV (Entity-Attribute-Value) - Recomendado

### Vantagens
✅ Máxima flexibilidade para campos dinâmicos  
✅ Validação de tipos de dados  
✅ Queries estruturadas possíveis  
✅ Histórico de mudanças rastreável  
✅ Suporta qualquer banco relacional  

### Desvantagens
⚠️ Queries mais complexas  
⚠️ Performance pode degradar com muitos atributos  
⚠️ Requer índices cuidadosos  

### Estrutura do Banco de Dados

```sql
-- Tabelas fixas existentes
CREATE TABLE pessoa (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE endereco (
    id BIGSERIAL PRIMARY KEY,
    pessoa_id BIGINT REFERENCES pessoa(id) ON DELETE CASCADE,
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabelas para campos dinâmicos (EAV)
CREATE TABLE campo_customizado (
    id BIGSERIAL PRIMARY KEY,
    entidade VARCHAR(50) NOT NULL, -- 'pessoa' ou 'endereco'
    nome VARCHAR(100) NOT NULL,
    label VARCHAR(255) NOT NULL,
    tipo_dado VARCHAR(50) NOT NULL, -- 'text', 'number', 'date', 'boolean', 'select', 'email', 'phone'
    obrigatorio BOOLEAN DEFAULT FALSE,
    opcoes JSONB, -- Para campos tipo 'select': ["Opção 1", "Opção 2"]
    validacao JSONB, -- Regras de validação: {"min": 0, "max": 100, "pattern": "regex"}
    ordem INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entidade, nome)
);

CREATE TABLE valor_campo_customizado (
    id BIGSERIAL PRIMARY KEY,
    campo_id BIGINT REFERENCES campo_customizado(id) ON DELETE CASCADE,
    entidade_id BIGINT NOT NULL, -- ID da pessoa ou endereço
    valor_texto TEXT,
    valor_numero NUMERIC,
    valor_data DATE,
    valor_booleano BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(campo_id, entidade_id)
);

-- Índices para performance
CREATE INDEX idx_valor_campo_entidade ON valor_campo_customizado(entidade_id);
CREATE INDEX idx_valor_campo_campo_id ON valor_campo_customizado(campo_id);
CREATE INDEX idx_campo_customizado_entidade ON campo_customizado(entidade);
```

### Exemplo de Dados

```sql
-- Criar campo customizado "Profissão" para Pessoa
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, obrigatorio, ordem)
VALUES ('pessoa', 'profissao', 'Profissão', 'text', false, 1);

-- Criar campo customizado "Complemento" para Endereço
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, obrigatorio, ordem)
VALUES ('endereco', 'complemento', 'Complemento', 'text', false, 2);

-- Criar campo tipo select "Estado Civil"
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, obrigatorio, opcoes, ordem)
VALUES ('pessoa', 'estado_civil', 'Estado Civil', 'select', false, 
        '["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]'::jsonb, 3);

-- Armazenar valor para uma pessoa específica
INSERT INTO valor_campo_customizado (campo_id, entidade_id, valor_texto)
VALUES (1, 100, 'Engenheiro de Software');
```

---

## Opção 2: Coluna JSONB (PostgreSQL) - Alternativa Moderna

### Vantagens
✅ Mais simples de implementar  
✅ Queries diretas com operadores JSONB  
✅ Índices GIN para performance  
✅ Menos tabelas  

### Desvantagens
⚠️ Menos estruturado  
⚠️ Validação mais complexa  
⚠️ Específico do PostgreSQL  

### Estrutura do Banco de Dados

```sql
-- Adicionar coluna JSONB às tabelas existentes
ALTER TABLE pessoa ADD COLUMN campos_customizados JSONB DEFAULT '{}'::jsonb;
ALTER TABLE endereco ADD COLUMN campos_customizados JSONB DEFAULT '{}'::jsonb;

-- Índice GIN para queries eficientes
CREATE INDEX idx_pessoa_campos_gin ON pessoa USING GIN (campos_customizados);
CREATE INDEX idx_endereco_campos_gin ON endereco USING GIN (campos_customizados);

-- Tabela de metadados dos campos (para o form builder)
CREATE TABLE definicao_campo_customizado (
    id BIGSERIAL PRIMARY KEY,
    entidade VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    label VARCHAR(255) NOT NULL,
    tipo_dado VARCHAR(50) NOT NULL,
    obrigatorio BOOLEAN DEFAULT FALSE,
    opcoes JSONB,
    validacao JSONB,
    ordem INTEGER DEFAULT 0,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entidade, nome)
);
```

### Exemplo de Uso

```sql
-- Inserir pessoa com campos customizados
INSERT INTO pessoa (nome, cpf, email, campos_customizados)
VALUES ('João Silva', '12345678901', 'joao@email.com', 
        '{"profissao": "Engenheiro", "estado_civil": "Casado(a)", "telefone_comercial": "27999999999"}'::jsonb);

-- Query por campo customizado
SELECT * FROM pessoa 
WHERE campos_customizados->>'profissao' = 'Engenheiro';

-- Query com índice GIN
SELECT * FROM pessoa 
WHERE campos_customizados @> '{"estado_civil": "Casado(a)"}'::jsonb;
```

---

## Arquitetura da Aplicação

### Backend (API REST)

```
backend/
├── models/
│   ├── pessoa.py
│   ├── endereco.py
│   ├── campo_customizado.py
│   └── valor_campo_customizado.py
├── controllers/
│   ├── pessoa_controller.py
│   ├── campo_customizado_controller.py
│   └── form_builder_controller.py
├── services/
│   ├── dynamic_form_service.py
│   └── validation_service.py
└── routes/
    ├── pessoa_routes.py
    └── campo_customizado_routes.py
```

### Endpoints Principais

```
# Gerenciamento de Campos Customizados
POST   /api/campos-customizados          # Criar novo campo
GET    /api/campos-customizados          # Listar campos por entidade
PUT    /api/campos-customizados/:id      # Atualizar campo
DELETE /api/campos-customizados/:id      # Remover campo

# Gerenciamento de Pessoas com Campos Dinâmicos
POST   /api/pessoas                      # Criar pessoa (com campos customizados)
GET    /api/pessoas/:id                  # Obter pessoa (com valores customizados)
PUT    /api/pessoas/:id                  # Atualizar pessoa
GET    /api/pessoas/formulario           # Obter definição do formulário

# Gerenciamento de Endereços
POST   /api/pessoas/:id/enderecos        # Criar endereço
GET    /api/pessoas/:id/enderecos        # Listar endereços
```

### Exemplo de Payload (Criar Pessoa)

```json
{
  "nome": "Maria Santos",
  "cpf": "98765432100",
  "email": "maria@email.com",
  "campos_customizados": {
    "profissao": "Médica",
    "estado_civil": "Solteiro(a)",
    "telefone_comercial": "27988888888",
    "data_nascimento": "1990-05-15"
  },
  "enderecos": [
    {
      "logradouro": "Rua das Flores",
      "numero": "123",
      "cidade": "Vitória",
      "estado": "ES",
      "cep": "29000000",
      "campos_customizados": {
        "complemento": "Apto 301",
        "ponto_referencia": "Próximo ao shopping"
      }
    }
  ]
}
```

---

## Frontend (Form Builder + Renderer)

### Componentes Principais

```
frontend/
├── components/
│   ├── FormBuilder/
│   │   ├── FormBuilder.vue          # Interface para criar campos
│   │   ├── FieldEditor.vue          # Editor de propriedades do campo
│   │   └── FieldTypeSelector.vue    # Seletor de tipo de campo
│   ├── DynamicForm/
│   │   ├── DynamicForm.vue          # Renderizador do formulário
│   │   ├── DynamicField.vue         # Componente genérico de campo
│   │   └── FieldTypes/
│   │       ├── TextField.vue
│   │       ├── NumberField.vue
│   │       ├── DateField.vue
│   │       ├── SelectField.vue
│   │       └── BooleanField.vue
│   └── PessoaForm/
│       └── PessoaForm.vue           # Formulário completo de Pessoa
└── services/
    ├── campo_customizado_service.js
    └── pessoa_service.js
```

### Fluxo de Uso

1. **Administrador acessa Form Builder**
   - Define novos campos customizados
   - Configura tipo, validação, obrigatoriedade
   - Salva definições via API

2. **Usuário preenche formulário**
   - Sistema carrega definição de campos (fixos + customizados)
   - Renderiza formulário dinamicamente
   - Valida dados no frontend e backend
   - Submete dados via API

3. **Sistema armazena dados**
   - Campos fixos → tabelas `pessoa`/`endereco`
   - Campos customizados → tabela `valor_campo_customizado` ou coluna JSONB

---

## Validação em Camadas

### 1. Frontend (Vue.js/React)
```javascript
const validationRules = {
  text: (value, rules) => {
    if (rules.required && !value) return 'Campo obrigatório';
    if (rules.minLength && value.length < rules.minLength) 
      return `Mínimo ${rules.minLength} caracteres`;
    if (rules.pattern && !new RegExp(rules.pattern).test(value))
      return 'Formato inválido';
    return null;
  },
  number: (value, rules) => {
    if (rules.required && value === null) return 'Campo obrigatório';
    if (rules.min && value < rules.min) return `Mínimo: ${rules.min}`;
    if (rules.max && value > rules.max) return `Máximo: ${rules.max}`;
    return null;
  }
};
```

### 2. Backend (Python/Node.js)
```python
class DynamicFormValidator:
    def validate_custom_fields(self, entity_type, custom_data):
        fields = CampoCustomizado.query.filter_by(
            entidade=entity_type, 
            ativo=True
        ).all()
        
        errors = {}
        for field in fields:
            value = custom_data.get(field.nome)
            
            # Validar obrigatoriedade
            if field.obrigatorio and not value:
                errors[field.nome] = f'{field.label} é obrigatório'
                continue
            
            # Validar tipo de dado
            if value and not self._validate_type(value, field.tipo_dado):
                errors[field.nome] = f'{field.label} tem tipo inválido'
            
            # Validar regras customizadas
            if field.validacao:
                validation_error = self._apply_rules(value, field.validacao)
                if validation_error:
                    errors[field.nome] = validation_error
        
        return errors
```

---

## Queries Complexas (Relatórios)

### Exemplo: Buscar pessoas por campo customizado

```sql
-- EAV Pattern
SELECT p.*, vcc.valor_texto as profissao
FROM pessoa p
LEFT JOIN valor_campo_customizado vcc ON vcc.entidade_id = p.id
LEFT JOIN campo_customizado cc ON cc.id = vcc.campo_id
WHERE cc.nome = 'profissao' 
  AND vcc.valor_texto ILIKE '%engenheiro%';

-- JSONB Pattern
SELECT * FROM pessoa
WHERE campos_customizados->>'profissao' ILIKE '%engenheiro%';
```

### Exemplo: Relatório com múltiplos campos customizados

```sql
-- Pivot dinâmico com EAV
SELECT 
    p.id,
    p.nome,
    MAX(CASE WHEN cc.nome = 'profissao' THEN vcc.valor_texto END) as profissao,
    MAX(CASE WHEN cc.nome = 'estado_civil' THEN vcc.valor_texto END) as estado_civil,
    MAX(CASE WHEN cc.nome = 'telefone_comercial' THEN vcc.valor_texto END) as telefone
FROM pessoa p
LEFT JOIN valor_campo_customizado vcc ON vcc.entidade_id = p.id
LEFT JOIN campo_customizado cc ON cc.id = vcc.campo_id
GROUP BY p.id, p.nome;
```

---

## Considerações de Performance

### Índices Recomendados
```sql
-- Para EAV
CREATE INDEX idx_valor_entidade_campo ON valor_campo_customizado(entidade_id, campo_id);
CREATE INDEX idx_valor_texto ON valor_campo_customizado(valor_texto) WHERE valor_texto IS NOT NULL;
CREATE INDEX idx_valor_numero ON valor_campo_customizado(valor_numero) WHERE valor_numero IS NOT NULL;

-- Para JSONB
CREATE INDEX idx_pessoa_campos_gin ON pessoa USING GIN (campos_customizados);
CREATE INDEX idx_pessoa_profissao ON pessoa ((campos_customizados->>'profissao'));
```

### Estratégias de Otimização
1. **Cache** de definições de campos (Redis)
2. **Materialização** de views para relatórios complexos
3. **Particionamento** da tabela `valor_campo_customizado` por entidade
4. **Denormalização seletiva** para campos muito consultados

---

## Tecnologias Recomendadas

### Stack Backend
- **Python**: FastAPI ou Flask
- **Node.js**: Express ou NestJS
- **Java**: Spring Boot

### Stack Frontend
- **Vue.js 3** + Vite (recomendado para form builders)
- **React** + Next.js
- **Angular**

### Banco de Dados
- **PostgreSQL 12+** (suporta JSONB e queries avançadas)
- **MySQL 8.0+** (suporta JSON)
- **SQL Server 2016+**

### Bibliotecas Úteis
- **Frontend**: FormKit, VeeValidate, React Hook Form
- **Backend**: Pydantic (Python), Joi (Node.js), Hibernate Validator (Java)

---

## Próximos Passos

1. **Escolher abordagem**: EAV vs JSONB vs Híbrida
2. **Definir stack tecnológico**: Backend e Frontend
3. **Criar protótipo**: Form Builder básico
4. **Implementar validações**: Frontend e Backend
5. **Testes de performance**: Com volume realista de dados
6. **Documentação**: API e guia de uso

---

## Recomendação Final

Para seu caso, recomendo:

> **Abordagem Híbrida**: EAV para metadados + JSONB para valores
> 
> - Use tabela `campo_customizado` para definições (EAV)
> - Use coluna JSONB em `pessoa`/`endereco` para armazenar valores
> - Melhor dos dois mundos: estrutura + flexibilidade

Esta abordagem oferece:
- ✅ Validação estruturada via metadados
- ✅ Performance de queries com JSONB
- ✅ Facilidade de manutenção
- ✅ Escalabilidade

