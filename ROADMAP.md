# Roadmap do projeto

O projeto é desenvolvido como portfólio técnico, em etapas incrementais. Este documento registra a sequência de trabalho sem prazos fixos; o escopo de cada unidade deve ser autorizado antes da implementação.

## Estado e sequência

| Etapa | Estado | Próximo resultado esperado |
| --- | --- | --- |
| Bronze — aquisição e preservação | Implementação concluída e validada offline | Manter registrada a pendência de comprovação da carga real no S3 |
| Silver — transformação e qualidade | Em preparação documental | Inspecionar os artefatos Bronze disponíveis e definir contratos, granularidade e validações antes de transformar dados |
| Gold — indicadores e apoio à decisão | Planejada | Definir indicadores somente após a Silver fornecer dados conformados e limitações documentadas |
| App — apresentação e interação | Planejada | Apresentar resultados já validados, sem concentrar regras de negócio na interface |

## Próxima etapa: Silver

A Silver começa pela confirmação dos artefatos de entrada realmente disponíveis, sua estrutura e suas limitações. Em seguida, devem ser definidos, com evidência dos dados e autorização do autor, o primeiro recorte, a granularidade, os contratos de entrada e saída, as transformações necessárias e os critérios de Data Quality.

Não estão definidos nesta etapa documental: ferramenta de transformação, formato de armazenamento, esquema canônico, política geral de rejeição/quarentena ou regras de negócio. Essas decisões não devem ser inferidas apenas a partir dos nomes das fontes ou dos campos descritos nos documentos.

Consulte [STATUS da Silver](etl-silver/STATUS.md) e [orientações iniciais da Silver](etl-silver/ETL.md). A pendência da carga real da Bronze está detalhada em [STATUS da Bronze](ingestao-bronze/STATUS.md).
