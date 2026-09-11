# Política de dados

Dados Bronze reais ficam no AWS S3 e não são versionados. O `.gitignore` bloqueia `data/`, exceto esta política e fixtures opcionais em `samples/`.

Permitido: documentação, schemas, contratos, manifests sem segredos e fixtures pequenas, sintéticas ou redistribuíveis, com proveniência e licença.

Proibido: extratos completos, datasets Silver/Gold gerados, credenciais, tokens, dados pessoais ou dados sem termos verificados.

Nunca limpe manualmente um objeto Bronze. Preserve os bytes, calcule SHA-256, registre a versão e faça transformações reproduzíveis downstream.
