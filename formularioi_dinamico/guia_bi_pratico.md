# Guia Prático: Como Fazer BI dos Dados Customizados

Para fazer BI (Business Intelligence) de dados que estão "escondidos" dentro de um JSON ou em tabelas EAV, o segredo é **tornar os dados tabulares** (colunas e linhas fixas) antes de enviar para a ferramenta de BI (Power BI, Tableau, Metabase).

Aqui está o passo a passo de como você faz isso:

---

## Passo 1: "Achatando" o JSON (Flattening)

Se você escolheu a **Opção 2 (JSONB)**, os dados estão em uma coluna. Para o BI, você cria uma **View** que transforma cada chave do JSON em uma coluna real.

### SQL para PostgreSQL:
```sql
CREATE OR REPLACE VIEW vw_bi_pessoas_detalhado AS
SELECT 
    p.id,
    p.nome,
    p.cpf,
    -- Extraindo campos simples
    p.campos_customizados->>'sexo' AS sexo,
    p.campos_customizados->>'escolaridade' AS escolaridade,
    (p.campos_customizados->>'salario')::numeric AS salario,
    
    -- Tratando campos que o usuário pode ter digitado errado (usando COALESCE)
    -- Isso une "raca" e "raça" em uma única coluna no BI!
    COALESCE(
        p.campos_customizados->>'raca_cor', 
        p.campos_customizados->>'raca', 
        p.campos_customizados->>'Raça'
    ) AS raca_unificada
    
FROM pessoa p;
```

---

## Passo 2: Lidando com Dados Multivalorados (Raça, Cores, etc.)

Dados como "Raça" (onde a pessoa pode marcar mais de uma) são arrays no JSON: `["Parda", "Indígena"]`. 

Para gráficos de pizza ou barras, você precisa **explodir** esses dados:

### SQL para Explodir Arrays:
```sql
CREATE OR REPLACE VIEW vw_bi_distribuicao_raca AS
SELECT 
    p.id AS pessoa_id,
    jsonb_array_elements_text(
        CASE 
            WHEN jsonb_typeof(p.campos_customizados->'raca_cor') = 'array' 
            THEN p.campos_customizados->'raca_cor'
            ELSE '["Não Informado"]'::jsonb 
        END
    ) AS raca_item
FROM pessoa p;
```
*Isso transforma uma pessoa com 2 raças em **2 linhas** na view, permitindo que o Power BI conte corretamente.*

---

## Passo 3: Criando uma "Tabela de Fatos" Estável

Ferramentas de BI sofrem se a estrutura do banco muda toda hora. A melhor prática é criar uma **Tabela de BI** (ou View Materializada) que seja estável.

```sql
CREATE MATERIALIZED VIEW mv_bi_analytics AS
SELECT 
    p.id,
    p.nome,
    p.cidade, -- de endereco
    p.estado, -- de endereco
    -- Campos calculados para o BI
    CASE 
        WHEN (p.campos_customizados->>'idade')::int < 18 THEN 'Menor de Idade'
        WHEN (p.campos_customizados->>'idade')::int BETWEEN 18 AND 60 THEN 'Adulto'
        ELSE 'Idoso'
    END AS faixa_etaria,
    -- Campos customizados
    p.campos_customizados->>'sexo' AS genero,
    p.campos_customizados->>'profissao' AS cargo
FROM pessoa p
JOIN endereco e ON p.id = e.pessoa_id;
```

---

## Passo 4: Conectando na Ferramenta de BI

### No Power BI:
1. Clique em **Obter Dados** -> **PostgreSQL**.
2. Digite o servidor e o banco.
3. Importe a View `mv_bi_analytics` em vez da tabela original.
4. **Pronto!** O Power BI verá colunas normais como `genero`, `faixa_etaria` e `cargo`.

---

## Por que essa é a melhor solução?

1. **Performance**: Consultar JSON direto no Power BI é lento. Consultar uma View Materializada é instantâneo.
2. **Limpeza**: Você resolve o problema de "raca" vs "raça" direto no SQL da View, entregando o dado limpo para o BI.
3. **Segurança**: Você pode esconder colunas sensíveis (como CPF ou Senha) na View de BI.
4. **Independência**: Se você mudar o nome do campo no formulário dinâmico, você só ajusta o SQL da View, e seu dashboard de BI não quebra.

---

## Dica de Ouro para o BI

Se o volume de dados for muito grande (milhões de linhas), use um processo de **ETL** (Extract, Transform, Load) para copiar esses dados transformados para uma tabela física de madrugada.

```sql
-- Executar via CRON toda noite
REFRESH MATERIALIZED VIEW mv_bi_analytics;
```

Com isso, seu BI voará e seus usuários poderão criar qualquer campo que o relatório se adaptará! 🚀
