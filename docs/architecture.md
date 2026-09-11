# Arquitetura da Phase 1

## Objetivo

A arquitetura sustenta uma demonstração histórica e auditável de Decision Intelligence humanitária. Ela prioriza clareza e rastreabilidade, não escala de produção, e mantém deliberadamente a ingestão manual.

## Fluxo de dados

```text
Datasets públicos históricos
        ↓
S3 Bronze (upload manual, bytes originais, manifest + checksum)
        ├──> Data Profiling reproduzível
        ↓
Data Quality (resultado da regra + severidade + disposition)
        ↓
dbt staging -> Silver validada/conformada -> indicadores Gold
        └──────── lineage e evidências de qualidade ────────┐
                                                            ↓
                                             Decision Engine determinístico
                                                            ↓
                                                resultado estruturado
                                                            ↓
                                    explicação com IA (opcional/falível)
                                                            ↓
                                          camada de apresentação Streamlit
```

## Limites dos componentes

### Bronze e acesso a dados

- `src/data/` conterá utilitários simples de acesso e manifest quando implementado.
- Arquivos são copiados manualmente para um prefix versionado do S3 e nunca alterados no local.
- O manifest registra URL, publicador, timestamp, nome original, checksum, licença e observações do processo.
- Credenciais e dados raw ficam fora do Git; apenas contratos, manifests sem segredos e pequenas fixtures intencionais podem ser versionados.

### Profiling e Data Quality

- `notebooks/profiling/` serve para exploração reproduzível; lógica reutilizável vai para `src/quality/`.
- Cada resultado identifica dataset/versão, regra/versão, escopo, valor observado, resultado, severidade, explicação e timestamp.
- Falhas `CRITICAL` bloqueiam ou colocam registros em quarentena; `WARNING` permite continuidade com ressalvas; `INFO` registra observações.
- Quality scores complementam, mas não substituem, evidências por regra.

### Camadas de transformação

- **Staging:** renomes, casts, normalização e colunas de proveniência alinhados à fonte.
- **Silver:** entidades validadas e conformadas, mantendo rejeições para auditoria.
- **Gold:** indicadores documentados por município/evento adequados ao contrato do score.
- dbt controla transformações SQL e testes; Python não deve duplicá-las por conveniência.

### Decision Engine

- `src/decision_engine/` recebe um registro Gold versionado e devolve resultado estruturado.
- O score expõe fatores normalizados, pesos, contribuições, tratamento de ausências, versão, estado de qualidade e justificativa determinística.
- O desenho passa por revisão de proxy bias e sensitivity. Ranking é apoio à decisão, não verdade moral ou estatística.

### Explicação com IA

- `src/ai/` recebe somente o resultado estruturado e as ressalvas de qualidade.
- IA não altera score, ranking, fatores ou eligibility e deve diferenciar evidência de interpretação.
- Schema validation, metadados de prompt/versão, falha segura e fallback determinístico são obrigatórios.

### Interface

- `app/` permanece fina: carrega resultados preparados, seleciona cenários e apresenta evidências.
- A página de qualidade mostra métricas por dimensão, falhas e severidade.
- A página de decisão mostra indicadores, contribuições, proveniência, ressalvas, justificativa e explicação opcional.
- Business rules e acesso a dados não pertencem a callbacks do Streamlit.

## Contrato de rastreabilidade

```text
scenario/result ID
  -> versão da regra do score + contribuições
  -> model/run Gold + estado de qualidade
  -> lineage dos models Silver/staging
  -> versão do objeto Bronze + manifest/checksum
  -> metadados da fonte pública
```

Logs e relatórios não devem conter dados pessoais. O MVP usa dados agregados por município/evento; qualquer fonte em nível individual exige revisão de privacidade separada.

## Posição de deployment e riscos

O MVP é uma demonstração, não um sistema emergencial de produção. AWS S3 é o único componente cloud comprometido. Execução local é aceitável; orchestration, streaming, processamento distribuído, autenticação e alta disponibilidade ficam adiados.

| Risco | Controle inicial |
| --- | --- |
| Definições e códigos geográficos divergentes | Contratos, referência oficial e regras explícitas de conformidade |
| Ausências afetam desproporcionalmente locais vulneráveis | Publicar missingness por grupo/geografia e ressalvas no score |
| Score composto oculta escolhas de valor | Versionar fatores/pesos, exibir contribuições e revisar sensitivity |
| IA inventa fatos ou exagera certeza | Grounding, validação, fallback e ressalvas visíveis |
| Processo Bronze perde proveniência | Manifest, checksum, versionamento e checklist do operador |
