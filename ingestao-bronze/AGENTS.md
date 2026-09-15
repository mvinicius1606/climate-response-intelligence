# AGENTS.md — Ingestão Bronze

## 1. Finalidade

Este arquivo complementa o `AGENTS.md` da raiz com regras específicas da etapa:

```text
ingestao-bronze/
```

O **Prompt Inicial** define a ação atual, seu escopo, entregáveis, validações e quais documentações devem ser criadas ou modificadas.

Este arquivo não define a próxima tarefa da Bronze.

---

# 2. Responsabilidade da Bronze

A etapa Bronze é responsável pela obtenção e preservação dos dados provenientes de fontes externas.

De forma geral:

```text
Fonte externa
↓
extração
↓
metadata
↓
checksum
↓
storage
↓
manifest
```

Transformações analíticas, integração entre fontes, padronização de negócio, feature engineering e Machine Learning não pertencem à Bronze.

---

# 3. Estrutura do código

O código deve ser dividido por responsabilidades reais.

Estrutura conceitual:

```text
ingestao-bronze/
│
├── gatilhador.py
├── config/
├── src/
│   ├── models.py
│   ├── config_loader.py
│   ├── extractors.py
│   ├── metadata.py
│   ├── storage.py
│   ├── ingestion_service.py
│   └── logging_config.py
│
├── tests/
└── docs/
```

Essa estrutura é orientativa.

Não criar módulos vazios apenas para reproduzi-la.

Um novo arquivo deve existir quando houver uma responsabilidade clara que justifique sua separação.

---

# 4. Responsabilidades principais

## `gatilhador.py`

Ponto de entrada da aplicação.

Deve:

* receber a ação solicitada;
* carregar configuração inicial;
* configurar logging;
* iniciar o fluxo de ingestão;
* informar o resultado final da execução.

Não deve concentrar lógica de extração, armazenamento ou transformação.

---

## `config_loader.py`

Responsável por:

* carregar configurações;
* validar estrutura;
* fornecer configurações para os demais componentes.

Não deve realizar ingestão.

---

## `extractors.py`

Responsável pelo acesso às fontes externas.

Pode lidar com:

* API;
* HTTP;
* download direto;
* paginação;
* arquivos;
* scraping, quando explicitamente necessário.

O extractor deve se limitar à obtenção do dado.

---

## `metadata.py`

Responsável por informações de rastreabilidade, como:

* origem;
* URL;
* timestamp;
* formato;
* tamanho;
* checksum;
* identificador da execução;
* demais informações exigidas pelo manifest.

---

## `storage.py`

Responsável pela persistência.

Pode possuir implementações para:

```text
local
S3
```

O restante da aplicação deve depender da interface de storage e evitar acoplamento direto à AWS sempre que possível.

---

## `ingestion_service.py`

Responsável por coordenar o fluxo.

Exemplo:

```text
carregar configuração
↓
extrair
↓
gerar metadata
↓
calcular checksum
↓
persistir
↓
gerar manifest
↓
retornar resultado
```

O fluxo deve ser simples de ler.

---

# 5. Formato do código

Priorizar código:

* legível;
* explícito;
* modular;
* tipado quando útil;
* testável;
* com nomes descritivos;
* com funções pequenas o suficiente para possuir responsabilidade clara.

Evitar:

* funções gigantes;
* classes sem necessidade;
* abstrações prematuras;
* duplicação;
* `if` excessivamente aninhado;
* lógica escondida;
* comentários explicando código confuso em vez de melhorar o código.

Comentários devem explicar principalmente:

> por que algo existe

e não apenas repetir:

> o que a linha faz.

---

# 6. Separação de responsabilidades

Evitar componentes que misturem simultaneamente:

```text
download
+
tratamento
+
AWS
+
logging
+
regra de negócio
```

Preferir:

```text
extractor
→ obtém

metadata
→ descreve

storage
→ salva

service
→ coordena
```

A modularização deve facilitar entendimento e testes.

Não fragmentar o código apenas para aumentar o número de arquivos.

---

# 7. Configuração

Quando aplicável, fontes devem ser configuradas externamente, preferencialmente por arquivos em:

```text
config/
```

A configuração deve representar parâmetros, não lógica de programação.

Evitar colocar regras complexas dentro de YAML.

O código deve receber configurações como dependência sempre que possível.

---

# 8. Logging

Logging é parte importante da Bronze.

A execução deve possuir logs claros, detalhados e úteis para acompanhar o fluxo.

O logging deve ser configurado centralmente.

Preferência:

```text
src/logging_config.py
```

Os demais módulos devem apenas obter seu logger:

```python
import logging

logger = logging.getLogger(__name__)
```

Não configurar logging independentemente em cada módulo.

---

# 9. Estilo dos logs

Os logs podem utilizar **emojis** para facilitar leitura visual no terminal.

Os emojis devem complementar a mensagem, sem substituir informações textuais importantes.

Exemplos recomendados:

```text
🚀 início de execução
⚙️ configuração
🔎 pesquisa/verificação
🌐 chamada externa
📥 download
📄 arquivo
🧾 metadata
🔐 checksum
💾 persistência local
☁️ armazenamento S3
🔁 retry
⚠️ warning
❌ erro
✅ sucesso
🏁 conclusão
```

Exemplo:

```text
🚀 Iniciando ingestão | fonte=ibge_demografia | run_id=abc123
⚙️ Configuração carregada | fonte=ibge_demografia
🌐 Iniciando requisição | url=...
📥 Download concluído | bytes=152340
🔐 Checksum SHA-256 calculado
💾 Arquivo salvo localmente | path=...
🧾 Manifest criado | run_id=abc123
✅ Ingestão concluída | fonte=ibge_demografia
🏁 Execução finalizada | status=SUCCESS
```

---

# 10. Contexto nos logs

Sempre que útil, incluir campos como:

```text
run_id
source
dataset
file
url
attempt
status
duration
size
destination
```

Evitar mensagens vagas como:

```text
Funcionou.
```

Preferir:

```text
✅ Upload concluído | source=ana_hidroweb | destination=s3://...
```

---

# 11. Responsabilidade dos logs

Cada módulo deve registrar somente eventos que conhece.

Exemplo:

```text
extractor
→ sabe se o download funcionou

metadata
→ sabe se checksum/metadata foram gerados

storage
→ sabe se a persistência funcionou

ingestion_service
→ sabe se a ingestão completa funcionou

gatilhador
→ sabe se a execução solicitada terminou
```

`storage.py`, por exemplo, não deve registrar:

```text
✅ Pipeline completo com sucesso
```

porque não conhece o pipeline completo.

---

# 12. Níveis de logging

Utilizar os níveis de forma coerente.

### `DEBUG`

Detalhes úteis para investigação técnica.

### `INFO`

Fluxo normal da execução.

### `WARNING`

Problemas recuperáveis ou situações inesperadas que não impedem imediatamente a execução.

### `ERROR`

Falha que impede parte relevante da operação.

### `CRITICAL`

Utilizar somente para falhas realmente graves que impossibilitem a continuidade da execução ou representem risco importante.

---

# 13. Exceções

Não esconder erros.

Evitar:

```python
except Exception:
    pass
```

Quando uma exceção for relevante:

* adicionar contexto;
* registrar adequadamente;
* preservar o traceback quando necessário;
* propagar a exceção quando o componente não tiver responsabilidade para resolvê-la.

Exemplo:

```python
try:
    ...
except RequestException:
    logger.exception(
        "❌ Falha durante download | source=%s | url=%s",
        source,
        url,
    )
    raise
```

---

# 14. Retry

Quando uma fonte exigir retry:

* definir limite;
* registrar tentativa;
* diferenciar erro temporário de erro definitivo;
* evitar loops infinitos.

Exemplo:

```text
⚠️ Timeout na requisição | attempt=1/3
🔁 Nova tentativa em 2s
```

Após esgotar:

```text
❌ Download falhou após 3 tentativas
```

---

# 15. `run_id`

Sempre que uma ação representar uma execução de ingestão, preferir um identificador único de execução.

Exemplo:

```text
run_id=20260915T021530Z-a3f82c
```

O mesmo `run_id` deve acompanhar os logs e metadata relacionados àquela execução.

Isso facilita reconstruir:

> o que aconteceu naquela ingestão específica.

---

# 16. Secrets nos logs

Nunca registrar:

* AWS Access Key;
* AWS Secret Access Key;
* AWS Session Token;
* API keys;
* tokens;
* senhas;
* conteúdo de `.env`;
* headers de autenticação.

Se necessário registrar configuração, mascarar valores sensíveis.

---

# 17. Storage local e S3

O desenvolvimento pode utilizar storage local antes da integração real com S3.

O fluxo desejado é:

```text
ingestion_service
↓
storage.save(...)
```

e não:

```text
ingestion_service
↓
boto3 diretamente
```

Quando possível, permitir:

```text
LocalStorage
S3Storage
```

sem alterar a lógica central da ingestão.

---

# 18. Docker

A Bronze representa uma aplicação de ingestão.

Não criar um container diferente para cada módulo interno.

Em princípio:

```text
ingestao-bronze/
→ um Dockerfile
```

Docker deve empacotar a aplicação completa.

Separar containers somente quando existirem serviços realmente independentes e houver necessidade concreta.

---

# 19. Testes

Código novo deve ser testável.

Testes específicos da Bronze devem permanecer em:

```text
ingestao-bronze/tests/
```

Sempre que possível, testes unitários não devem depender diretamente de:

* internet real;
* AWS real;
* APIs reais;
* filesystem global.

Utilizar mocks, fixtures ou diretórios temporários quando apropriado.

Integrações reais devem ser executadas somente quando fizerem parte da validação definida no Prompt Inicial.

---

# 20. Documentação

A documentação não deve ser criada ou modificada automaticamente apenas porque uma ação ocorreu.

O **Prompt Inicial** deve definir quais documentos fazem parte daquela ação.

Exemplos:

```text
docs/fontes-de-dados.md
docs/arquitetura.md
docs/ingestao.md
docs/metadata-lineage.md
docs/testes.md
docs/decisoes.md
STATUS.md
README.md
```

O agente deve atualizar os documentos especificados no prompt seguindo as regras do `AGENTS.md` raiz.

Se a ação tornar uma documentação diretamente relacionada incorreta, o agente deve informar isso e agir conforme a autonomia concedida no Prompt Inicial.

---

# 21. Decisões

Quando o Prompt Inicial determinar registro em:

```text
docs/decisoes.md
```

a decisão deve ser registrada somente após a validação da ação.

O formato e as regras de autoria seguem o `AGENTS.md` raiz.

Não registrar decisões ainda não confirmadas como definitivas.

---

# 22. STATUS

Quando o Prompt Inicial determinar atualização de:

```text
STATUS.md
```

o estado deve refletir somente o que foi realmente validado.

Não marcar como concluído algo que:

* ainda não foi testado;
* depende de validação futura;
* existe apenas como estrutura;
* ainda possui falha conhecida que impede seu funcionamento.

---

# 23. Regra final

Na Bronze:

```text
Prompt Inicial
↓
define a ação

AGENTS raiz
↓
define o método global

AGENTS Bronze
↓
define padrão de implementação da ingestão

STATUS + docs + código
↓
fornecem contexto

Codex
↓
executa somente a ação autorizada

testes e validações
↓
confirmam o resultado

documentação indicada no prompt
↓
registra o trabalho validado
```

O código da Bronze deve permanecer:

* compreensível;
* observável;
* modular;
* testável;
* rastreável;
* simples de evoluir.

O logging deve permitir acompanhar claramente cada execução, utilizando mensagens detalhadas e emojis de forma consistente e profissional.

