# Estado atual — Ingestão Bronze

**Atualizado em:** 15/09/2026.

| Componente | Estado | Evidência / limite |
| --- | --- | --- |
| Pesquisa inicial dos quatro domínios | CONCLUÍDO | Catálogos, serviços, publicações e limitações documentados |
| Validação integral das fontes para o MVP temporal municipal | PENDENTE | ANA, S2ID, histórico rodoviário e versões temporais ainda insuficientemente confirmados |
| Configurações dos recursos confirmados | CONCLUÍDO | Oito YAML descritivos, com validação limitada às amostras e documentos registrados |
| População/área — versão disponível em 2024 | PENDENTE | Descritor atual da tabela 4714 informa atualização em 2026 |
| Cobertura pluviométrica estadual completa | PENDENTE | Índice INMET contém 44 arquivos do RS; conteúdo validado somente em A801 |
| Série de impactos por município e publicação | PENDENTE | Confirmados PDFs agregados e um decreto; recuperação dos demais recursos pendente |
| Série logística por trecho e publicação | PENDENTE | Evidências pontuais confirmadas; histórico completo de mapas não demonstrado |
| Ingestão IBGE | PENDENTE | Nenhum extractor implementado ou executado |
| Ingestão ANA / INMET | PENDENTE | Somente validação de fonte e amostragem |
| Ingestão Defesa Civil / S2ID | PENDENTE | Somente descoberta e documentos confirmados |
| Ingestão Logística | PENDENTE | Somente descoberta e documentos confirmados |

## Entregas existentes

- [Inventário das fontes e evidências](docs/dados-de-fonte.md).
- [Decisão de seleção inicial](docs/decisoes.md).
- Oito configurações em [config/](config/): cinco tabelas IBGE, INMET, coletivas RS e Decreto 57.614.

Os arquivos de implementação e o `config.yml` existentes continuam placeholders. Configuração não equivale a ingestão, e as amostras de validação não constituem carga Bronze.

## Próxima ação recomendada

Uma ingestão pequena da tabela SIDRA 9514 é a candidata inicial. A execução depende de novo Prompt Inicial. As pendências e seus critérios de validação estão no [inventário](docs/dados-de-fonte.md#8-pendências-e-primeira-ingestão-recomendada).
