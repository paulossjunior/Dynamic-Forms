# Campos Multivalorados - Especificação Completa

## Visão Geral

Campos multivalorados permitem que o usuário selecione **múltiplas opções** para um mesmo campo. Exemplos comuns incluem:
- **Raça/Cor** (pessoa pode se identificar com múltiplas raças)
- **Idiomas** (pessoa pode falar múltiplos idiomas)
- **Áreas de Interesse**
- **Habilidades/Competências**

Para campos de **seleção única** como **Sexo/Gênero**, usamos `radio` ou `select` simples.

---

## Estrutura do Banco de Dados para Multivalorados

### Opção 1: Tabela de Relacionamento (Recomendado para EAV)

```sql
-- Adicionar suporte a múltiplos valores
CREATE TABLE valor_campo_customizado (
    id BIGSERIAL PRIMARY KEY,
    campo_id BIGINT REFERENCES campo_customizado(id) ON DELETE CASCADE,
    entidade_id BIGINT NOT NULL,
    valor_texto TEXT,
    valor_numero NUMERIC,
    valor_data DATE,
    valor_booleano BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- REMOVER constraint UNIQUE para permitir múltiplos valores
    -- UNIQUE(campo_id, entidade_id) -- ❌ Removido!
);

-- Adicionar índice composto para queries eficientes
CREATE INDEX idx_valor_campo_entidade_campo ON valor_campo_customizado(entidade_id, campo_id);

-- Adicionar flag no campo_customizado para indicar se aceita múltiplos valores
ALTER TABLE campo_customizado ADD COLUMN permite_multiplos BOOLEAN DEFAULT FALSE;
```

### Opção 2: Array JSONB (PostgreSQL)

```sql
-- Usar JSONB array para armazenar múltiplos valores
ALTER TABLE valor_campo_customizado ADD COLUMN valor_array JSONB;

-- Índice GIN para buscar dentro do array
CREATE INDEX idx_valor_array_gin ON valor_campo_customizado USING GIN (valor_array);
```

### Opção 3: Coluna JSONB Direta (Mais Simples)

```sql
-- Se usar abordagem JSONB pura, arrays são nativos
ALTER TABLE pessoa ADD COLUMN campos_customizados JSONB DEFAULT '{}'::jsonb;

-- Exemplo de dados:
-- {"racas": ["Parda", "Indígena"], "idiomas": ["Português", "Inglês", "Espanhol"]}
```

---

## Tipos de Campos Multivalorados

### 1. Multiselect (Dropdown com Múltipla Seleção)

**Uso**: Quando há muitas opções e o usuário pode selecionar várias.

```sql
INSERT INTO campo_customizado (
    entidade, nome, label, tipo_dado, permite_multiplos, opcoes, ordem
) VALUES (
    'pessoa', 
    'idiomas', 
    'Idiomas que fala', 
    'multiselect', 
    true,
    '["Português", "Inglês", "Espanhol", "Francês", "Alemão", "Mandarim", "Japonês"]'::jsonb,
    10
);
```

**Renderização Frontend**:
```vue
<template>
  <div class="field-multiselect">
    <label>{{ field.label }}</label>
    <select multiple v-model="selectedValues">
      <option v-for="option in field.opcoes" :key="option" :value="option">
        {{ option }}
      </option>
    </select>
  </div>
</template>
```

### 2. Checkbox Group (Grupo de Checkboxes)

**Uso**: Quando há poucas opções (até ~10) e é importante visualizar todas.

**Exemplo: Raça/Cor (IBGE)**

```sql
INSERT INTO campo_customizado (
    entidade, nome, label, tipo_dado, permite_multiplos, opcoes, ordem
) VALUES (
    'pessoa', 
    'raca_cor', 
    'Raça/Cor (autodeclaração)', 
    'checkbox_group', 
    true,
    '["Branca", "Preta", "Parda", "Amarela", "Indígena"]'::jsonb,
    5
);
```

**Renderização Frontend**:
```vue
<template>
  <div class="field-checkbox-group">
    <label>{{ field.label }}</label>
    <div class="checkbox-options">
      <label v-for="option in field.opcoes" :key="option" class="checkbox-item">
        <input 
          type="checkbox" 
          :value="option" 
          v-model="selectedValues"
        />
        {{ option }}
      </label>
    </div>
  </div>
</template>
```

### 3. Radio Button (Seleção Única)

**Uso**: Para campos que aceitam **apenas uma opção**.

**Exemplo: Sexo/Gênero**

```sql
INSERT INTO campo_customizado (
    entidade, nome, label, tipo_dado, permite_multiplos, opcoes, ordem
) VALUES (
    'pessoa', 
    'sexo', 
    'Sexo', 
    'radio', 
    false, -- ❗ Seleção única
    '["Masculino", "Feminino", "Outro", "Prefiro não informar"]'::jsonb,
    4
);
```

**Renderização Frontend**:
```vue
<template>
  <div class="field-radio">
    <label>{{ field.label }}</label>
    <div class="radio-options">
      <label v-for="option in field.opcoes" :key="option" class="radio-item">
        <input 
          type="radio" 
          :name="field.nome" 
          :value="option" 
          v-model="selectedValue"
        />
        {{ option }}
      </label>
    </div>
  </div>
</template>
```

### 4. Tags (Entrada Livre + Sugestões)

**Uso**: Quando o usuário pode criar valores customizados além das opções predefinidas.

```sql
INSERT INTO campo_customizado (
    entidade, nome, label, tipo_dado, permite_multiplos, opcoes, ordem
) VALUES (
    'pessoa', 
    'habilidades', 
    'Habilidades/Competências', 
    'tags', 
    true,
    '["Python", "JavaScript", "SQL", "Docker", "AWS", "React", "Vue.js"]'::jsonb, -- Sugestões
    15
);
```

**Renderização Frontend** (com biblioteca como vue-multiselect):
```vue
<template>
  <div class="field-tags">
    <label>{{ field.label }}</label>
    <multiselect
      v-model="selectedValues"
      :options="field.opcoes"
      :multiple="true"
      :taggable="true"
      @tag="addTag"
      placeholder="Digite ou selecione"
    />
  </div>
</template>
```

---

## Armazenamento de Dados

### Exemplo 1: EAV com Múltiplos Registros

```sql
-- Pessoa ID 100 seleciona múltiplas raças
INSERT INTO valor_campo_customizado (campo_id, entidade_id, valor_texto)
VALUES 
    (5, 100, 'Parda'),
    (5, 100, 'Indígena');

-- Query para obter valores
SELECT vcc.valor_texto
FROM valor_campo_customizado vcc
JOIN campo_customizado cc ON cc.id = vcc.campo_id
WHERE cc.nome = 'raca_cor' AND vcc.entidade_id = 100;

-- Resultado:
-- Parda
-- Indígena
```

### Exemplo 2: JSONB Array

```sql
-- Armazenar como array JSONB
INSERT INTO valor_campo_customizado (campo_id, entidade_id, valor_array)
VALUES (5, 100, '["Parda", "Indígena"]'::jsonb);

-- Query para buscar pessoas que selecionaram "Parda"
SELECT p.*
FROM pessoa p
JOIN valor_campo_customizado vcc ON vcc.entidade_id = p.id
JOIN campo_customizado cc ON cc.id = vcc.campo_id
WHERE cc.nome = 'raca_cor' 
  AND vcc.valor_array ? 'Parda'; -- Operador ? verifica se existe no array
```

### Exemplo 3: JSONB Direto na Tabela Pessoa

```sql
-- Inserir pessoa com campos multivalorados
INSERT INTO pessoa (nome, cpf, campos_customizados)
VALUES (
    'Ana Silva',
    '11122233344',
    '{
        "sexo": "Feminino",
        "raca_cor": ["Parda", "Indígena"],
        "idiomas": ["Português", "Espanhol", "Guarani"],
        "habilidades": ["Python", "Data Science", "Machine Learning"]
    }'::jsonb
);

-- Query: Buscar pessoas que falam Espanhol
SELECT * FROM pessoa
WHERE campos_customizados->'idiomas' ? 'Espanhol';

-- Query: Buscar pessoas que se identificam como Parda
SELECT * FROM pessoa
WHERE campos_customizados->'raca_cor' ? 'Parda';
```

---

## Payload da API (Criar/Atualizar Pessoa)

### Exemplo Completo com Campos Multivalorados

```json
{
  "nome": "Carlos Mendes",
  "cpf": "55566677788",
  "email": "carlos@email.com",
  "campos_customizados": {
    "sexo": "Masculino",
    "raca_cor": ["Preta", "Parda"],
    "estado_civil": "Casado(a)",
    "idiomas": ["Português", "Inglês", "Francês"],
    "profissao": "Engenheiro de Software",
    "habilidades": ["Python", "JavaScript", "Docker", "Kubernetes", "AWS"],
    "data_nascimento": "1985-03-20",
    "telefone_comercial": "27999887766"
  },
  "enderecos": [
    {
      "logradouro": "Av. Principal",
      "numero": "500",
      "cidade": "Vitória",
      "estado": "ES",
      "cep": "29050000",
      "campos_customizados": {
        "complemento": "Sala 1001",
        "tipo_imovel": ["Comercial", "Residencial"]
      }
    }
  ]
}
```

---

## Validação de Campos Multivalorados

### Backend (Python/FastAPI)

```python
from typing import List, Union

class DynamicFormValidator:
    def validate_multivalue_field(
        self, 
        field_definition: CampoCustomizado, 
        value: Union[str, List[str]]
    ) -> List[str]:
        errors = []
        
        # Converter para lista se necessário
        values = value if isinstance(value, list) else [value]
        
        # Validar se campo aceita múltiplos valores
        if len(values) > 1 and not field_definition.permite_multiplos:
            errors.append(f'{field_definition.label} aceita apenas um valor')
            return errors
        
        # Validar se valores estão nas opções permitidas
        if field_definition.opcoes:
            opcoes_validas = field_definition.opcoes
            for v in values:
                if v not in opcoes_validas:
                    errors.append(f'"{v}" não é uma opção válida para {field_definition.label}')
        
        # Validar obrigatoriedade
        if field_definition.obrigatorio and not values:
            errors.append(f'{field_definition.label} é obrigatório')
        
        return errors
```

### Frontend (Vue.js)

```javascript
const validateMultiValueField = (field, value) => {
  const errors = [];
  const values = Array.isArray(value) ? value : [value];
  
  // Validar múltiplos valores
  if (values.length > 1 && !field.permite_multiplos) {
    errors.push(`${field.label} aceita apenas um valor`);
    return errors;
  }
  
  // Validar opções
  if (field.opcoes && field.opcoes.length > 0) {
    const invalidValues = values.filter(v => !field.opcoes.includes(v));
    if (invalidValues.length > 0) {
      errors.push(`Valores inválidos: ${invalidValues.join(', ')}`);
    }
  }
  
  // Validar obrigatoriedade
  if (field.obrigatorio && values.length === 0) {
    errors.push(`${field.label} é obrigatório`);
  }
  
  return errors;
};
```

---

## Queries e Relatórios

### Exemplo 1: Contar pessoas por raça/cor

```sql
-- EAV com múltiplos registros
SELECT vcc.valor_texto as raca, COUNT(DISTINCT vcc.entidade_id) as total
FROM valor_campo_customizado vcc
JOIN campo_customizado cc ON cc.id = vcc.campo_id
WHERE cc.nome = 'raca_cor'
GROUP BY vcc.valor_texto
ORDER BY total DESC;

-- Resultado:
-- raca    | total
-- --------|------
-- Parda   | 450
-- Branca  | 320
-- Preta   | 180
-- Indígena| 45
-- Amarela | 25
```

### Exemplo 2: Buscar pessoas que falam Inglês E Espanhol

```sql
-- JSONB
SELECT * FROM pessoa
WHERE campos_customizados->'idiomas' ?& ARRAY['Inglês', 'Espanhol'];
-- Operador ?& verifica se TODOS os elementos existem no array
```

### Exemplo 3: Buscar pessoas que falam Inglês OU Espanhol

```sql
-- JSONB
SELECT * FROM pessoa
WHERE campos_customizados->'idiomas' ?| ARRAY['Inglês', 'Espanhol'];
-- Operador ?| verifica se QUALQUER elemento existe no array
```

### Exemplo 4: Relatório de diversidade racial

```sql
-- Pessoas que se identificam com múltiplas raças
SELECT 
    p.id,
    p.nome,
    jsonb_array_length(p.campos_customizados->'raca_cor') as num_racas,
    p.campos_customizados->'raca_cor' as racas
FROM pessoa p
WHERE jsonb_array_length(p.campos_customizados->'raca_cor') > 1;
```

---

## Componentes Frontend Completos

### MultiSelectField.vue

```vue
<template>
  <div class="dynamic-field multiselect-field">
    <label :for="field.nome" class="field-label">
      {{ field.label }}
      <span v-if="field.obrigatorio" class="required">*</span>
    </label>
    
    <select 
      :id="field.nome"
      :name="field.nome"
      multiple
      v-model="internalValue"
      @change="handleChange"
      class="multiselect-input"
      :class="{ 'has-error': hasError }"
    >
      <option 
        v-for="option in field.opcoes" 
        :key="option" 
        :value="option"
      >
        {{ option }}
      </option>
    </select>
    
    <div v-if="internalValue.length > 0" class="selected-tags">
      <span 
        v-for="value in internalValue" 
        :key="value" 
        class="tag"
      >
        {{ value }}
        <button @click="removeValue(value)" class="tag-remove">×</button>
      </span>
    </div>
    
    <span v-if="error" class="error-message">{{ error }}</span>
    <span v-if="field.descricao" class="field-help">{{ field.descricao }}</span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  field: Object,
  modelValue: [Array, String],
  error: String
});

const emit = defineEmits(['update:modelValue']);

const internalValue = ref(
  Array.isArray(props.modelValue) ? props.modelValue : []
);

const hasError = computed(() => !!props.error);

const handleChange = () => {
  emit('update:modelValue', internalValue.value);
};

const removeValue = (value) => {
  internalValue.value = internalValue.value.filter(v => v !== value);
  handleChange();
};

watch(() => props.modelValue, (newValue) => {
  internalValue.value = Array.isArray(newValue) ? newValue : [];
});
</script>

<style scoped>
.multiselect-input {
  width: 100%;
  min-height: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.multiselect-input.has-error {
  border-color: #e74c3c;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #3498db;
  color: white;
  border-radius: 4px;
  font-size: 14px;
}

.tag-remove {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}
</style>
```

### CheckboxGroupField.vue

```vue
<template>
  <div class="dynamic-field checkbox-group-field">
    <label class="field-label">
      {{ field.label }}
      <span v-if="field.obrigatorio" class="required">*</span>
    </label>
    
    <div class="checkbox-options">
      <label 
        v-for="option in field.opcoes" 
        :key="option" 
        class="checkbox-item"
      >
        <input 
          type="checkbox" 
          :value="option" 
          v-model="internalValue"
          @change="handleChange"
        />
        <span class="checkbox-label">{{ option }}</span>
      </label>
    </div>
    
    <span v-if="error" class="error-message">{{ error }}</span>
    <span v-if="field.descricao" class="field-help">{{ field.descricao }}</span>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  field: Object,
  modelValue: [Array, String],
  error: String
});

const emit = defineEmits(['update:modelValue']);

const internalValue = ref(
  Array.isArray(props.modelValue) ? props.modelValue : []
);

const handleChange = () => {
  emit('update:modelValue', internalValue.value);
};

watch(() => props.modelValue, (newValue) => {
  internalValue.value = Array.isArray(newValue) ? newValue : [];
});
</script>

<style scoped>
.checkbox-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-label {
  font-size: 16px;
  user-select: none;
}
</style>
```

---

## Resumo de Tipos de Campos

| Tipo | Permite Múltiplos | Uso Ideal | Exemplo |
|------|-------------------|-----------|---------|
| `text` | ❌ | Texto livre curto | Nome, CPF |
| `textarea` | ❌ | Texto livre longo | Observações |
| `number` | ❌ | Valores numéricos | Idade, Salário |
| `date` | ❌ | Datas | Data de Nascimento |
| `email` | ❌ | Emails | Email principal |
| `phone` | ❌ | Telefones | Telefone |
| `boolean` | ❌ | Sim/Não | Ativo, Aceita termos |
| `radio` | ❌ | Seleção única de lista | Sexo, Estado Civil |
| `select` | ❌ | Seleção única (muitas opções) | País, Estado |
| `multiselect` | ✅ | Múltiplas opções (muitas opções) | Idiomas, Países visitados |
| `checkbox_group` | ✅ | Múltiplas opções (poucas opções) | Raça/Cor, Áreas de interesse |
| `tags` | ✅ | Entrada livre + sugestões | Habilidades, Tags |

---

## Recomendação Final

Para **dados demográficos** como solicitado:

```sql
-- Sexo/Gênero (seleção única)
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, permite_multiplos, opcoes)
VALUES ('pessoa', 'sexo', 'Sexo', 'radio', false, 
        '["Masculino", "Feminino", "Outro", "Prefiro não informar"]'::jsonb);

-- Raça/Cor (múltipla seleção - IBGE)
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, permite_multiplos, opcoes)
VALUES ('pessoa', 'raca_cor', 'Raça/Cor (autodeclaração)', 'checkbox_group', true, 
        '["Branca", "Preta", "Parda", "Amarela", "Indígena"]'::jsonb);

-- Etnia/Povo Indígena (se aplicável)
INSERT INTO campo_customizado (entidade, nome, label, tipo_dado, permite_multiplos, opcoes)
VALUES ('pessoa', 'etnia_indigena', 'Etnia/Povo Indígena', 'tags', true, 
        '["Guarani", "Tupiniquim", "Pataxó", "Krenak", "Maxakali"]'::jsonb);
```

✅ **Sexo**: Radio button (seleção única)  
✅ **Raça/Cor**: Checkbox group (múltipla seleção)  
✅ **Etnia**: Tags (entrada livre com sugestões)
