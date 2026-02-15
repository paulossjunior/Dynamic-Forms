# Proposta de Arquitetura: Formulários Dinâmicos em Bancos Relacionais

Esta proposta detalha como permitir que usuários criem campos customizados em um sistema com tabelas fixas (Pessoa e Endereço), mantendo a integridade, validação e capacidade de análise (BI).

---

## 1. O Desafio
Adicionar flexibilidade (campos dinâmicos) a um ambiente rígido (PostgreSQL/MySQL) sem perder:
- **Tipagem** (saber se é texto, número, data).
- **Validação** (regras de obrigatoriedade, máscaras).
- **Qualidade de Dados** (evitar campos duplicados como "raça" e "raca").
- **Capacidade de BI** (gerar relatórios em ferramentas como Power BI).

---

## 2. Arquitetura Recomendada: Padrão Híbrido
A melhor solução utiliza **Metadados (EAV)** para definir os campos e **JSONB** para armazenar os valores.

### Estrutura do Banco (SQL):
```sql
-- Definição dos campos (Metadados)
CREATE TABLE definicao_campo (
    id SERIAL PRIMARY KEY,
    entidade VARCHAR(50), -- 'pessoa' ou 'endereco'
    nome_tecnico VARCHAR(100) UNIQUE, -- slug: raca_cor
    configuracao JSONB -- Regras de validação, label, tipo, opcoes
);

-- Tabelas principais com suporte a JSONB
ALTER TABLE pessoa ADD COLUMN campos_customizados JSONB DEFAULT '{}';
ALTER TABLE endereco ADD COLUMN campos_customizados JSONB DEFAULT '{}';
```

---

## 3. Tipagem e Validação em JSON
Diferente de um JSON bagunçado, aqui as regras de validação ficam dentro da configuração do campo.

**Exemplo de configuração de um campo:**
```json
{
  "label": "Raça ou Cor",
  "tipo": "checkbox_group",
  "permite_multiplos": true,
  "opcoes": ["Branca", "Preta", "Parda", "Amarela", "Indígena"],
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Selecione pelo menos uma opção"
  }
}
```

---

## 4. Campos Multivalorados
Para campos como **Raça/Cor** ou **Idiomas**, onde o usuário seleciona várias opções:
- **Armazenamento**: Array dentro do JSONB `{"raca_cor": ["Parda", "Indígena"]}`.
- **Renderização**: Componentes de `Checkboxes` ou `Multiselect` no frontend.
- **Validação**: Verificação de `min_items` e `max_items` via motor de regras.

---

## 5. Prevenção de Caos (Duplicidade)
Para evitar que usuários criem campos iguais ou parecidos (ex: "Telefone" e "Fone"):
1. **Normalização**: Todo nome é convertido para `snake_case` e sem acentos (raca_cor).
2. **Fuzzy Matching**: O sistema avisa se o usuário tentar criar algo com 80% de similaridade a um campo existente.
3. **Sugestões por Categoria**: Oferecer campos padrão (Sexo, CPF, Data Nasc) para o usuário apenas "ativar".

---

## 6. Business Intelligence (BI) - O Segredo
O maior medo em campos dinâmicos é o relatório. A solução é usar **Views do Banco** para "achatar" o JSON para o Power BI.

**Como funciona:**
1. Criamos uma **VIEW** SQL que extrai cada chave do JSON como uma coluna real.
2. Usamos `jsonb_array_elements` para "explodir" campos multivalorados, permitindo contar cada raça/cor individualmente em um gráfico.
3. O Power BI conecta nessa VIEW e vê uma tabela normal, sem complicação.

---

## 7. Benefícios da Proposta
- ✅ **Flexibilidade**: O usuário cria campos sem precisar de um DBA/Programador.
- ✅ **Performance**: JSONB no PostgreSQL permite índices GIN para buscas rápidas.
- ✅ **Escalabilidade**: Funciona igual para 10 ou 1000 campos novos.
- ✅ **Limpeza**: Views de BI garantem dados tabulares prontos para análise.

---

## 📋 Documentação Detalhada Criada:
- [Arquitetura Geral](file:///home/paulossjunior/.gemini/antigravity/brain/b07b7eb3-c007-4ccf-9f7d-8d1b55365ca8/implementation_plan.md)
- [Campos Multivalorados](file:///home/paulossjunior/.gemini/antigravity/brain/b07b7eb3-c007-4ccf-9f7d-8d1b55365ca8/campos_multivalorados.md)
- [Validação em JSON](file:///home/paulossjunior/.gemini/antigravity/brain/b07b7eb3-c007-4ccf-9f7d-8d1b55365ca8/validacao_json.md)
- [Prevenção de Duplicatas](file:///home/paulossjunior/.gemini/antigravity/brain/b07b7eb3-c007-4ccf-9f7d-8d1b55365ca8/prevencao_duplicatas.md)
- [Guia Prático de BI](file:///home/paulossjunior/.gemini/antigravity/brain/b07b7eb3-c007-4ccf-9f7d-8d1b55365ca8/guia_bi_pratico.md)
