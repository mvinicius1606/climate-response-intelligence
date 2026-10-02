# Estado atual — Ingestão Bronze

**Atualizado em:** 02/10/2026.

**Estado da etapa:** implementação concluída e validada offline. A carga real no S3 continua sem comprovação e não é apresentada como realizada.

| Componente | Estado | Evidência / limite |
| --- | --- | --- |
| Pesquisa inicial dos quatro domínios | CONCLUÍDO | Catálogos, serviços, publicações e limitações documentados |
| Validação integral das fontes para o MVP temporal municipal | PENDENTE | ANA, S2ID, histórico rodoviário e versões temporais ainda insuficientemente confirmados |
| Configurações dos recursos confirmados | CONCLUÍDO | Oito YAML descritivos, com validação limitada às amostras e documentos registrados |
| População/área — referência histórica 2022 | CONCLUÍDO | Acesso e amostra confirmados; autor aceita atualização em 2026 para uso dos dados históricos |
| Cobertura pluviométrica estadual completa | PENDENTE | Índice INMET contém 44 arquivos do RS; conteúdo validado somente em A801 |
| Série de impactos por município e publicação | PENDENTE | Confirmados PDFs agregados e um decreto; recuperação dos demais recursos pendente |
| Série logística por trecho e publicação | PENDENTE | Evidências pontuais confirmadas; histórico completo de mapas não demonstrado |
| Implementação das oito fontes YAML | CONCLUÍDO | Dez testes offline aprovados; nove arquivos e 18 uploads simulados |
| Carga real IBGE / INMET / RS no S3 | PENDENTE | HEAD do bucket bem-sucedido; execução real interrompida por HTTP 403 na primeira fonte IBGE, sem uploads |
| Ingestão ANA | PENDENTE | Mantida como fonte pendente; descartada do uso imediato como dado validado da enchente do RS |
| Ingestão S2ID | PENDENTE | Fora do escopo desta implementação |
| Logística adicional | PENDENTE | Fora do escopo; pesquisa alternativa depende de autorização do autor |

## Entregas existentes

- [Inventário das fontes e evidências](docs/dados-de-fonte.md).
- [Arquitetura implementada](docs/ARCHTETURE.md).
- [Decisões de seleção e implementação](docs/decisoes.md).
- Oito configurações em [config/](config/): cinco tabelas IBGE, INMET, coletivas RS e Decreto 57.614.

O fluxo funcional está implementado em gatilhador.py, config_loader.py, extractor.py, metadata.py e aws.py. Validação offline não equivale a carga real no S3. Consulte [execução e limites](docs/INGESTAO.md).

## Próxima etapa

A próxima etapa do projeto é a Silver. Antes de transformar dados, confirmar a localização e disponibilidade dos artefatos Bronze que serão usados e definir um primeiro recorte de trabalho. A pendência operacional da carga real no S3 permanece registrada acima e em [execução e limites](docs/INGESTAO.md); ela não altera o estado dos testes offline nem deve ser ocultada.
