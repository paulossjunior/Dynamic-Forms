# Prevenção de Campos Duplicados e Similares

## Visão Geral do Problema

Usuários podem criar campos semanticamente idênticos com nomes diferentes:
- "raça" vs "raca" (sem acento)
- "Raça/Cor" vs "raca_cor" vs "racacor"
- "telefone" vs "fone" vs "tel"
- "data_nascimento" vs "dataNascimento" vs "dt_nasc"

Isso causa:
- ❌ Dados fragmentados
- ❌ Relatórios inconsistentes
- ❌ Confusão para usuários
- ❌ Dificuldade em análises de BI

---

## Estratégia 1: Normalização e Validação de Nomes

### Regras de Normalização

```sql
-- Adicionar colunas para normalização
ALTER TABLE definicao_campo_customizado 
ADD COLUMN nome_normalizado VARCHAR(100),
ADD COLUMN slug VARCHAR(100);

-- Constraint de unicidade no nome normalizado
CREATE UNIQUE INDEX idx_campo_nome_normalizado 
ON definicao_campo_customizado(entidade, nome_normalizado);
```

### Função de Normalização (Python)

```python
import re
import unicodedata

class FieldNameNormalizer:
    """Normaliza nomes de campos para prevenir duplicatas"""
    
    @staticmethod
    def normalize(name: str) -> str:
        """
        Normaliza nome do campo:
        - Remove acentos
        - Converte para minúsculas
        - Remove caracteres especiais
        - Substitui espaços por underscore
        """
        # Remover acentos
        nfkd = unicodedata.normalize('NFKD', name)
        name_sem_acento = ''.join([c for c in nfkd if not unicodedata.combining(c)])
        
        # Converter para minúsculas
        name_lower = name_sem_acento.lower()
        
        # Remover caracteres especiais (manter apenas letras, números e underscore)
        name_clean = re.sub(r'[^a-z0-9_]', '_', name_lower)
        
        # Remover underscores duplicados
        name_clean = re.sub(r'_+', '_', name_clean)
        
        # Remover underscores no início e fim
        name_clean = name_clean.strip('_')
        
        return name_clean
    
    @staticmethod
    def generate_slug(label: str) -> str:
        """Gera slug a partir do label"""
        return FieldNameNormalizer.normalize(label)


# Exemplos
normalizer = FieldNameNormalizer()

print(normalizer.normalize("Raça/Cor"))           # raca_cor
print(normalizer.normalize("raça"))               # raca
print(normalizer.normalize("Raça"))               # raca
print(normalizer.normalize("Data de Nascimento")) # data_de_nascimento
print(normalizer.normalize("data_nascimento"))    # data_nascimento
print(normalizer.normalize("Data-Nascimento"))    # data_nascimento
```

### Validação no Backend

```python
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

@router.post("/campos-customizados")
def create_campo_customizado(data: Dict[str, Any]):
    """Criar campo customizado com validação de duplicatas"""
    
    entidade = data['entidade']
    nome = data['nome']
    label = data['label']
    
    # Normalizar nome
    normalizer = FieldNameNormalizer()
    nome_normalizado = normalizer.normalize(nome)
    slug = normalizer.generate_slug(label)
    
    # Verificar se já existe campo com nome normalizado similar
    campo_existente = db.session.query(DefinicaoCampoCustomizado).filter(
        DefinicaoCampoCustomizado.entidade == entidade,
        DefinicaoCampoCustomizado.nome_normalizado == nome_normalizado
    ).first()
    
    if campo_existente:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "Campo duplicado",
                "message": f"Já existe um campo similar: '{campo_existente.configuracao['label']}'",
                "campo_existente": {
                    "id": campo_existente.id,
                    "nome": campo_existente.nome,
                    "label": campo_existente.configuracao['label']
                }
            }
        )
    
    # Criar campo
    novo_campo = DefinicaoCampoCustomizado(
        entidade=entidade,
        nome=nome,
        nome_normalizado=nome_normalizado,
        slug=slug,
        configuracao=data['configuracao']
    )
    
    try:
        db.session.add(novo_campo)
        db.session.commit()
        return {"id": novo_campo.id, "message": "Campo criado com sucesso"}
    except IntegrityError:
        db.session.rollback()
        raise HTTPException(status_code=409, detail="Campo duplicado")
```

---

## Estratégia 2: Detecção de Similaridade (Fuzzy Matching)

### Usando Distância de Levenshtein

```python
from difflib import SequenceMatcher

class FieldSimilarityDetector:
    """Detecta campos similares usando algoritmos de similaridade"""
    
    @staticmethod
    def similarity_ratio(str1: str, str2: str) -> float:
        """
        Calcula similaridade entre duas strings (0.0 a 1.0)
        1.0 = idênticas, 0.0 = completamente diferentes
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    @staticmethod
    def levenshtein_distance(str1: str, str2: str) -> int:
        """Calcula distância de Levenshtein (número de edições necessárias)"""
        if len(str1) < len(str2):
            return FieldSimilarityDetector.levenshtein_distance(str2, str1)
        
        if len(str2) == 0:
            return len(str1)
        
        previous_row = range(len(str2) + 1)
        for i, c1 in enumerate(str1):
            current_row = [i + 1]
            for j, c2 in enumerate(str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def find_similar_fields(
        new_field_name: str, 
        existing_fields: List[Dict], 
        threshold: float = 0.8
    ) -> List[Dict]:
        """
        Encontra campos similares acima do threshold
        
        Args:
            new_field_name: Nome do novo campo
            existing_fields: Lista de campos existentes
            threshold: Limite de similaridade (0.0 a 1.0)
        
        Returns:
            Lista de campos similares com score de similaridade
        """
        similar_fields = []
        
        for field in existing_fields:
            # Comparar com nome normalizado
            similarity = FieldSimilarityDetector.similarity_ratio(
                new_field_name, 
                field['nome_normalizado']
            )
            
            if similarity >= threshold:
                similar_fields.append({
                    **field,
                    'similarity_score': similarity
                })
            
            # Também comparar com label
            label_similarity = FieldSimilarityDetector.similarity_ratio(
                new_field_name,
                field['label']
            )
            
            if label_similarity >= threshold and label_similarity > similarity:
                # Atualizar se similaridade com label for maior
                similar_fields.append({
                    **field,
                    'similarity_score': label_similarity
                })
        
        # Ordenar por similaridade (maior primeiro)
        similar_fields.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Remover duplicatas
        seen = set()
        unique_similar = []
        for field in similar_fields:
            if field['id'] not in seen:
                seen.add(field['id'])
                unique_similar.append(field)
        
        return unique_similar


# Uso no endpoint
@router.post("/campos-customizados/validar")
def validate_campo_nome(data: Dict[str, Any]):
    """Validar se nome do campo é similar a campos existentes"""
    
    entidade = data['entidade']
    nome = data['nome']
    label = data.get('label', nome)
    
    # Normalizar
    normalizer = FieldNameNormalizer()
    nome_normalizado = normalizer.normalize(nome)
    label_normalizado = normalizer.normalize(label)
    
    # Buscar campos existentes
    campos_existentes = db.session.query(DefinicaoCampoCustomizado).filter_by(
        entidade=entidade,
        ativo=True
    ).all()
    
    existing_fields_data = [
        {
            'id': c.id,
            'nome': c.nome,
            'nome_normalizado': c.nome_normalizado,
            'label': c.configuracao.get('label', c.nome)
        }
        for c in campos_existentes
    ]
    
    # Detectar campos similares
    detector = FieldSimilarityDetector()
    
    # Verificar similaridade com nome
    similar_by_name = detector.find_similar_fields(
        nome_normalizado, 
        existing_fields_data, 
        threshold=0.8
    )
    
    # Verificar similaridade com label
    similar_by_label = detector.find_similar_fields(
        label_normalizado,
        existing_fields_data,
        threshold=0.8
    )
    
    # Combinar resultados
    all_similar = similar_by_name + similar_by_label
    
    # Remover duplicatas e ordenar
    seen = set()
    unique_similar = []
    for field in all_similar:
        if field['id'] not in seen:
            seen.add(field['id'])
            unique_similar.append(field)
    
    unique_similar.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return {
        "nome_normalizado": nome_normalizado,
        "is_duplicate": len(unique_similar) > 0,
        "similar_fields": unique_similar[:5]  # Top 5 mais similares
    }
```

---

## Estratégia 3: Categorização de Campos (Taxonomia)

### Definir Categorias Padrão

```sql
-- Tabela de categorias
CREATE TABLE categoria_campo (
    id BIGSERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    icone VARCHAR(50),
    ordem INTEGER DEFAULT 0
);

-- Adicionar categoria aos campos
ALTER TABLE definicao_campo_customizado 
ADD COLUMN categoria_id BIGINT REFERENCES categoria_campo(id);

-- Inserir categorias padrão
INSERT INTO categoria_campo (nome, descricao, icone, ordem) VALUES
('Identificação', 'Dados de identificação pessoal', 'id-card', 1),
('Demográfico', 'Dados demográficos (sexo, raça, idade)', 'users', 2),
('Contato', 'Informações de contato', 'phone', 3),
('Endereço', 'Dados de localização', 'map-pin', 4),
('Profissional', 'Informações profissionais', 'briefcase', 5),
('Financeiro', 'Dados financeiros', 'dollar-sign', 6),
('Educacional', 'Informações educacionais', 'graduation-cap', 7),
('Saúde', 'Dados de saúde', 'heart', 8),
('Outros', 'Campos diversos', 'more-horizontal', 99);
```

### Campos Padrão por Categoria

```python
# Definir campos padrão para evitar duplicatas
CAMPOS_PADRAO = {
    'Demográfico': [
        {
            'nome': 'sexo',
            'label': 'Sexo',
            'tipo': 'radio',
            'opcoes': ['Masculino', 'Feminino', 'Outro', 'Prefiro não informar']
        },
        {
            'nome': 'raca_cor',
            'label': 'Raça/Cor',
            'tipo': 'checkbox_group',
            'permite_multiplos': True,
            'opcoes': ['Branca', 'Preta', 'Parda', 'Amarela', 'Indígena']
        },
        {
            'nome': 'data_nascimento',
            'label': 'Data de Nascimento',
            'tipo': 'date'
        },
        {
            'nome': 'estado_civil',
            'label': 'Estado Civil',
            'tipo': 'select',
            'opcoes': ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)']
        }
    ],
    'Contato': [
        {
            'nome': 'telefone_celular',
            'label': 'Telefone Celular',
            'tipo': 'phone'
        },
        {
            'nome': 'telefone_fixo',
            'label': 'Telefone Fixo',
            'tipo': 'phone'
        },
        {
            'nome': 'email_pessoal',
            'label': 'Email Pessoal',
            'tipo': 'email'
        }
    ],
    'Profissional': [
        {
            'nome': 'profissao',
            'label': 'Profissão',
            'tipo': 'text'
        },
        {
            'nome': 'empresa',
            'label': 'Empresa',
            'tipo': 'text'
        },
        {
            'nome': 'cargo',
            'label': 'Cargo',
            'tipo': 'text'
        }
    ]
}

@router.get("/campos-customizados/sugestoes")
def get_campo_sugestoes(entidade: str, categoria: str):
    """Retorna sugestões de campos padrão por categoria"""
    
    # Buscar campos já criados nesta categoria
    campos_existentes = db.session.query(DefinicaoCampoCustomizado).join(
        CategoriaField
    ).filter(
        DefinicaoCampoCustomizado.entidade == entidade,
        CategoriaField.nome == categoria,
        DefinicaoCampoCustomizado.ativo == True
    ).all()
    
    nomes_existentes = {c.nome_normalizado for c in campos_existentes}
    
    # Filtrar sugestões (remover campos já criados)
    sugestoes = CAMPOS_PADRAO.get(categoria, [])
    normalizer = FieldNameNormalizer()
    
    sugestoes_disponiveis = [
        s for s in sugestoes 
        if normalizer.normalize(s['nome']) not in nomes_existentes
    ]
    
    return {
        "categoria": categoria,
        "sugestoes": sugestoes_disponiveis,
        "campos_existentes": [
            {
                "nome": c.nome,
                "label": c.configuracao.get('label')
            }
            for c in campos_existentes
        ]
    }
```

---

## Estratégia 4: Workflow de Aprovação

### Adicionar Status de Aprovação

```sql
-- Adicionar status de aprovação
ALTER TABLE definicao_campo_customizado 
ADD COLUMN status VARCHAR(20) DEFAULT 'pendente',
ADD COLUMN criado_por BIGINT REFERENCES usuario(id),
ADD COLUMN aprovado_por BIGINT REFERENCES usuario(id),
ADD COLUMN aprovado_em TIMESTAMP;

-- Constraint de check
ALTER TABLE definicao_campo_customizado
ADD CONSTRAINT check_status 
CHECK (status IN ('pendente', 'aprovado', 'rejeitado'));

-- Apenas campos aprovados são usados
CREATE INDEX idx_campo_status_ativo 
ON definicao_campo_customizado(entidade, status, ativo)
WHERE status = 'aprovado' AND ativo = true;
```

### Endpoint de Aprovação

```python
@router.post("/campos-customizados/{campo_id}/aprovar")
def aprovar_campo(campo_id: int, current_user: Usuario = Depends(get_current_admin)):
    """Aprovar campo customizado (apenas administradores)"""
    
    campo = db.session.query(DefinicaoCampoCustomizado).get(campo_id)
    
    if not campo:
        raise HTTPException(status_code=404, detail="Campo não encontrado")
    
    if campo.status == 'aprovado':
        raise HTTPException(status_code=400, detail="Campo já aprovado")
    
    # Verificar duplicatas antes de aprovar
    normalizer = FieldNameNormalizer()
    nome_normalizado = normalizer.normalize(campo.nome)
    
    duplicata = db.session.query(DefinicaoCampoCustomizado).filter(
        DefinicaoCampoCustomizado.id != campo_id,
        DefinicaoCampoCustomizado.entidade == campo.entidade,
        DefinicaoCampoCustomizado.nome_normalizado == nome_normalizado,
        DefinicaoCampoCustomizado.status == 'aprovado'
    ).first()
    
    if duplicata:
        raise HTTPException(
            status_code=409,
            detail=f"Campo duplicado: '{duplicata.configuracao['label']}' já existe"
        )
    
    # Aprovar
    campo.status = 'aprovado'
    campo.aprovado_por = current_user.id
    campo.aprovado_em = datetime.now()
    
    db.session.commit()
    
    return {"message": "Campo aprovado com sucesso"}


@router.post("/campos-customizados/{campo_id}/rejeitar")
def rejeitar_campo(
    campo_id: int, 
    motivo: str,
    current_user: Usuario = Depends(get_current_admin)
):
    """Rejeitar campo customizado"""
    
    campo = db.session.query(DefinicaoCampoCustomizado).get(campo_id)
    
    if not campo:
        raise HTTPException(status_code=404, detail="Campo não encontrado")
    
    campo.status = 'rejeitado'
    campo.configuracao['motivo_rejeicao'] = motivo
    
    db.session.commit()
    
    return {"message": "Campo rejeitado"}
```

---

## Estratégia 5: Interface com Sugestões Inteligentes

### Frontend: Validação em Tempo Real

```vue
<template>
  <div class="campo-form">
    <h2>Criar Novo Campo Customizado</h2>
    
    <!-- Seletor de Categoria -->
    <div class="form-group">
      <label>Categoria</label>
      <select v-model="categoria" @change="loadSugestoes">
        <option value="">Selecione uma categoria</option>
        <option v-for="cat in categorias" :key="cat.id" :value="cat.nome">
          {{ cat.nome }}
        </option>
      </select>
    </div>
    
    <!-- Sugestões de Campos Padrão -->
    <div v-if="sugestoes.length > 0" class="sugestoes-box">
      <h3>💡 Campos Sugeridos</h3>
      <p>Esses campos já estão prontos para uso:</p>
      <div class="sugestoes-list">
        <button 
          v-for="sug in sugestoes" 
          :key="sug.nome"
          @click="usarSugestao(sug)"
          class="sugestao-btn"
        >
          <strong>{{ sug.label }}</strong>
          <span class="tipo-badge">{{ sug.tipo }}</span>
        </button>
      </div>
    </div>
    
    <!-- Nome do Campo -->
    <div class="form-group">
      <label>Nome do Campo</label>
      <input 
        v-model="nome" 
        @input="checkSimilarity"
        placeholder="Ex: raca_cor"
      />
      <small>Use snake_case (letras minúsculas e underscore)</small>
    </div>
    
    <!-- Label do Campo -->
    <div class="form-group">
      <label>Label (Rótulo)</label>
      <input 
        v-model="label" 
        @input="checkSimilarity"
        placeholder="Ex: Raça/Cor"
      />
    </div>
    
    <!-- Alerta de Campos Similares -->
    <div v-if="camposSimilares.length > 0" class="alert alert-warning">
      <h4>⚠️ Campos Similares Encontrados</h4>
      <p>Já existem campos parecidos. Você realmente precisa criar um novo?</p>
      <ul>
        <li v-for="similar in camposSimilares" :key="similar.id">
          <strong>{{ similar.label }}</strong> 
          ({{ (similar.similarity_score * 100).toFixed(0) }}% similar)
          <button @click="usarCampoExistente(similar)" class="btn-link">
            Usar este campo
          </button>
        </li>
      </ul>
    </div>
    
    <!-- Tipo do Campo -->
    <div class="form-group">
      <label>Tipo do Campo</label>
      <select v-model="tipo">
        <option value="text">Texto</option>
        <option value="number">Número</option>
        <option value="email">Email</option>
        <option value="date">Data</option>
        <option value="radio">Seleção Única (Radio)</option>
        <option value="select">Seleção Única (Dropdown)</option>
        <option value="checkbox_group">Múltipla Seleção (Checkboxes)</option>
        <option value="multiselect">Múltipla Seleção (Dropdown)</option>
      </select>
    </div>
    
    <!-- Botões -->
    <div class="form-actions">
      <button @click="salvar" :disabled="camposSimilares.length > 0 && !confirmarDuplicata">
        Criar Campo
      </button>
      
      <label v-if="camposSimilares.length > 0">
        <input type="checkbox" v-model="confirmarDuplicata" />
        Confirmo que preciso criar este campo mesmo com similares existentes
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { debounce } from 'lodash';

const categoria = ref('');
const nome = ref('');
const label = ref('');
const tipo = ref('text');
const categorias = ref([]);
const sugestoes = ref([]);
const camposSimilares = ref([]);
const confirmarDuplicata = ref(false);

const loadCategorias = async () => {
  const response = await fetch('/api/categorias-campo');
  categorias.value = await response.json();
};

const loadSugestoes = async () => {
  if (!categoria.value) return;
  
  const response = await fetch(
    `/api/campos-customizados/sugestoes?entidade=pessoa&categoria=${categoria.value}`
  );
  const data = await response.json();
  sugestoes.value = data.sugestoes;
};

const checkSimilarity = debounce(async () => {
  if (!nome.value && !label.value) {
    camposSimilares.value = [];
    return;
  }
  
  const response = await fetch('/api/campos-customizados/validar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      entidade: 'pessoa',
      nome: nome.value,
      label: label.value
    })
  });
  
  const data = await response.json();
  camposSimilares.value = data.similar_fields || [];
  confirmarDuplicata.value = false;
}, 500);

const usarSugestao = (sugestao) => {
  nome.value = sugestao.nome;
  label.value = sugestao.label;
  tipo.value = sugestao.tipo;
  checkSimilarity();
};

const usarCampoExistente = (campo) => {
  alert(`Redirecionando para editar o campo "${campo.label}"`);
  // Redirecionar para página de edição
};

const salvar = async () => {
  // Implementar salvamento
  console.log('Salvando campo:', { nome, label, tipo });
};

onMounted(() => {
  loadCategorias();
});
</script>
```

---

## Resumo das Estratégias

| Estratégia | Eficácia | Complexidade | Quando Usar |
|------------|----------|--------------|-------------|
| **1. Normalização** | ⭐⭐⭐⭐⭐ | Baixa | Sempre! Base essencial |
| **2. Fuzzy Matching** | ⭐⭐⭐⭐ | Média | Detecção inteligente |
| **3. Categorização** | ⭐⭐⭐⭐ | Média | Organização e sugestões |
| **4. Workflow Aprovação** | ⭐⭐⭐⭐⭐ | Alta | Ambientes corporativos |
| **5. Interface Inteligente** | ⭐⭐⭐⭐⭐ | Média | Melhor UX |

---

## Recomendação Final

### Implementação em Camadas

**Camada 1 (Essencial):**
✅ Normalização de nomes (snake_case, sem acentos)  
✅ Constraint UNIQUE no banco de dados  
✅ Validação básica no backend  

**Camada 2 (Recomendado):**
✅ Detecção de similaridade (fuzzy matching)  
✅ Sugestões de campos padrão por categoria  
✅ Alerta visual no frontend  

**Camada 3 (Avançado):**
✅ Workflow de aprovação para administradores  
✅ Taxonomia completa de campos  
✅ Auditoria e histórico de mudanças  

Esta abordagem **multicamadas** garante qualidade de dados sem frustrar usuários! 🎯
