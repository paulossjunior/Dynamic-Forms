# Documentação Técnica: Sistema de Formulários Dinâmicos

**Versão:** 1.0  
**Status:** Especificação Técnica Final  
**Autor:** Antigravity AI  

---

## 1. Introdução
Esta documentação descreve a arquitetura técnica para a implementação de um sistema de formulários dinâmicos integrado a um banco de dados relacional (PostgreSQL 12+ recomendado). O sistema permite que administradores criem campos customizados com tipagem, validação e suporte a múltiplos valores, sem a necessidade de alterações no esquema fixo do banco de dados para cada novo campo.

## 2. Visão Geral da Arquitetura

O sistema adota um padrão **Híbrido EAV-JSONB**:
- **Metadados (EAV)**: Armazenados em uma tabela de definições para gerenciar tipos, labels e regras.
- **Valores (JSONB)**: Armazenados em colunas nativas JSONB nas tabelas de negócio (`pessoa`, `endereco`) para alta performance e flexibilidade.

### Tecnologias Recomendadas
- **Backend:** Python (FastAPI/Flask) ou Node.js (NestJS).
- **Banco de Dados:** PostgreSQL 12.4+ (suporte avançado a JSONB e GIN indexes).
- **Frontend:** Vue.js 3 ou React com bibliotecas de formulários (FormKit/React Hook Form).

---

## 3. Modelo de Dados (DDL)

### 3.1. Tabelas Fixas
```sql
CREATE TABLE pessoa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(11) UNIQUE,
    email VARCHAR(255),
    campos_customizados JSONB DEFAULT '{}', -- Armazena valores dinâmicos
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE endereco (
    id SERIAL PRIMARY KEY,
    pessoa_id INTEGER REFERENCES pessoa(id) ON DELETE CASCADE,
    logradouro VARCHAR(255),
    campos_customizados JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2. Definição de Campos (Metadados)
```sql
CREATE TABLE definicao_campo_customizado (
    id SERIAL PRIMARY KEY,
    entidade VARCHAR(50) NOT NULL, -- 'pessoa' ou 'endereco'
    nome_tecnico VARCHAR(100) NOT NULL, -- slug gerado: raca_cor
    nome_normalizado VARCHAR(100) NOT NULL, -- p/ prevenção de duplicatas
    configuracao JSONB NOT NULL, -- Configurações de UI e Validação
    status VARCHAR(20) DEFAULT 'aprovado',
    ativo BOOLEAN DEFAULT TRUE,
    UNIQUE(entidade, nome_normalizado)
);

CREATE INDEX idx_definicao_config_gin ON definicao_campo_customizado USING GIN (configuracao);
```

---

## 4. Estrutura do JSON de Configuração
Cada campo possui um objeto de configuração que dita o comportamento no Frontend e no Backend.

```json
{
  "label": "Raça ou Cor",
  "tipo": "checkbox_group",
  "placeholder": "Selecione",
  "opcoes": ["Branca", "Preta", "Parda", "Amarela", "Indígena"],
  "permite_multiplos": true,
  "validacao": {
    "obrigatorio": true,
    "min_items": 1,
    "mensagem_obrigatorio": "Este campo é mandatório"
  },
  "ui": {
    "ordem": 10,
    "largura": "50%",
    "visivel": true
  }
}
```

---

## 5. Lógica de Validação

O sistema deve implementar um motor de validação que consome o JSON acima.

### 5.1. Tipos de Campos e Regras
| Tipo | Validação Nativa | Formato de Dados |
|------|------------------|------------------|
| `text` | Regex, Min/Max | String |
| `number` | Range (Min/Max) | Numeric |
| `date` | Min/Max Date | ISO Date String |
| `email` | RFC 5322 | String |
| `cpf` | Módulo 11 (Brasil) | String (numérica) |
| `checkbox_group` | Min/Max Items | Array de Strings |

---

## 6. Business Intelligence (BI) e Analytics

Para garantir que os dados "escondidos" no JSON sejam analisáveis, deve-se utilizar o padrão de **Flattening via SQL Views**.

### 6.1. SQL View para BI
```sql
CREATE VIEW vw_bi_consolidado AS
SELECT 
    p.id,
    p.nome,
    p.campos_customizados->>'sexo' AS genero,
    -- Converte array JSONB em string para o Power BI
    (SELECT string_agg(val, ', ') 
     FROM jsonb_array_elements_text(p.campos_customizados->'raca_cor') AS val) AS raca_cor
FROM pessoa p;
```

---

## 7. Prevenção de Duplicatas Semânticas

Para evitar a criação de campos redundantes (ex: `raca` e `raça`):
1. **Normalização:** Todos os nomes de entrada são convertidos para `lowercase`, sem acentos e espaços substituídos por underscores.
2. **Constraint de Banco:** A coluna `nome_normalizado` possui índice UNIQUE.
3. **Fuzzy Matching:** O backend deve calcular a Distância de Levenshtein entre o novo campo e os existentes, bloqueando se a similaridade for > 85%.

---

## 8. Segurança e Performance

### 8.1. Performance
- Sempre use **GIN Indexes** nas colunas `campos_customizados` no PostgreSQL para permitir que buscas dentro do JSON sejam tão rápidas quanto em colunas normais.
- Utilize **Views Materializadas** para relatórios pesados, atualizando-as via CRON ou Triggers.

### 8.2. Segurança
- Valide o esquema do JSON de entrada contra a `definicao_campo_customizado` em cada `POST`/`PUT`.
- Higienize strings de entrada para prevenir XSS armazenado dentro do JSON.

---

## 9. Endpoints da API (RESUMO)

- `GET /api/v1/meta/campos/{entidade}`: Carrega estrutura para renderizar o form.
- `POST /api/v1/{entidade}`: Recebe dados fixos + `campos_customizados`.
- `GET /api/v1/reports/export`: Exporta os dados já "achatados" em CSV/Parquet.

---
*Fim do Documento Técnico*
