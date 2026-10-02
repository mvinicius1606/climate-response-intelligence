# Orientações iniciais — ETL Silver

## Objetivo

A Silver deve transformar dados brutos da Bronze em conjuntos estruturados, consistentes e rastreáveis para consumo analítico posterior. O foco desta etapa é tornar explícitos os contratos, a granularidade, as regras de qualidade e os tratamentos aplicados, preservando a ligação com os arquivos de origem.

Esta documentação marca o início da preparação da etapa. Não registra implementação, execução de transformações ou validação de dados Silver.

## Contexto de entrada

A Bronze contém oito configurações de fontes: cinco consultas IBGE em JSON, um acervo anual INMET em ZIP com arquivos CSV e três documentos PDF distribuídos por duas configurações RS. Uma execução completa foi projetada para produzir nove arquivos originais e nove manifests.

O código e os testes offline da ingestão estão concluídos. A tentativa real registrada em 15/09/2026 foi interrompida por HTTP 403 na primeira fonte IBGE e não realizou uploads. Portanto, a existência, localização e conteúdo dos objetos que serão usados como entrada da Silver devem ser confirmados antes de assumir que há dados disponíveis. Consulte o [STATUS da Bronze](../ingestao-bronze/STATUS.md) e o [inventário de fontes](../ingestao-bronze/docs/dados-de-fonte.md).

## Limites de responsabilidade

- A Bronze continua sendo a referência dos bytes originais e dos manifests de aquisição; transformações não devem sobrescrever esses objetos.
- A Silver não deve converter uma ausência em zero, remover registros ou harmonizar categorias sem regra explícita, justificativa e evidência.
- Datas de referência, observação, publicação e aquisição são conceitos distintos e devem continuar identificáveis quando relevantes.
- Os PDFs têm conteúdo documental e cobertura pontual; não se presume que todo arquivo tenha extração tabular adequada.
- A documentação das fontes contém limites de cobertura e validação que precisam acompanhar qualquer conjunto derivado.

## Decisões ainda necessárias

Antes da primeira transformação, definir com base nos artefatos reais e em escopo autorizado:

1. Quais arquivos e fontes entram no primeiro recorte.
2. Onde os arquivos de origem estão disponíveis e como a execução os acessará.
3. A granularidade e os campos esperados de cada conjunto Silver.
4. Tipos, identificadores, datas e tratamento de categorias e valores ausentes.
5. Regras de validação, disposição de registros inválidos e evidências de lineage.
6. Ferramenta, formato de saída e organização de armazenamento, se necessários.

Os itens acima são perguntas de trabalho, não decisões já adotadas. Não há escolha documentada de dbt, Pandas, Parquet ou outra tecnologia para esta etapa.

## Sequência de trabalho

1. Confirmar e inspecionar um artefato Bronze real, junto ao manifest correspondente.
2. Registrar schema observado, granularidade, limitações e perguntas em aberto.
3. Propor o contrato do primeiro conjunto Silver e revisar seu impacto nos consumidores.
4. Implementar apenas o recorte autorizado, preservando a origem e tornando os tratamentos auditáveis.
5. Validar com testes e evidências apropriados antes de atualizar o status.

O estado atual e a próxima ação estão em [STATUS](STATUS.md). As responsabilidades gerais de qualidade e lineage estão em [DATAQUALITY.md](../DATAQUALITY.md).

O status da Silver deve refletir somente trabalho implementado e validado; a preparação documental não comprova transformações nem qualidade dos dados.
