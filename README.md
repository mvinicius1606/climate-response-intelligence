# Climate Response Intelligence

> Dados confiáveis para uma resposta a desastres climáticos justa, transparente e orientada por evidências.

Climate Response Intelligence é um projeto de portfólio e de hackathon universitário voltado ao uso de dados públicos históricos para apoiar a distribuição humanitária de recursos. Integra a Trilha 3 — **Justiça, Ética, Trabalho e Sociedade** — do hackathon *Inovação para uma Sociedade Mais Humana*.

O recorte atual estuda as enchentes do **Rio Grande do Sul, entre 27/04 e 27/05/2024**, com dados demográficos de referência 2022 e registros oficiais do evento.

## Sumário

- [Problema e objetivo](#problema-e-objetivo)
- [Estado atual](#estado-atual)
- [Arquitetura](#arquitetura)
- [Fontes configuradas](#fontes-configuradas)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Como executar](#como-executar)
- [Validação e limitações](#validação-e-limitações)
- [Documentação e desenvolvimento](#documentação-e-desenvolvimento)
- [Licença](#licença)

## Problema e objetivo

A população de um município, isoladamente, não representa sua necessidade humanitária. Pessoas afetadas, vulnerabilidade, infraestrutura danificada e restrições de acesso também influenciam a resposta ao desastre.

O objetivo é construir uma base rastreável para produzir indicadores e apoiar uma priorização municipal explicável. As decisões devem permanecer sob responsabilidade humana, com regras revisáveis e limitações dos dados visíveis.

O desenvolvimento começa pela aquisição e preservação dos originais. Transformações, indicadores e apresentação serão construídos em unidades de trabalho posteriores.

## Estado atual

**Referência: 15/09/2026.**

| Componente | Situação |
| --- | --- |
| Pesquisa e configuração inicial de fontes | Oito YAMLs selecionados, com evidências e limitações documentadas |
| Implementação da ingestão Bronze | Implementada e validada por dez testes offline |
| Carga real das oito fontes no S3 | Pendente; tentativa real interrompida por HTTP 403 na primeira fonte IBGE; nenhum upload realizado |
| Silver — transformação e Data Quality | Planejada |
| Gold — indicadores e apoio à decisão | Planejada |
| App — apresentação e interação | Planejado |

A implementação atual processa **oito configurações que produzem nove arquivos brutos e nove manifests**. Os testes utilizam HTTP e S3 simulados; eles não comprovam acesso ao bucket nem sucesso de uma carga real.

O detalhamento está no [STATUS da Bronze](ingestao-bronze/STATUS.md).

## Arquitetura

A organização do projeto segue quatro etapas:

```text
Fontes oficiais
    ↓
Bronze: aquisição e preservação dos bytes originais
    ↓
Silver: transformação, conformação e Data Quality [planejada]
    ↓
Gold: indicadores e apoio à decisão [planejada]
    ↓
App: apresentação e interação [planejado]
```

A Bronze implementada utiliza Python e funções simples:

```text
gatilhador.py
    ↓
config_loader.py → YAMLs validados → dict Python
    ↓
extractor.py → API/JSON, ZIP ou PDF → bytes originais
    ↓
metadata.py → configuração + metadata da execução + SHA-256
    ↓
aws.py → arquivo bruto e manifest JSON no S3
    ↓
próxima configuração
```

As dependências são **PyYAML**, **boto3** e **python-dotenv**. O acesso HTTP utiliza a biblioteca padrão do Python.

Os originais são imutáveis: o envio impede sobrescritas de objetos existentes. As chaves seguem `source.id/nome-do-arquivo`; cada original recebe um arquivo associado com sufixo `.manifest.json`.

## Fontes configuradas

| Instituição | Configuração / conteúdo | Formato | Arquivos por execução |
| --- | --- | --- | --- |
| IBGE | População, área e densidade — SIDRA 4714 | JSON | 1 |
| IBGE | População por idade — SIDRA 9514 | JSON | 1 |
| IBGE | Abastecimento de água — SIDRA 6803 | JSON | 1 |
| IBGE | Esgotamento sanitário — SIDRA 6805 | JSON | 1 |
| IBGE | Tipo de domicílio — SIDRA 6326 | JSON | 1 |
| INMET | Acervo anual de estações automáticas de 2024 | ZIP | 1 |
| Governo RS | Coletivas de 09 e 10/05/2024 | PDF | 2 |
| Governo RS / DOE | Decreto 57.614, em cópia oficial preservada pela PGM de Porto Alegre | PDF | 1 |

Os dados IBGE utilizam referência **2022**. A atualização posterior de uma tabela, inclusive em 2026, não impede seu uso histórico autorizado; ano de referência e data de atualização são informações distintas.

O ZIP nacional do INMET é preservado integralmente, sem extrair CSVs ou filtrar estações na Bronze. As três medições ausentes identificadas na estação A801 foram aceitas pelo autor e devem permanecer exatamente como disponibilizadas pela fonte.

ANA, S2ID e fontes logísticas adicionais não fazem parte do executor atual. Consulte o [inventário das fontes](ingestao-bronze/docs/dados-de-fonte.md) para evidências, cobertura e pendências.

## Estrutura do repositório

```text
climate-response-intelligence/
├── ingestao-bronze/
│   ├── config/             # oito YAMLs de fontes
│   ├── src/                # configuração, extração, metadata e AWS
│   ├── tests/              # testes offline da Bronze
│   ├── docs/               # fontes, decisões e execução
│   ├── gatilhador.py       # ponto de entrada
│   ├── requirements.txt
│   └── STATUS.md
├── etl-silver/             # etapa planejada
├── inteligencia-gold/      # etapa planejada
├── app/                    # etapa planejada
├── tests/                  # espaço para testes transversais
├── AGENTS.md
├── README.md
├── CHANGELOG.md
└── ROADMAP.md
```

A presença de um diretório ou placeholder não significa funcionalidade implementada.

## Como executar

A partir da raiz do repositório:

```powershell
cd ingestao-bronze
python -m pip install -r requirements.txt
python gatilhador.py
```

A execução requer um bucket S3 existente e credenciais com permissão de escrita. A configuração é carregada do ambiente e dos arquivos `.env` locais da etapa e da raiz, sem sobrescrever variáveis já definidas no ambiente.

São utilizados `BUCKET_BRONZE`, `AWS_REGION`, `AWS_SECRET_ACCESS_KEY` e `AWS_ACESS_KEY_ID` — esta última com a grafia existente no ambiente do projeto. O nome padrão `AWS_ACCESS_KEY_ID` também é aceito, assim como `AWS_SESSION_TOKEN`, quando necessário.

**Esse comando realiza downloads e uploads reais**, incluindo o ZIP completo do INMET. Para verificar o código sem esses acessos, execute os testes:

```powershell
python -B -m unittest discover -s tests -v
```

Consulte [execução da ingestão Bronze](ingestao-bronze/docs/INGESTAO.md) para configuração, organização dos objetos e tratamento de falhas.

## Validação e limitações

Os dez testes offline verificam carregamento das fontes, dispatch dos três mecanismos, múltiplos PDFs, preservação dos bytes, SHA-256, serialização e independência do manifest, configuração AWS, propagação de erros e orquestração.

Limites atuais:

- A carga integrada permanece pendente: HEAD do bucket funcionou, mas a primeira fonte IBGE retornou HTTP 403 em 15/09/2026.
- A primeira falha interrompe a execução. Não há retry HTTP automático.
- Reexecuções verificam arquivos existentes e completam manifests ausentes quando conteúdo e configuração coincidem; divergências são bloqueadas.
- O bruto e o manifest são enviados separadamente; uma carga parcial pode ser retomada com a metadata de recuperação armazenada no original.
- Os arquivos ficam em memória durante o processamento de cada fonte.
- A cobertura municipal e temporal completa do evento ainda não foi demonstrada.

A Bronze preserva o conteúdo recebido, sem limpeza, preenchimento de nulos, conversão para Parquet ou cálculo de indicadores.

## Documentação e desenvolvimento

- [Qualidade de dados e Data Lineage](DATAQUALITY.md)
- [Regras globais de trabalho](AGENTS.md)
- [Regras da Bronze](ingestao-bronze/AGENTS.md)
- [Estado atual da Bronze](ingestao-bronze/STATUS.md)
- [Execução e validação](ingestao-bronze/docs/INGESTAO.md)
- [Inventário de fontes e limitações](ingestao-bronze/docs/dados-de-fonte.md)
- [Decisões da Bronze](ingestao-bronze/docs/decisoes.md)

O projeto avança em pequenas unidades autorizadas, com validação e documentação proporcionais à mudança. Credenciais, datasets volumosos e artefatos gerados não devem ser versionados.

## Licença

Ainda não foi escolhida uma licença de software. As licenças e condições de uso dos datasets devem ser avaliadas individualmente; a origem oficial não equivale à confirmação de uma licença específica.
