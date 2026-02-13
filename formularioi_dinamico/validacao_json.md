# Validação com Regras em JSON (Opção 2 - JSONB)

## Visão Geral

Na **Opção 2 (JSONB)**, você pode armazenar **todas as regras de validação dentro do próprio JSON**, incluindo:
- Obrigatoriedade
- Tamanho mínimo/máximo
- Padrões (regex)
- Valores permitidos
- Validações customizadas
- Mensagens de erro personalizadas

---

## Estrutura do JSON de Validação

### Tabela de Definição de Campos

```sql
CREATE TABLE definicao_campo_customizado (
    id BIGSERIAL PRIMARY KEY,
    entidade VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    configuracao JSONB NOT NULL, -- ✨ Toda a configuração em JSON!
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entidade, nome)
);

-- Índice GIN para queries eficientes
CREATE INDEX idx_definicao_campo_config ON definicao_campo_customizado USING GIN (configuracao);
CREATE INDEX idx_definicao_campo_entidade ON definicao_campo_customizado(entidade, ativo);
```

### Estrutura Completa do JSON de Configuração

```json
{
  "label": "Nome do Campo",
  "tipo": "text",
  "ordem": 1,
  "descricao": "Texto de ajuda para o usuário",
  "placeholder": "Digite aqui...",
  "permite_multiplos": false,
  "opcoes": ["Opção 1", "Opção 2", "Opção 3"],
  
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Este campo é obrigatório",
    
    "min": 3,
    "mensagem_min": "Mínimo de 3 caracteres",
    
    "max": 100,
    "mensagem_max": "Máximo de 100 caracteres",
    
    "pattern": "^[A-Za-zÀ-ÿ\\s]+$",
    "mensagem_pattern": "Apenas letras são permitidas",
    
    "min_value": 0,
    "max_value": 150,
    "mensagem_range": "Valor deve estar entre 0 e 150",
    
    "email": true,
    "mensagem_email": "Email inválido",
    
    "cpf": true,
    "mensagem_cpf": "CPF inválido",
    
    "url": true,
    "mensagem_url": "URL inválida",
    
    "custom": {
      "validator": "validar_idade_minima",
      "params": {"idade_minima": 18},
      "mensagem": "Idade mínima: 18 anos"
    }
  },
  
  "condicional": {
    "campo": "estado_civil",
    "operador": "equals",
    "valor": "Casado(a)",
    "acao": "show"
  }
}
```

---

## Exemplos de Campos com Validação

### Exemplo 1: Campo de Texto Simples (Nome)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'nome_completo', '{
  "label": "Nome Completo",
  "tipo": "text",
  "ordem": 1,
  "placeholder": "Digite seu nome completo",
  "descricao": "Informe seu nome completo como consta no documento",
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Nome completo é obrigatório",
    "min": 3,
    "mensagem_min": "Nome deve ter no mínimo 3 caracteres",
    "max": 200,
    "mensagem_max": "Nome deve ter no máximo 200 caracteres",
    "pattern": "^[A-Za-zÀ-ÿ\\s]+$",
    "mensagem_pattern": "Nome deve conter apenas letras"
  }
}'::jsonb);
```

### Exemplo 2: Campo de Email

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'email_profissional', '{
  "label": "Email Profissional",
  "tipo": "email",
  "ordem": 2,
  "placeholder": "seuemail@empresa.com",
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Email profissional é obrigatório",
    "email": true,
    "mensagem_email": "Digite um email válido",
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
    "mensagem_pattern": "Email deve ter formato válido"
  }
}'::jsonb);
```

### Exemplo 3: Campo Numérico (Idade)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'idade', '{
  "label": "Idade",
  "tipo": "number",
  "ordem": 3,
  "placeholder": "Digite sua idade",
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Idade é obrigatória",
    "min_value": 0,
    "max_value": 150,
    "mensagem_range": "Idade deve estar entre 0 e 150 anos"
  }
}'::jsonb);
```

### Exemplo 4: Campo de Seleção Única (Sexo)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'sexo', '{
  "label": "Sexo",
  "tipo": "radio",
  "ordem": 4,
  "opcoes": ["Masculino", "Feminino", "Outro", "Prefiro não informar"],
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Sexo é obrigatório",
    "in": ["Masculino", "Feminino", "Outro", "Prefiro não informar"],
    "mensagem_in": "Selecione uma opção válida"
  }
}'::jsonb);
```

### Exemplo 5: Campo Multivalorado (Raça/Cor)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'raca_cor', '{
  "label": "Raça/Cor (autodeclaração)",
  "tipo": "checkbox_group",
  "ordem": 5,
  "permite_multiplos": true,
  "opcoes": ["Branca", "Preta", "Parda", "Amarela", "Indígena"],
  "descricao": "Você pode selecionar mais de uma opção",
  "validacao": {
    "obrigatorio": false,
    "min_items": 1,
    "mensagem_min_items": "Selecione pelo menos uma opção",
    "max_items": 5,
    "mensagem_max_items": "Selecione no máximo 5 opções",
    "in": ["Branca", "Preta", "Parda", "Amarela", "Indígena"],
    "mensagem_in": "Selecione apenas opções válidas"
  }
}'::jsonb);
```

### Exemplo 6: Campo de CPF

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'cpf', '{
  "label": "CPF",
  "tipo": "cpf",
  "ordem": 6,
  "placeholder": "000.000.000-00",
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "CPF é obrigatório",
    "cpf": true,
    "mensagem_cpf": "CPF inválido",
    "pattern": "^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$",
    "mensagem_pattern": "CPF deve estar no formato 000.000.000-00"
  }
}'::jsonb);
```

### Exemplo 7: Campo de Data de Nascimento

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'data_nascimento', '{
  "label": "Data de Nascimento",
  "tipo": "date",
  "ordem": 7,
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Data de nascimento é obrigatória",
    "min_date": "1900-01-01",
    "max_date": "today",
    "mensagem_range": "Data deve estar entre 01/01/1900 e hoje",
    "custom": {
      "validator": "validar_idade_minima",
      "params": {"idade_minima": 18},
      "mensagem": "Você deve ter pelo menos 18 anos"
    }
  }
}'::jsonb);
```

### Exemplo 8: Campo Condicional (Nome do Cônjuge)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'nome_conjuge', '{
  "label": "Nome do Cônjuge",
  "tipo": "text",
  "ordem": 8,
  "placeholder": "Digite o nome do cônjuge",
  "condicional": {
    "campo": "estado_civil",
    "operador": "equals",
    "valor": "Casado(a)",
    "acao": "show"
  },
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Nome do cônjuge é obrigatório para pessoas casadas",
    "min": 3,
    "max": 200
  }
}'::jsonb);
```

### Exemplo 9: Campo de Telefone

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'telefone_celular', '{
  "label": "Telefone Celular",
  "tipo": "phone",
  "ordem": 9,
  "placeholder": "(00) 00000-0000",
  "validacao": {
    "obrigatorio": true,
    "mensagem_obrigatorio": "Telefone celular é obrigatório",
    "pattern": "^\\(\\d{2}\\) \\d{5}-\\d{4}$",
    "mensagem_pattern": "Telefone deve estar no formato (00) 00000-0000"
  }
}'::jsonb);
```

### Exemplo 10: Campo de Salário (Moeda)

```sql
INSERT INTO definicao_campo_customizado (entidade, nome, configuracao)
VALUES ('pessoa', 'salario', '{
  "label": "Salário",
  "tipo": "currency",
  "ordem": 10,
  "placeholder": "R$ 0,00",
  "validacao": {
    "obrigatorio": false,
    "min_value": 0,
    "max_value": 1000000,
    "mensagem_range": "Salário deve estar entre R$ 0,00 e R$ 1.000.000,00"
  }
}'::jsonb);
```

---

## Motor de Validação Backend (Python)

### Validador Genérico

```python
from typing import Any, Dict, List, Optional
import re
from datetime import datetime, date
from validate_docbr import CPF, CNPJ

class DynamicFieldValidator:
    """Motor de validação baseado em regras JSON"""
    
    def __init__(self):
        self.cpf_validator = CPF()
        self.cnpj_validator = CNPJ()
    
    def validate_field(
        self, 
        field_config: Dict[str, Any], 
        value: Any,
        all_values: Dict[str, Any] = None
    ) -> List[str]:
        """
        Valida um campo baseado em sua configuração JSON
        
        Args:
            field_config: Configuração do campo (JSON)
            value: Valor a ser validado
            all_values: Todos os valores do formulário (para validações condicionais)
        
        Returns:
            Lista de mensagens de erro (vazia se válido)
        """
        errors = []
        validacao = field_config.get('validacao', {})
        
        # Verificar se campo é condicional
        if not self._is_field_visible(field_config, all_values):
            return []  # Campo não visível, não validar
        
        # Validar obrigatoriedade
        if validacao.get('obrigatorio') and not value:
            errors.append(
                validacao.get('mensagem_obrigatorio', f"{field_config['label']} é obrigatório")
            )
            return errors  # Se obrigatório e vazio, retornar imediatamente
        
        # Se não obrigatório e vazio, não validar outros campos
        if not value:
            return []
        
        # Validar tipo específico
        tipo = field_config.get('tipo')
        
        if tipo == 'text' or tipo == 'textarea':
            errors.extend(self._validate_text(value, validacao))
        
        elif tipo == 'number' or tipo == 'currency':
            errors.extend(self._validate_number(value, validacao))
        
        elif tipo == 'email':
            errors.extend(self._validate_email(value, validacao))
        
        elif tipo == 'cpf':
            errors.extend(self._validate_cpf(value, validacao))
        
        elif tipo == 'cnpj':
            errors.extend(self._validate_cnpj(value, validacao))
        
        elif tipo == 'phone':
            errors.extend(self._validate_phone(value, validacao))
        
        elif tipo == 'date':
            errors.extend(self._validate_date(value, validacao))
        
        elif tipo == 'url':
            errors.extend(self._validate_url(value, validacao))
        
        elif tipo in ['select', 'radio']:
            errors.extend(self._validate_select(value, validacao, field_config.get('opcoes', [])))
        
        elif tipo in ['multiselect', 'checkbox_group', 'tags']:
            errors.extend(self._validate_multiselect(value, validacao, field_config.get('opcoes', [])))
        
        # Validação customizada
        if validacao.get('custom'):
            errors.extend(self._validate_custom(value, validacao['custom'], all_values))
        
        return errors
    
    def _is_field_visible(self, field_config: Dict, all_values: Dict) -> bool:
        """Verifica se campo é visível baseado em condições"""
        condicional = field_config.get('condicional')
        if not condicional or not all_values:
            return True
        
        campo_ref = condicional.get('campo')
        operador = condicional.get('operador')
        valor_esperado = condicional.get('valor')
        valor_atual = all_values.get(campo_ref)
        
        if operador == 'equals':
            is_condition_met = valor_atual == valor_esperado
        elif operador == 'not_equals':
            is_condition_met = valor_atual != valor_esperado
        elif operador == 'in':
            is_condition_met = valor_atual in valor_esperado
        else:
            is_condition_met = True
        
        acao = condicional.get('acao', 'show')
        return is_condition_met if acao == 'show' else not is_condition_met
    
    def _validate_text(self, value: str, validacao: Dict) -> List[str]:
        """Valida campo de texto"""
        errors = []
        
        # Tamanho mínimo
        if 'min' in validacao and len(value) < validacao['min']:
            errors.append(
                validacao.get('mensagem_min', f"Mínimo de {validacao['min']} caracteres")
            )
        
        # Tamanho máximo
        if 'max' in validacao and len(value) > validacao['max']:
            errors.append(
                validacao.get('mensagem_max', f"Máximo de {validacao['max']} caracteres")
            )
        
        # Padrão (regex)
        if 'pattern' in validacao:
            if not re.match(validacao['pattern'], value):
                errors.append(
                    validacao.get('mensagem_pattern', "Formato inválido")
                )
        
        return errors
    
    def _validate_number(self, value: float, validacao: Dict) -> List[str]:
        """Valida campo numérico"""
        errors = []
        
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return ["Valor deve ser um número"]
        
        # Valor mínimo
        if 'min_value' in validacao and num_value < validacao['min_value']:
            errors.append(
                validacao.get('mensagem_range', f"Valor mínimo: {validacao['min_value']}")
            )
        
        # Valor máximo
        if 'max_value' in validacao and num_value > validacao['max_value']:
            errors.append(
                validacao.get('mensagem_range', f"Valor máximo: {validacao['max_value']}")
            )
        
        return errors
    
    def _validate_email(self, value: str, validacao: Dict) -> List[str]:
        """Valida email"""
        errors = []
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            errors.append(
                validacao.get('mensagem_email', "Email inválido")
            )
        
        return errors
    
    def _validate_cpf(self, value: str, validacao: Dict) -> List[str]:
        """Valida CPF"""
        errors = []
        
        # Remover formatação
        cpf_limpo = re.sub(r'\D', '', value)
        
        if not self.cpf_validator.validate(cpf_limpo):
            errors.append(
                validacao.get('mensagem_cpf', "CPF inválido")
            )
        
        return errors
    
    def _validate_cnpj(self, value: str, validacao: Dict) -> List[str]:
        """Valida CNPJ"""
        errors = []
        
        cnpj_limpo = re.sub(r'\D', '', value)
        
        if not self.cnpj_validator.validate(cnpj_limpo):
            errors.append(
                validacao.get('mensagem_cnpj', "CNPJ inválido")
            )
        
        return errors
    
    def _validate_phone(self, value: str, validacao: Dict) -> List[str]:
        """Valida telefone"""
        errors = []
        
        if 'pattern' in validacao:
            if not re.match(validacao['pattern'], value):
                errors.append(
                    validacao.get('mensagem_pattern', "Telefone inválido")
                )
        
        return errors
    
    def _validate_date(self, value: str, validacao: Dict) -> List[str]:
        """Valida data"""
        errors = []
        
        try:
            data_value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return ["Data inválida"]
        
        # Data mínima
        if 'min_date' in validacao:
            min_date_str = validacao['min_date']
            if min_date_str == 'today':
                min_date = date.today()
            else:
                min_date = datetime.strptime(min_date_str, '%Y-%m-%d').date()
            
            if data_value < min_date:
                errors.append(
                    validacao.get('mensagem_range', f"Data mínima: {min_date}")
                )
        
        # Data máxima
        if 'max_date' in validacao:
            max_date_str = validacao['max_date']
            if max_date_str == 'today':
                max_date = date.today()
            else:
                max_date = datetime.strptime(max_date_str, '%Y-%m-%d').date()
            
            if data_value > max_date:
                errors.append(
                    validacao.get('mensagem_range', f"Data máxima: {max_date}")
                )
        
        return errors
    
    def _validate_url(self, value: str, validacao: Dict) -> List[str]:
        """Valida URL"""
        errors = []
        
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, value):
            errors.append(
                validacao.get('mensagem_url', "URL inválida")
            )
        
        return errors
    
    def _validate_select(self, value: str, validacao: Dict, opcoes: List[str]) -> List[str]:
        """Valida campo de seleção única"""
        errors = []
        
        if 'in' in validacao:
            if value not in validacao['in']:
                errors.append(
                    validacao.get('mensagem_in', "Opção inválida")
                )
        elif opcoes and value not in opcoes:
            errors.append("Opção inválida")
        
        return errors
    
    def _validate_multiselect(self, value: List[str], validacao: Dict, opcoes: List[str]) -> List[str]:
        """Valida campo de seleção múltipla"""
        errors = []
        
        if not isinstance(value, list):
            return ["Valor deve ser uma lista"]
        
        # Mínimo de itens
        if 'min_items' in validacao and len(value) < validacao['min_items']:
            errors.append(
                validacao.get('mensagem_min_items', f"Selecione pelo menos {validacao['min_items']} opções")
            )
        
        # Máximo de itens
        if 'max_items' in validacao and len(value) > validacao['max_items']:
            errors.append(
                validacao.get('mensagem_max_items', f"Selecione no máximo {validacao['max_items']} opções")
            )
        
        # Validar cada item
        if 'in' in validacao:
            for item in value:
                if item not in validacao['in']:
                    errors.append(
                        validacao.get('mensagem_in', f"Opção inválida: {item}")
                    )
                    break
        elif opcoes:
            for item in value:
                if item not in opcoes:
                    errors.append(f"Opção inválida: {item}")
                    break
        
        return errors
    
    def _validate_custom(self, value: Any, custom_config: Dict, all_values: Dict) -> List[str]:
        """Executa validação customizada"""
        validator_name = custom_config.get('validator')
        params = custom_config.get('params', {})
        mensagem = custom_config.get('mensagem', "Validação customizada falhou")
        
        # Implementar validadores customizados aqui
        if validator_name == 'validar_idade_minima':
            return self._validar_idade_minima(value, params.get('idade_minima', 18), mensagem)
        
        return []
    
    def _validar_idade_minima(self, data_nascimento: str, idade_minima: int, mensagem: str) -> List[str]:
        """Validador customizado: idade mínima"""
        try:
            data_nasc = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            hoje = date.today()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            
            if idade < idade_minima:
                return [mensagem]
        except ValueError:
            return ["Data de nascimento inválida"]
        
        return []


# Uso no endpoint
@router.post("/pessoas")
def create_pessoa(data: Dict[str, Any]):
    """Criar pessoa com validação dinâmica"""
    
    # Carregar definições de campos
    campos_def = db.session.query(DefinicaoCampoCustomizado).filter_by(
        entidade='pessoa',
        ativo=True
    ).all()
    
    # Validar cada campo
    validator = DynamicFieldValidator()
    all_errors = {}
    
    campos_customizados = data.get('campos_customizados', {})
    
    for campo_def in campos_def:
        field_config = campo_def.configuracao
        field_name = campo_def.nome
        field_value = campos_customizados.get(field_name)
        
        errors = validator.validate_field(field_config, field_value, campos_customizados)
        if errors:
            all_errors[field_name] = errors
    
    if all_errors:
        raise HTTPException(status_code=400, detail=all_errors)
    
    # Criar pessoa
    nova_pessoa = Pessoa(
        nome=data['nome'],
        cpf=data['cpf'],
        email=data['email'],
        campos_customizados=campos_customizados
    )
    
    db.session.add(nova_pessoa)
    db.session.commit()
    
    return {"id": nova_pessoa.id, "message": "Pessoa criada com sucesso"}
```

---

## Validação Frontend (Vue.js)

```javascript
// composables/useFieldValidator.js
import { ref } from 'vue';

export function useFieldValidator() {
  const validateField = (fieldConfig, value, allValues = {}) => {
    const errors = [];
    const validacao = fieldConfig.validacao || {};
    
    // Verificar visibilidade condicional
    if (!isFieldVisible(fieldConfig, allValues)) {
      return [];
    }
    
    // Obrigatoriedade
    if (validacao.obrigatorio && !value) {
      errors.push(validacao.mensagem_obrigatorio || `${fieldConfig.label} é obrigatório`);
      return errors;
    }
    
    if (!value) return [];
    
    // Validações por tipo
    const tipo = fieldConfig.tipo;
    
    if (tipo === 'text' || tipo === 'textarea') {
      errors.push(...validateText(value, validacao));
    } else if (tipo === 'number' || tipo === 'currency') {
      errors.push(...validateNumber(value, validacao));
    } else if (tipo === 'email') {
      errors.push(...validateEmail(value, validacao));
    } else if (tipo === 'cpf') {
      errors.push(...validateCPF(value, validacao));
    } else if (tipo === 'date') {
      errors.push(...validateDate(value, validacao));
    } else if (tipo === 'multiselect' || tipo === 'checkbox_group') {
      errors.push(...validateMultiselect(value, validacao, fieldConfig.opcoes));
    }
    
    return errors;
  };
  
  const isFieldVisible = (fieldConfig, allValues) => {
    const condicional = fieldConfig.condicional;
    if (!condicional) return true;
    
    const valorAtual = allValues[condicional.campo];
    let conditionMet = false;
    
    if (condicional.operador === 'equals') {
      conditionMet = valorAtual === condicional.valor;
    } else if (condicional.operador === 'not_equals') {
      conditionMet = valorAtual !== condicional.valor;
    }
    
    return condicional.acao === 'show' ? conditionMet : !conditionMet;
  };
  
  const validateText = (value, validacao) => {
    const errors = [];
    
    if (validacao.min && value.length < validacao.min) {
      errors.push(validacao.mensagem_min || `Mínimo de ${validacao.min} caracteres`);
    }
    
    if (validacao.max && value.length > validacao.max) {
      errors.push(validacao.mensagem_max || `Máximo de ${validacao.max} caracteres`);
    }
    
    if (validacao.pattern && !new RegExp(validacao.pattern).test(value)) {
      errors.push(validacao.mensagem_pattern || 'Formato inválido');
    }
    
    return errors;
  };
  
  const validateNumber = (value, validacao) => {
    const errors = [];
    const numValue = parseFloat(value);
    
    if (isNaN(numValue)) {
      return ['Valor deve ser um número'];
    }
    
    if (validacao.min_value !== undefined && numValue < validacao.min_value) {
      errors.push(validacao.mensagem_range || `Valor mínimo: ${validacao.min_value}`);
    }
    
    if (validacao.max_value !== undefined && numValue > validacao.max_value) {
      errors.push(validacao.mensagem_range || `Valor máximo: ${validacao.max_value}`);
    }
    
    return errors;
  };
  
  const validateEmail = (value, validacao) => {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailPattern.test(value)) {
      return [validacao.mensagem_email || 'Email inválido'];
    }
    return [];
  };
  
  const validateCPF = (value, validacao) => {
    // Implementar validação de CPF
    const cpfLimpo = value.replace(/\D/g, '');
    if (cpfLimpo.length !== 11) {
      return [validacao.mensagem_cpf || 'CPF inválido'];
    }
    // Adicionar validação completa de CPF aqui
    return [];
  };
  
  const validateDate = (value, validacao) => {
    const errors = [];
    const dataValue = new Date(value);
    
    if (isNaN(dataValue.getTime())) {
      return ['Data inválida'];
    }
    
    if (validacao.min_date) {
      const minDate = validacao.min_date === 'today' ? new Date() : new Date(validacao.min_date);
      if (dataValue < minDate) {
        errors.push(validacao.mensagem_range || `Data mínima: ${minDate.toLocaleDateString()}`);
      }
    }
    
    if (validacao.max_date) {
      const maxDate = validacao.max_date === 'today' ? new Date() : new Date(validacao.max_date);
      if (dataValue > maxDate) {
        errors.push(validacao.mensagem_range || `Data máxima: ${maxDate.toLocaleDateString()}`);
      }
    }
    
    return errors;
  };
  
  const validateMultiselect = (value, validacao, opcoes) => {
    const errors = [];
    
    if (!Array.isArray(value)) {
      return ['Valor deve ser uma lista'];
    }
    
    if (validacao.min_items && value.length < validacao.min_items) {
      errors.push(validacao.mensagem_min_items || `Selecione pelo menos ${validacao.min_items} opções`);
    }
    
    if (validacao.max_items && value.length > validacao.max_items) {
      errors.push(validacao.mensagem_max_items || `Selecione no máximo ${validacao.max_items} opções`);
    }
    
    return errors;
  };
  
  return {
    validateField,
    isFieldVisible
  };
}
```

---

## Resumo

### ✅ Vantagens de Validação em JSON

1. **Flexibilidade Total** - Adicione/modifique regras sem alterar código
2. **Mensagens Personalizadas** - Cada regra pode ter sua própria mensagem
3. **Validações Condicionais** - Campos aparecem/desaparecem baseado em outros
4. **Extensível** - Fácil adicionar novos tipos de validação
5. **Portável** - Mesma configuração funciona em frontend e backend

### 📋 Tipos de Validação Suportados

- ✅ Obrigatoriedade
- ✅ Tamanho mínimo/máximo (texto)
- ✅ Valor mínimo/máximo (número)
- ✅ Padrão regex
- ✅ Email
- ✅ CPF/CNPJ
- ✅ Telefone
- ✅ URL
- ✅ Data (com min/max)
- ✅ Seleção (valores permitidos)
- ✅ Multiseleção (min/max itens)
- ✅ Validações customizadas
- ✅ Validações condicionais

Esta abordagem oferece **máxima flexibilidade** mantendo **total controle** sobre as regras de validação! 🎯
