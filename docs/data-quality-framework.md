# Data Quality Framework

## Objetivo

Data Quality deve explicar não apenas que uma regra falhou, mas **por que importa, qual ação será tomada e se o registro pode contribuir com segurança para a decisão**. O framework começa por checks simples e valiosos; sofisticação estatística só entra quando as evidências exigirem.

## Dimensões

| Dimensão | Pergunta | Exemplo |
| --- | --- | --- |
| Completeness | Valores obrigatórios estão presentes? | `municipality_id IS NOT NULL` |
| Validity | Valor respeita tipo, domínio ou range? | `available_resources >= 0` |
| Uniqueness | A granularidade declarada é respeitada? | uma linha por município/evento |
| Consistency | Valores relacionados concordam? | `elderly_population <= total_population` |
| Referential integrity | Chave existe na referência aprovada? | código municipal existe na versão oficial |
| Temporal quality | Datas são coerentes e estão na cobertura? | início não ocorre depois do fim |
| Statistical quality | Distribuições inesperadas foram investigadas? | outlier ou mudança de cobertura |
| Geospatial quality | Coordenadas e associações são plausíveis? | ranges e ponto dentro do município |
| Business rules | Registro serve para a decisão declarada? | afetados não excedem população total |

## Severidade e disposition

| Severidade | Significado | Ação padrão |
| --- | --- | --- |
| `CRITICAL` | Pode corromper identidade, lineage, cálculo ou interpretação segura | Bloquear publicação ou colocar registro em quarentena |
| `WARNING` | Limitação material permite uso controlado | Continuar com flag, ressalva e monitoramento |
| `INFO` | Observação diagnóstica ou risco baixo | Continuar e registrar |

Exceções devem ser explícitas, temporárias, justificadas e revisáveis; nunca silenciosas.

## Schema do catálogo de regras

Cada regra define `rule_id`, `rule_version`, nome, descrição, dataset, colunas, escopo, dimensão, severidade, expressão, justificativa, impacto na decisão, tratamento da falha, disposition de sucesso/falha, owner e data de vigência.

## Regras iniciais provisórias

| Rule ID | Condição | Dimensão | Severidade | Tratamento da falha |
| --- | --- | --- | --- | --- |
| `DQ-001` | municipality ID presente | Completeness | `CRITICAL` | Quarentena; identidade e joins são inseguros |
| `DQ-002` | municipality ID existe na referência oficial aprovada | Referential integrity | `CRITICAL` | Quarentena; investigar mapeamento/versão |
| `DQ-003` | business key declarada é única | Uniqueness | `CRITICAL` | Quarentena do grupo; confirmar granularidade |
| `DQ-004` | populações total e afetada não são negativas | Validity | `CRITICAL` | Quarentena; não corrigir sem evidência |
| `DQ-005` | população afetada não excede a total | Consistency | `CRITICAL` | Quarentena ou correção documentada na fonte |
| `DQ-006` | população idosa não excede a total | Consistency | `CRITICAL` | Investigar denominador/período |
| `DQ-007` | latitude em [-90,90] e longitude em [-180,180] | Geospatial quality | `CRITICAL` | Quarentena das coordenadas |
| `DQ-008` | recursos disponíveis não são negativos | Business rule | `CRITICAL` | Retirar do cálculo e colocar em quarentena |
| `DQ-009` | data está na cobertura documentada | Temporal quality | `WARNING` | Continuar com ressalva e investigação |
| `DQ-010` | completeness dos fatores opcionais é reportada por geografia | Completeness | `WARNING` | Aplicar política documentada para fator ausente |

As regras só se tornam ativas após conciliação com os Data Contracts.

## Resultados e relatórios

Cada execução registra run ID, versão do objeto de origem, ID do registro, regra/versão, valor observado ou detalhe, status, severidade, disposition e timestamp. O relatório agrega registros totais, válidos, bloqueados e com ressalvas; falhas por regra; pass rate por dimensão; missingness por geografia/grupo quando ético; e versão da fonte/run.

Um overall quality score pode resumir o estado, mas deve mostrar sua fórmula e nunca esconder falha crítica. O release gate falha quando regras críticas não resolvidas atingem dados Gold publicados.

## Evolução da implementação

1. Confirmar contratos e executar profiling.
2. Ativar o menor conjunto crítico com fixtures sintéticas.
3. Criar checks reutilizáveis em Python.
4. Adicionar generic tests e custom SQL tests legíveis no dbt.
5. Persistir evidências e registros rejeitados.
6. Acrescentar checks temporais, estatísticos e geoespaciais conforme riscos observados.
