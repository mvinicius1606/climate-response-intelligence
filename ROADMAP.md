# Roadmap para a v0.1

Plano de entrega da primeira versão funcional em **24 de setembro de 2026**. O core técnico deve estar utilizável em 20–21 de setembro, reservando os dias finais para integração, testes, documentação e apresentação.

## Regras de entrega

- Concluir primeiro um recorte end-to-end pequeno.
- Armazenar manualmente e de forma imutável as fontes da Phase 1; automação não é critério de sucesso.
- Anexar evidências a cada trabalho concluído.
- Manter o score determinístico e as explicações baseadas no resultado estruturado.
- Reduzir escopo em vez de introduzir infraestrutura não planejada.

## Plano diário

| Data | Marco | Entregas / critério de saída | Estado |
| --- | --- | --- | --- |
| 11/set | Project Foundation | Estrutura, README, arquitetura, roadmap e backlog | Concluído |
| 12/set | Fontes e contratos | Fontes avaliadas; uma principal escolhida; granularidade, schema, chaves, licença, cobertura e limitações documentadas | Próximo |
| 13/set | AWS Bronze | Convenção de bucket/prefix; fonte original enviada manualmente; manifest e checksum registrados | Planejado |
| 14/set | Data Profiling | Profiling Python/Pandas reproduzível de tipos, nulos, duplicatas, cardinalidade, ranges, distribuições e chaves | Planejado |
| 15/set | Data Quality Framework | Catálogo versionado com dimensões, severidade, justificativa, tratamento e disposition | Planejado |
| 16/set | Fundamentos de dbt | Projeto mínimo e adapter local; primeiro source e model; `source()`, `ref()`, YAML e instruções | Planejado |
| 17/set | dbt staging | Staging models tipados, renomeados e normalizados, com proveniência | Planejado |
| 18/set | Testes dbt | `not_null`, `unique`, `relationships`, `accepted_values` e primeiros custom tests legíveis | Planejado |
| 19/set | Silver | Registros validados e conformados; registros rejeitados/quarentenados auditáveis | Planejado |
| 20/set | Qualidade avançada | Regras entre colunas e de negócio; relatório com falhas reais; core utilizável | Planejado |
| 21/set | Gold e Decision Intelligence | Indicadores por município/evento e score transparente com pesos e sensibilidade documentados | Planejado |
| 22/set | Decision Engine e IA | Resultado determinístico estruturado; explicação fundamentada, fallback e validação básica | Planejado |
| 23/set | Streamlit e end-to-end | Páginas finas de qualidade e cenário; fluxo completo e smoke test | Planejado |
| 24/set | Release v0.1 | Documentação, screenshots, limitações, teste de reprodução, demo script e release notes | Planejado |
| 25/set | Contingência online | Somente correções e apresentação; sem novo escopo de core | Reservado |
| 1/out | Possível etapa presencial | Demo estável e pacote de apresentação | Condicional |

## Definition of Done da v0.1

- [ ] Datasets históricos, licenças, granularidade, schemas, cobertura e limitações documentados.
- [ ] Originais no S3 Bronze com manifest, timestamp, checksum e URL de origem.
- [ ] Profiling reproduzível com evidências de problemas reais.
- [ ] Regras de qualidade com dimensão, severidade, impacto, tratamento e disposition.
- [ ] Projeto dbt funcional com sources, staging, Silver, Gold, generic tests e custom tests selecionados.
- [ ] Dados inválidos visíveis e auditáveis, sem descarte silencioso.
- [ ] Gold suporta um score de priorização determinístico e documentado.
- [ ] Cada score expõe fatores, pesos, versão da regra e lineage.
- [ ] IA explica o resultado sem alterá-lo e possui fallback sem IA.
- [ ] Streamlit consome módulos da aplicação sem conter lógica central.
- [ ] Testes, configuração, limitações, screenshots e demo script estão documentados.
- [ ] Uma pessoa revisora consegue rastrear a recomendação até fonte e evidências de qualidade.

## Gate da Phase 2

O trabalho preditivo e operacional só começa após revisão das evidências da v0.1 e confirmação de que qualidade, lineage e reconstrução histórica são adequadas. Ingestão agendada, observações atuais, temporal features, previsões 24/48/72h, monitoramento e simulação são possibilidades futuras, não compromissos para setembro.

## Pontos de aprendizado

Cada marco deve reservar uma tarefa acessível: escrever um `source contract`, interpretar um profiling, adicionar uma regra e fixture, construir um staging model, criar um generic test e um custom test e explicar um fator do score em linguagem simples.
