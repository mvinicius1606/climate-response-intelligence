# Climate Response Intelligence

> Dados confiáveis para uma resposta a desastres climáticos justa, transparente e orientada por evidências.

Climate Response Intelligence é um projeto de portfólio e de hackathon universitário que transforma dados públicos históricos sobre desastres em informações auditáveis para a distribuição humanitária de recursos.

> Como dados confiáveis podem tornar a distribuição de recursos em crises climáticas mais justa, transparente e baseada em evidências?

O projeto integra a Trilha 3 — **Justiça, Ética, Trabalho e Sociedade** — do hackathon *Inovação para uma Sociedade Mais Humana: soluções integradas para os desafios do presente e do futuro*.

## O problema

O tamanho da população, sozinho, não representa adequadamente a prioridade humanitária. Um município menor pode ter maior necessidade quando há mais pessoas afetadas, maior vulnerabilidade, infraestrutura danificada, acesso limitado ou poucos recursos locais.

O sistema combinará esses fatores por regras explícitas e revisáveis. Ele é uma ferramenta de **apoio à decisão**, não uma autoridade autônoma: pessoas continuam responsáveis pelas decisões, as limitações das fontes permanecem visíveis e nenhuma narrativa gerada por IA pode alterar o `priority score` determinístico.

## Princípios orientadores

- **Confiança antes da previsão:** recomendações dependem da confiabilidade dos dados de origem.
- **Validação histórica antes da previsão futura:** reconstruir eventos conhecidos antes de criar previsões.
- **Equidade desde a concepção:** avaliar necessidade e vulnerabilidade, não apenas população absoluta.
- **Decisões explicáveis:** rastrear cada resultado até entradas, `quality checks`, pesos e `business rules`.
- **IA responsável:** usar IA para explicar resultados estruturados, nunca para decidir quem recebe recursos.
- **A tecnologia acompanha o problema:** evitar infraestrutura sem valor real para este MVP de dados estáticos.

## Escopo

### Phase 1 — Historical Data Quality & Decision Intelligence (v0.1)

O MVP de setembro de 2026 usa dados públicos históricos, com ingestão manual, para validar a fundação de dados e produzir priorização municipal explicável.

```text
Dados públicos históricos -> S3 Bronze (raw/immutable) -> Data Profiling -> Data Quality
    -> dbt staging/silver/gold -> Decision Engine determinístico
    -> Explicação com IA baseada em evidências -> Interface Streamlit fina
```

Marcos:

- core técnico pronto até **20–21 de setembro de 2026**;
- etapa online de **21–25 de setembro de 2026**;
- v0.1 pronta até **24 de setembro de 2026**;
- possível etapa presencial em **1º de outubro de 2026**.

A v0.1 inclui documentação das fontes, armazenamento Bronze manual e imutável, profiling reproduzível, regras de qualidade com severidade, transformações e testes dbt, dados Gold orientados à decisão, score determinístico, explicações fundamentadas e uma pequena interface de demonstração.

### Phase 2 — Predictive & Operational Intelligence (futuro)

Somente depois de a Phase 1 comprovar a fundação de dados, uma fase posterior poderá incluir ingestão recorrente de dados meteorológicos, `temporal features`, previsões, monitoramento e simulação de cenários. A Phase 2 **não faz parte do MVP de setembro**.

### Fora do escopo da v0.1

- Kafka, Airflow, Spark, streaming, Kubernetes ou arquitetura distribuída;
- Machine Learning preditivo e agentes autônomos;
- autenticação, frontend React ou operação em produção;
- ingestão Bronze automatizada.

## Arquitetura proposta

| Camada | Responsabilidade |
| --- | --- |
| Fontes públicas | Dados históricos de desastres, demografia, vulnerabilidade, infraestrutura e geografia |
| S3 Bronze | Cópias manuais e imutáveis, `source manifests` e checksums |
| Profiling e Data Quality | Detectar anomalias e avaliar dimensões de qualidade |
| dbt staging e Silver | Renomear, tipar, padronizar, validar e conformar registros |
| Gold | Publicar indicadores por município/evento com proveniência |
| Decision Engine | Calcular `priority score` determinístico e justificativa por fator |
| Explicação com IA | Explicar somente o resultado estruturado recebido, com salvaguardas e grounding |
| Streamlit | Apresentar evidências de qualidade e cenários sem conter `business logic` |

Consulte [a documentação de arquitetura](docs/architecture.md) para limites e requisitos de rastreabilidade.

## Estrutura do repositório

```text
.
├── app/                    # placeholder da interface fina
├── data/                   # política de dados; datasets locais ignorados
├── dbt/                    # placeholder do projeto dbt
├── docs/                   # arquitetura, fontes, qualidade, backlog e decisões
├── notebooks/profiling/    # placeholder para exploração reproduzível
├── src/                    # data, quality, decision_engine e ai
├── tests/                  # placeholder para testes automatizados
├── README.md
└── ROADMAP.md
```

Os diretórios contêm apenas placeholders documentais, sem implementações prematuras. Datasets grandes ou sensíveis, credenciais, artefatos gerados e profiles locais nunca devem ser versionados.

## Estado atual e próximo marco

**Project Foundation (11 de setembro de 2026):** estrutura, escopo, roadmap, arquitetura, framework inicial de qualidade, template de fontes e backlog priorizado estão documentados. Ainda não há comportamento implementado em dbt, IA ou Streamlit.

1. Leia [ROADMAP.md](ROADMAP.md).
2. Avalie fontes candidatas com [docs/data-sources.md](docs/data-sources.md).
3. Registre proprietário, licença, data de obtenção, granularidade, chaves, cobertura, schema e limitações.
4. Defina o primeiro `data contract` antes de enviar o original imutável ao S3 Bronze.
5. Registre aprendizados e decisões conforme o trabalho avançar.

Ainda não há comando de instalação ou execução. As instruções serão adicionadas junto ao primeiro recorte executável de profiling, para que permaneçam corretas.

## Critério de sucesso e salvaguardas

Uma recomendação deve ser rastreável da explicação aos fatores determinísticos, registros Gold, transformações, resultados de qualidade e metadados da fonte original. O sistema não pode ocultar dados ausentes, apresentar prioridade como verdade objetiva nem sugerir que IA substitui julgamento humanitário.

## Contribuição e documentação

Mantenha mudanças pequenas, legíveis e ligadas ao [backlog](docs/backlog.md). Prefira soluções diretas, registre decisões relevantes em `docs/decisions/`, não versione credenciais ou datasets grandes e forneça evidências para cada critério concluído.

- [Roadmap](ROADMAP.md)
- [Arquitetura](docs/architecture.md)
- [Inventário de fontes e template de contrato](docs/data-sources.md)
- [Framework de Data Quality](docs/data-quality-framework.md)
- [Backlog inicial](docs/backlog.md)
- [Learning Log](docs/learning-log.md)
- [Política de dados](data/README.md)

## Licença

Ainda não foi escolhida uma licença de software; portanto, direitos de reutilização não estão implícitos. Cada dataset deve ter sua própria licença ou termos avaliados e documentados. A seleção da licença do repositório está no backlog.
