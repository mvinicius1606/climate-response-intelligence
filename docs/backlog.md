# Backlog inicial — GitHub Issues propostas

Tarefas prontas para virar issues; labels e tamanhos são sugestões.

## P0 — caminho crítico

### 1. Selecionar caso histórico e datasets principais
**Labels:** `data-sources`, `documentation`, `priority:p0` — **Tamanho:** M

- Comparar fontes confiáveis de desastre, demografia, vulnerabilidade e geografia.
- Verificar licença, granularidade, cobertura, IDs, metodologia e download reproduzível.
- Escolher evento/geografia delimitados e justificar relevância e viabilidade.
- **Aceite:** inventário e um Data Contract revisados; limitações explícitas.
- **Aprendizado:** preencher uma fonte e explicar granularidade e chave.

### 2. Definir e executar o processo manual do S3 Bronze
**Labels:** `aws`, `data-engineering`, `priority:p0` — **Tamanho:** S

- Definir bucket/prefix, criptografia, bloqueio público, versionamento, retenção e least privilege.
- Criar manifest legível por máquina e verificação SHA-256.
- Fazer upload do original sem expor credenciais.
- **Aceite:** outra pessoa repete o checklist; versão e checksum conferem.

### 3. Criar baseline de profiling reproduzível
**Labels:** `python`, `data-quality`, `priority:p0` — **Tamanho:** M

- Avaliar schema/tipos, nulos, duplicatas, cardinalidade, ranges, distribuições e chaves.
- Separar narrativa do notebook de funções reutilizáveis; usar fixtures sintéticas.
- **Aceite:** um comando documentado reproduz output versionado.
- **Aprendizado:** adicionar e interpretar um check.

### 4. Tornar executável o catálogo de regras
**Labels:** `data-quality`, `priority:p0` — **Tamanho:** M

- Conciliar regras com contratos e atribuir owner/versão.
- Emitir resultado, severidade, justificativa, impacto, tratamento e disposition.
- Preservar quarentena e evidências de falhas reais.
- **Aceite:** testes cobrem sucesso/falha e totais reconciliam.

### 5. Criar projeto dbt mínimo e staging models
**Labels:** `dbt`, `learning`, `priority:p0` — **Tamanho:** M

- Escolher o adapter local mais simples e documentar sources, `source()`, `ref()`, YAML e lineage.
- Criar models tipados, renomeados e normalizados sem macros prematuras.
- **Aceite:** `dbt debug`, build e test passam em ambiente limpo.
- **Aprendizado:** adicionar uma coluna documentada e um generic test.

### 6. Publicar Silver auditável e evidências de qualidade
**Labels:** `dbt`, `data-quality`, `priority:p0` — **Tamanho:** M

- Conformar IDs oficiais, preservar proveniência e adicionar generic/custom tests.
- Manter rejeições e ressalvas inspecionáveis.
- **Aceite:** contagens reconciliam registros válidos, em quarentena e com ressalva.

### 7. Definir indicadores Gold e priorização determinística v1
**Labels:** `decision-intelligence`, `ethics`, `priority:p0` — **Tamanho:** L

- Definir fatores, normalização, pesos, política de ausência e versão.
- Revisar proxies, bias geográfico, sensitivity e impacto da qualidade.
- **Aceite:** score decomposto em contribuições reproduzíveis, incluindo empates e ausências.

## P1 — experiência e garantia do MVP

### 8. Adicionar explicações com IA e fallback determinístico
**Labels:** `ai`, `responsible-ai`, `priority:p1` — **Tamanho:** M

- Definir contratos estruturados e metadados de prompt/versão.
- Impedir alteração do score ou invenção de fatores; validar outputs e mostrar ressalvas.
- **Aceite:** fixtures cobrem fluxo normal, output inválido, API indisponível e dados ausentes.

### 9. Criar demonstração Streamlit fina
**Labels:** `streamlit`, `ux`, `priority:p1` — **Tamanho:** M

- Criar páginas de Data Quality e Decision Intelligence apoiadas pelos módulos.
- Mostrar falhas, severidade, contribuições, proveniência e limitações.
- **Aceite:** fluxo sem lógica central na UI; screenshots sem segredos.

### 10. Concluir garantia end-to-end da release
**Labels:** `testing`, `documentation`, `release`, `priority:p1` — **Tamanho:** M

- Executar pipeline do input à UI e documentar setup, evidências, limitações e demo script.
- **Aceite:** ensaio limpo passa e cada item da Definition of Done possui evidência.

## P2 — governança e continuidade

### 11. Escolher licença e política de contribuição
**Labels:** `governance`, `priority:p2` — **Tamanho:** S

- Confirmar restrições e esclarecer que fontes mantêm seus termos.
- **Aceite:** licença e orientação são consistentes e revisadas.

### 12. Preparar descoberta da Phase 2
**Labels:** `phase-2`, `research`, `priority:p2` — **Tamanho:** S

- Registrar usuários, horizonte, latência, avaliação e monitoramento; não implementar orchestration ou modelos.
- **Aceite:** proposta de go/no-go baseada em evidências identifica dependências da Phase 1.
