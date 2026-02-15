---
description: Aplicar TDD (Red-Green-Refactor) em desenvolvimento
---

# Workflow: TDD (Test-Driven Development)

Aplique TDD em qualquer desenvolvimento seguindo este ciclo.

## 🔴 Red - Escrever Teste que Falha

### Backend (Python + pytest)

```python
# backend/tests/test_feature.py
def test_should_do_something():
    # Arrange
    input_data = "test"
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == "expected"
```

### Frontend (Vue + Vitest)

```javascript
// frontend/tests/Component.spec.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Component from '@/components/Component.vue'

describe('Component', () => {
  it('should render correctly', () => {
    const wrapper = mount(Component)
    expect(wrapper.text()).toContain('Expected Text')
  })
})
```

// turbo
Executar testes:
```bash
# Backend
cd backend && pytest

# Frontend  
cd frontend && npm run test
```

## 🟢 Green - Fazer Teste Passar

Implemente **apenas** o código necessário para o teste passar.

Não adicione funcionalidades extras!

// turbo
Executar testes novamente:
```bash
pytest  # ou npm run test
```

## 🔵 Refactor - Melhorar Código

Agora que os testes passam, melhore:

- ✅ Remover duplicação
- ✅ Aplicar SOLID
- ✅ Melhorar nomes
- ✅ Adicionar documentação

// turbo
Executar testes após refatoração:
```bash
pytest  # ou npm run test
```

## Commit

```bash
git commit -m "test(scope): add test for feature"
git commit -m "feat(scope): implement feature"
git commit -m "refactor(scope): improve code quality"
```

## Repetir

Volte ao **Red** para a próxima funcionalidade!
