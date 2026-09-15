# Qualidade de dados e Data Lineage

## Sumário

1. [Objetivo](#objetivo)
2. [Responsabilidades por etapa](#responsabilidades-por-etapa)
3. [Controles atuais e evidências](#controles-atuais-e-evidências)
4. [Rastreabilidade temporal](#rastreabilidade-temporal)
5. [Ausências e cobertura](#ausências-e-cobertura)
6. [Validação e evolução](#validação-e-evolução)

## Objetivo

A confiabilidade do projeto depende de conhecer a origem dos dados, preservar o conteúdo recebido e explicitar suas limitações. Qualidade de dados significa avaliar se esses dados são adequados ao uso pretendido. Data Lineage é o registro do caminho entre a fonte, os arquivos adquiridos e os resultados derivados.

A Bronze fornece a base dessa rastreabilidade: conserva os originais e registra sua aquisição. Preservar um arquivo fielmente não demonstra que suas medições estão corretas, completas ou adequadas a uma análise municipal.

## Responsabilidades por etapa

| Etapa | Responsabilidade | Estado |
| --- | --- | --- |
| Bronze | Preservar originais e registrar origem, configuração, obtenção, tamanho, checksum e destino | Implementada e validada offline; carga real pendente |
| Silver | Avaliar tipos, chaves, duplicatas, ausências, consistência e relações entre fontes; documentar tratamentos | Planejada |
| Gold | Relacionar indicadores às entradas, regras e versões de cálculo | Planejada |
| App | Apresentar resultados com evidências e limitações compreensíveis | Planejado |

Detalhes técnicos específicos permanecem na [arquitetura da Bronze](ingestao-bronze/docs/ARCHTETURE.md). Esta documentação não implementa regras de qualidade ou contratos nas etapas futuras.

## Controles atuais e evidências

| Aspecto | Controle existente | O que ainda não demonstra |
| --- | --- | --- |
| Origem | YAML com instituição, identificação e parâmetros de acesso; URL solicitada no manifest | Exatidão de cada valor ou licença de reutilização |
| Configuração | Leitura segura e validação mínima de identificadores, recursos, URL e mecanismo | Validade do schema ou conteúdo retornado pela fonte |
| Preservação | Bytes obtidos são enviados sem limpeza, conversão ou preenchimento | Ausência de erros já existentes na origem |
| Integridade | SHA-256 e tamanho calculados sobre os bytes adquiridos | Comparação com checksum publicado pela instituição |
| Rastreabilidade | Manifest copia a configuração e adiciona metadata da aquisição | Lineage por linha, coluna ou transformação |
| Proteção contra sobrescrita | Upload condicional para chaves existentes | S3 Object Lock ou proteção contra alterações por outros clientes |
| Falhas operacionais | Resposta vazia, JSON inválido/erro, ZIP sem estrutura e PDF sem assinatura/terminador são rejeitados; exceções são propagadas | Validade semântica de uma resposta HTTP de sucesso |

O checksum funciona como uma referência para comparar o conteúdo em uma verificação posterior. Sua geração isolada não autentica a fonte nem prova a correção do dado. A implementação agora relê o original no S3 e compara tamanho e SHA-256; também relê e confere o manifest.

O status `validated` do YAML representa a validação documental e por amostra registrada no [inventário](ingestao-bronze/docs/dados-de-fonte.md). Não é um selo de qualidade de toda a base nem a confirmação de uma carga executada.

## Rastreabilidade temporal

O ano de referência, o instante da observação, a publicação, a revisão e a aquisição respondem a perguntas diferentes.

- **Referência ou observação:** a que período o dado se refere.
- **Publicação ou revisão:** quando a instituição divulgou ou alterou a informação.
- **Aquisição:** quando o projeto recebeu o conteúdo; registrada como `retrieved_at`.

O timestamp de aquisição não comprova que o mesmo dado estava disponível durante a enchente. A referência 2022 da tabela IBGE atualizada em 2026 foi aceita pelo autor para a reconstrução histórica; essa autorização não demonstra igualdade com a versão de 2024.

A comprovação de quais informações eram conhecidas em determinado instante dependeria de versões e datas de publicação que a ingestão atual não reconstrói automaticamente.

## Ausências e cobertura

A Bronze mantém as ausências como recebidas. Na amostra INMET A801, as linhas de 27/05/2024 às 09h, 10h e 11h UTC possuem campos meteorológicos vazios. O autor autorizou prosseguir com essas três lacunas, preservando o original. A ingestão conserva o ZIP completo sem abrir ou regravar seus CSVs.

Aceitar essas ausências permite continuar com a fonte, mas não comprova ausência de impacto em futuros acumulados. A definição de regras para resultados afetados por lacunas pertence à etapa analítica, mantendo o vínculo com o original.

A amostra de uma estação não valida a cobertura estadual. Da mesma forma, PDFs de publicações pontuais não constituem automaticamente uma série municipal completa. Datas e recortes descritos nos YAMLs não provocam filtros ou certificação automática de cobertura.

## Validação e evolução

Na implementação da Bronze, dez testes offline passaram, incluindo preservação dos bytes, checksum, cópia independente do manifest, recursos múltiplos, configuração, falhas e orquestração. HTTP e S3 foram simulados. A tentativa real de 15/09/2026 parou em HTTP 403 na primeira fonte IBGE. O HEAD do bucket funcionou, mas nenhum upload foi realizado nessa execução; não houve avaliação de todos os registros.

A conferência de tamanho e SHA-256 após releitura do S3 está implementada e validada offline. O código recupera manifests ausentes usando a metadata do original, preservando retrieved_at e exigindo configuração compatível. A comprovação integrada depende de uma carga real bem-sucedida.

A evolução do lineage para Silver e Gold deverá permitir relacionar saídas aos arquivos de entrada e às transformações aplicadas. Regras de qualidade deverão registrar finalidade, evidência, resultado e tratamento adotado. São orientações para futuras unidades autorizadas, sem introduzir ferramentas ou contratos executáveis nesta ação.

Consulte [STATUS](ingestao-bronze/STATUS.md), [execução e testes](ingestao-bronze/docs/INGESTAO.md) e [decisões](ingestao-bronze/docs/decisoes.md).
