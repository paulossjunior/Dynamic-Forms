# Arquitetura de Formulários Dinâmicos

Este diretório contém a documentação completa para a implementação de um sistema de formulários dinâmicos integrado a bancos de dados relacionais (Pessoa/Endereço).

## 🗂️ Índice de Documentos

Abaixo estão os links e descrições para cada parte da arquitetura:

1.  **[Documentação Técnica Principal](documentacao_tecnica.md)**
    *   O guia mestre com a especificação formal: DDL do banco (PostgreSQL), contratos de API e lógica do motor de validação.

2.  **[Resumo Executivo para Compartilhamento](resumo_arquitetura_final.md)**
    *   Um resumo conciso de toda a conversa e decisões de design. Perfeito para explicar a solução rapidamente para colegas.

3.  **[Plano de Implementação Original](implementation_plan.md)**
    *   A proposta inicial detalhando as três abordagens consideradas: EAV, JSONB e a abordagem Híbrida (Recomendada).

4.  **[Tratamento de Campos Multivalorados](campos_multivalorados.md)**
    *   Especificação detalhada para campos como Raça, Cor e Sexo. Explica como gerenciar seleções múltiplas no banco e na UI.

5.  **[Guia de Validação via JSON](validacao_json.md)**
    *   Como embutir regras complexas (CPF, Email, Regex, Datas) diretamente no JSON de configuração para que o sistema valide automaticamente.

6.  **[Prevenção de Campos Duplicados](prevencao_duplicatas.md)**
    *   Estratégias de normalização e algoritmos de similaridade (Levenshtein) para evitar que usuários criem campos redundantes.

7.  **[Guia Prático de BI (Power BI / Metabase)](guia_bi_pratico.md)**
    *   O passo a passo para transformar dados JSONB em tabelas limpas para relatórios e análise de dados.

8.  **[Visualização e Analytics na UI](visualizacao_e_bi.md)**
    *   Conceitos de tabelas dinâmicas, renderização de células por tipo e dashboards de analytics integrados.

---

## 🛠️ Resumo da Tech Stack Sugerida

*   **Banco de Dados:** PostgreSQL 12+ (Extensão JSONB).
*   **Backend:** FastAPI (Python) ou NestJS (Node.js).
*   **Frontend:** Vue.js 3 ou React (com renderização dinâmica de componentes).
*   **BI:** Power BI, Metabase ou Tableau conectando via SQL Views.

---
*Gerado por Antigravity AI*
