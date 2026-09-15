# Arquitetura da ingestão Bronze

## Sumário

- [Objetivo e estado](#objetivo-e-estado)
- [Fluxo e responsabilidades](#fluxo-e-responsabilidades)
- [Configuração e aquisição](#configuração-e-aquisição)
- [Manifest e destino](#manifest-e-destino)
- [Qualidade e lineage](#qualidade-e-lineage-na-aquisição)
- [Falhas e limites](#falhas-e-limites)
- [Validação e operação](#validação-e-operação)

## Objetivo e estado

A Bronze adquire e preserva os bytes das oito fontes YAML selecionadas. A implementação foi validada com dez testes offline; a carga real no S3 permanece pendente. Transformações e integração entre fontes pertencem às etapas posteriores.

## Fluxo e responsabilidades

| Componente | Entrada | Responsabilidade e saída |
| --- | --- | --- |
| `gatilhador.py` | Configurações e ambiente | Coordena sequencialmente as fontes e interrompe na primeira falha |
| `src/config_loader.py` | Arquivos `config/*.yml` | Usa `yaml.safe_load`, valida o mínimo necessário e retorna uma lista de dicts |
| `src/extractor.py` | Configuração da fonte | Executa GET e retorna lista de arquivos com bytes, nome, URL, resource_id e retrieved_at |
| `src/metadata.py` | Configuração, arquivo e destino | Copia a configuração e acrescenta metadata dinâmica, sem modificar a entrada |
| `src/aws.py` | Arquivo, manifest e configuração AWS | Envia o bruto e o manifest ao bucket existente |

```text
YAML → dict → GET → bytes originais → manifest → S3 → próximo YAML
```

Não há classes por fonte ou camada de services. API/JSON, download/ZIP e download/PDF são os três mecanismos compartilhados.

## Configuração e aquisição

Somente fontes com `status: validated` são processadas. O carregador ignora `config.yml` vazio e rejeita configurações validadas com identificadores duplicados, acesso incompatível, método diferente de GET ou URL inválida. Configurações sem o status exigido são ignoradas. A ordenação dos arquivos YAML define a ordem de execução.

Os cinco YAMLs IBGE usam o mesmo mecanismo API. O INMET produz um ZIP nacional integral. Os dois YAMLs RS produzem três PDFs, pois `rs-coletivas.yml` possui dois recursos. Uma execução completa produz nove originais e nove manifests.

Campos descritivos de escopo não são filtros executáveis. Não há extração de CSVs, recorte de estações, parsing analítico de PDF, alteração de JSON ou preenchimento dos campos ausentes.

## Manifest e destino

O manifest corresponde à cópia profunda da configuração acrescida da seção `ingestion`:

| Campo | Origem |
| --- | --- |
| `retrieved_at` | Timestamp UTC ao concluir o download |
| `filename` | Nome obtido da URL; para API sem nome JSON, source.id.json |
| `source_url` | URL solicitada |
| `resource_id` | Identificador do recurso, quando existente |
| `size_bytes` | Comprimento do conteúdo recebido |
| `sha256` | SHA-256 dos mesmos bytes enviados ao S3 |
| `s3_bucket`, `s3_key` | Destino configurado |

O manifest é serializado como JSON UTF-8. As chaves são `source.id/filename` e `source.id/filename.manifest.json`. Não há particionamento temporal ou versionamento automático.

Os uploads usam `IfNoneMatch="*"` para impedir sobrescritas. Essa proteção é aplicada pelo cliente; não representa configuração de S3 Object Lock. O manifest registra o destino pretendido e os dados da aquisição, sem afirmar que o upload teve sucesso antes da resposta do S3.

## Qualidade e lineage na aquisição

O lineage atual é por arquivo: cada manifest conecta a configuração da fonte, a URL solicitada, o recurso individual, o instante de aquisição e o destino do conteúdo identificado pelo SHA-256. A configuração é copiada para preservar o contexto utilizado na execução, sem modificar o dict de entrada.

Em rs-coletivas, cada PDF tem seu próprio manifest e resource_id, embora os dois manifests incluam a configuração completa da coletânea. No INMET, o lineage alcança o ZIP nacional; não existem manifests individuais dos CSVs internos ou das estações.

O registro permite identificar a origem e o destino pretendido de um arquivo. Não inclui lineage por registro ou coluna, histórico de transformações, versão do código, run_id, URL final após redirecionamento, headers da resposta ou versão do objeto S3. Esses recursos não foram implementados.

O SHA-256 identifica os bytes baixados e é comparado com o objeto relido do S3; não há comparação com checksum oficial. A validação mínima de configuração e a rejeição de respostas vazias também não verificam schema, duplicatas, plausibilidade ou completude das medições.

Bruto e manifest devem ser considerados em conjunto na revisão de uma carga. Como os uploads são separados, a existência de um original não garante a presença de seu manifest. A recuperação implementada completa o manifest ausente quando os bytes e a configuração coincidem com a metadata do original.

As responsabilidades de qualidade por etapa, os limites das evidências e o tratamento documental das ausências estão em [DATAQUALITY.md](../../DATAQUALITY.md).

## Falhas e limites

O logging padrão registra início da fonte, extração, upload e falhas. As exceções são propagadas. Não há retry HTTP automático. A validação mínima rejeita conteúdo vazio, JSON inválido ou objeto de erro, ZIP sem estrutura e PDF sem assinatura/terminador; não avalia a semântica dos registros.

Bruto e manifest são enviados separadamente. Uma falha após o primeiro upload pode deixar apenas o original armazenado; a repetição verifica o conteúdo existente e completa o manifest com retrieved_at original. Divergências e originais legados sem metadata de recuperação impedem a retomada automática.

Cada fonte mantém seus arquivos em memória durante o processamento. A integração real depende de rede, bucket existente e permissões AWS, ainda sem validação de carga completa. HEAD do bucket funcionou; a execução de 15/09/2026 parou no HTTP 403 da primeira fonte IBGE.

## Validação e operação

Os testes isolam HTTP e AWS e verificam fluxo, bytes, configuração, recursos múltiplos, checksum, manifest e erros. Consulte [execução e testes](INGESTAO.md), [estado atual](../STATUS.md) e [decisões](decisoes.md).
