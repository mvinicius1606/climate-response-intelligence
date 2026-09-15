# Changelog

## 15/09/2026 — Correções após vistoria da Bronze

- Rejeição de respostas incompatíveis com JSON, ZIP e PDF sem transformação do original.
- Recuperação de manifests ausentes com timestamp original, comparação de configuração e proteção contra sobrescrita.
- Releitura do S3 para conferir tamanho, SHA-256 e manifest; pares existentes compatíveis são preservados.
- Dez testes offline aprovados. HEAD do bucket funcionou; carga real interrompida por HTTP 403 na primeira fonte IBGE, sem uploads.
## 15/09/2026 — Primeira implementação da ingestão Bronze

- Implementado o fluxo funcional das oito fontes YAML existentes: cinco IBGE, uma INMET e duas RS, com nove arquivos brutos por execução completa.
- Adicionados manifests baseados na configuração, metadata de aquisição e SHA-256, com envio ao S3 protegido contra sobrescrita.
- Preservados JSON, ZIP e PDF originais, incluindo os campos ausentes do INMET.
- Oito testes offline aprovados; carga real e permissões do bucket continuam pendentes.
- Documentados execução, arquitetura, decisões, estado e limitações. Nenhuma etapa Silver, Gold ou App foi implementada.
