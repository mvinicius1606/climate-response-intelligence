# AGENTS.md — Ingestão Bronze

## 1. Finalidade

Este arquivo define as regras específicas para desenvolvimento, manutenção e evolução da etapa:

```text
ingestao-bronze/
```

do projeto **Climate Response Intelligence**.

As regras globais definidas em:

```text
/AGENTS.md
```

continuam válidas e devem ser lidas antes deste arquivo.

Este documento complementa as regras globais com instruções relacionadas à:

* aquisição de dados;
* preservação de fontes originais;
* configuração declarativa;
* metadata;
* checksum;
* rastreabilidade;
* Data Lineage inicial;
* armazenamento Bronze;
* testes de ingestão;
* preparação das fontes que posteriormente serão utilizadas pela Silver.

---

# 2. Objetivo da etapa Bronze

A camada Bronze deve responder:

> Quais dados foram obtidos, de onde vieram, quando foram obtidos e como podemos comprovar que permanecem fiéis à fonte original?

A Bronze não possui responsabilidade por:

* limpeza analítica;
* padronização extensa;
* integração entre fontes;
* cálculo de indicadores;
* criação de features;
* classificação de vulnerabilidade;
* definição de ponto de colapso;
* Machine Learning;
* scoring;
* Decision Intelligence.

Essas responsabilidades pertencem às etapas posteriores.

A função da Bronze é preservar a evidência original necessária para que o restante do projeto seja:

* reproduzível;
* auditável;
* rastreável;
* confiável.

---

# 3. Contexto do MVP histórico

A primeira versão do projeto reconstruirá aproximadamente um mês da enchente de 2024 no Rio Grande do Sul.

Período inicial de referência:

```text
27/04/2024
↓
27/05/2024
```

Esse período poderá ser refinado posteriormente caso a análise histórica indique necessidade.

O objetivo é preservar dados suficientes para reconstruir:

```text
antes
↓
escalada
↓
contingência
↓
colapso
↓
recuperação inicial
```

A ingestão deve ser projetada para esse replay histórico, porém sem impedir evolução futura para processamento incremental ou contínuo.

---

# 4. Visão futura

A arquitetura da Bronze deve permitir que uma fonte inicialmente histórica possa futuramente passar a fornecer dados recorrentes.

Exemplo:

```text
Phase 1

dados históricos de 2024
↓
ingestão sob demanda
↓
S3 Bronze
```

e posteriormente:

```text
Phase 2

dados meteorológicos/hidrológicos atuais
↓
ingestão recorrente
↓
mesma estrutura Bronze
```

A evolução futura deve preferencialmente alterar o mecanismo de acionamento, e não reconstruir toda a lógica de ingestão.

---

# 5. Fontes de dados do MVP

O MVP da Bronze possui cinco grupos principais de informação.

## 5.1. Município e demografia

Fonte principal:

```text
IBGE — Censo Demográfico 2022
```

Dados de interesse:

* código IBGE do município;
* nome do município;
* população total;
* população por faixa etária;
* crianças;
* idosos;
* densidade populacional;
* sexo, quando relevante;
* características domiciliares necessárias para análises posteriores.

O código IBGE municipal deve ser tratado como a principal chave geográfica do projeto.

---

## 5.2. Vulnerabilidade

Fonte principal:

```text
IBGE — Censo Demográfico 2022
```

Dados de interesse:

* renda;
* saneamento;
* abastecimento de água;
* características de moradia;
* vulnerabilidade habitacional;
* composição etária;
* indicadores socioeconômicos adequados à granularidade municipal.

A Bronze deve preservar as tabelas originais.

A classificação ou cálculo de vulnerabilidade pertence à Silver.

---

## 5.3. Chuva e hidrologia

Fontes principais:

```text
ANA / HidroWeb
+
fontes pluviométricas oficiais utilizadas no projeto
```

Dados de interesse:

* estações;
* coordenadas;
* rio;
* chuva;
* nível dos rios;
* vazão;
* timestamps;
* metadata das estações;
* séries históricas necessárias ao período estudado;
* dados de referência utilizados futuramente para criar uma hidrometria base.

A Bronze não deve calcular:

```text
chuva_6h
chuva_24h
chuva_72h
delta_nivel
velocidade_subida
```

Esses cálculos pertencem à Silver ou Gold, de acordo com a modelagem definida.

---

## 5.4. Impacto e severidade

Fontes principais:

```text
Defesa Civil RS
S2ID
```

Dados de interesse:

* municípios afetados;
* população afetada;
* desalojados;
* desabrigados;
* feridos;
* óbitos, quando pertinentes;
* boletins;
* situação de emergência;
* calamidade pública;
* decretos;
* data e hora de publicação;
* data de reconhecimento;
* atualizações posteriores.

Esses dados serão utilizados posteriormente como:

* ground truth;
* referência institucional;
* validação histórica;
* construção de targets.

A Bronze não deve transformar automaticamente esses registros em `target` de Machine Learning.

---

## 5.5. Logística e infraestrutura

Fontes principais:

```text
Governo do Rio Grande do Sul
DAER
Defesa Civil
demais fontes oficiais adotadas pelo projeto
```

Dados de interesse:

* rodovia;
* trecho;
* km;
* município relacionado;
* bloqueio total;
* bloqueio parcial;
* ponte interditada;
* alagamento;
* deslizamento;
* rota alternativa;
* liberação de trecho;
* timestamp do boletim.

Essas informações permitirão reconstruir posteriormente:

```text
acessibilidade
↓
redução de rotas
↓
isolamento
↓
recuperação logística
```

A Bronze apenas preserva os registros originais.

---

# 6. Fontes que não fazem parte do MVP inicial

Não adicionar automaticamente novas fontes apenas porque podem ser úteis.

Neste primeiro ciclo, não priorizar:

* PEERS;
* doações;
* hospitais;
* CNES;
* medicamentos;
* hipertensão;
* diabetes;
* abrigos detalhados;
* dados individualizados de saúde;
* otimização avançada de rotas.

Essas fontes podem ser incorporadas posteriormente caso exista uma necessidade concreta.

Toda inclusão de nova fonte deve ser justificada em:

```text
docs/decisoes.md
```

---

# 7. Arquitetura config-driven

A ingestão deve seguir prioritariamente uma arquitetura declarativa.

Princípio:

```text
YAML
→ define O QUE deve ser ingerido

Python
→ define COMO realizar a ingestão
```

Adicionar uma nova fonte não deve resultar automaticamente em um novo pipeline independente.

Sempre verificar primeiro se a nova fonte pode utilizar componentes existentes.

---

# 8. Configuração por fonte

Cada fonte independente deve possuir sua própria configuração.

Exemplo conceitual:

```text
config/
├── ibge-demografia.yml
├── ibge-vulnerabilidade.yml
├── ana-hidroweb.yml
├── defesa-civil.yml
└── logistica-rs.yml
```

Evitar concentrar todas as fontes em um único arquivo YAML quando isso prejudicar:

* leitura;
* manutenção;
* validação;
* histórico;
* isolamento entre fontes.

---

# 9. Responsabilidade dos arquivos YAML

Arquivos YAML devem declarar apenas configurações.

Exemplos:

```yaml
nome: ana_hidroweb
tipo: api
formato: json

periodo:
  inicio: "2024-04-27"
  fim: "2024-05-27"

destino:
  prefixo: "bronze/ana/hidroweb"

ativo: true
```

Arquivos YAML não devem se transformar em uma linguagem de programação improvisada.

Não colocar neles:

* regras complexas;
* algoritmos;
* lógica condicional extensa;
* transformação analítica;
* código Python serializado.

---

# 10. Estrutura interna da ingestão

A arquitetura deve favorecer responsabilidades claras.

Estrutura conceitual:

```text
ingestao-bronze/
│
├── AGENTS.md
├── STATUS.md
│
├── config/
│
├── docs/
│   ├── ingestao.md
│   ├── arquitetura.md
│   ├── fontes-de-dados.md
│   ├── metadata-lineage.md
│   ├── decisoes.md
│   └── testes.md
│
├── src/
│   ├── models.py
│   ├── config_loader.py
│   ├── extractors.py
│   ├── metadata.py
│   ├── storage.py
│   └── ingestion_service.py
│
├── tests/
│
├── gatilhador.py
├── Dockerfile
└── requirements.txt
```

A estrutura pode evoluir se houver necessidade concreta.

Não criar arquivos ou abstrações vazias apenas para reproduzir esta árvore.

---

# 11. Responsabilidade dos módulos

## 11.1. `models.py`

Responsável por estruturas de dados utilizadas pela ingestão.

Exemplos:

* configuração de fonte;
* resultado de extração;
* metadata;
* manifest;
* resultado de execução.

Evitar concentrar comportamento complexo nesse módulo.

---

## 11.2. `config_loader.py`

Responsável por:

* localizar configurações;
* carregar YAML;
* validar estrutura;
* transformar configuração em objeto Python adequado.

Não deve executar ingestão.

---

## 11.3. `extractors.py`

Responsável pela comunicação com fontes externas.

Pode incluir mecanismos reutilizáveis para:

* HTTP;
* APIs;
* arquivos;
* downloads;
* ZIP;
* paginação.

Quando uma fonte exigir comportamento realmente particular, pode existir um extractor especializado.

Não criar um extractor específico se o comportamento já puder ser atendido por um componente genérico.

---

## 11.4. `metadata.py`

Responsável por gerar informações como:

* origem;
* URL;
* horário de coleta;
* período solicitado;
* nome da fonte;
* formato;
* tamanho;
* checksum;
* identificador da execução;
* demais informações de proveniência.

---

## 11.5. `storage.py`

Responsável por persistência.

Deve isolar operações relacionadas a:

* filesystem local, quando utilizado;
* Amazon S3;
* caminhos;
* chaves;
* upload;
* verificação de escrita.

Não deve conter regras de extração.

---

## 11.6. `ingestion_service.py`

Responsável por orquestrar o fluxo.

Deve permanecer simples e legível.

Fluxo esperado:

```text
carregar configuração
↓
extrair
↓
gerar metadata
↓
calcular checksum
↓
persistir dado bruto
↓
persistir manifest
↓
registrar resultado
```

Ao abrir esse arquivo, deve ser possível compreender o fluxo principal rapidamente.

---

## 11.7. `gatilhador.py`

Responsável por iniciar a ingestão.

Exemplos conceituais:

```bash
python gatilhador.py --fonte ana_hidroweb
```

ou:

```bash
python gatilhador.py --todas
```

O gatilho não deve concentrar lógica de negócio.

---

# 12. Preservação do formato original

A Bronze deve preservar o formato recebido da fonte sempre que possível.

Exemplos:

```text
JSON
→ JSON

CSV
→ CSV

XLSX
→ XLSX

ZIP
→ ZIP original quando relevante

PDF
→ PDF
```

Não converter arquivos apenas para padronizar a Bronze.

A normalização pertence à Silver.

---

# 13. Raw significa raw

A Bronze deve preservar o dado original com mínima interferência.

Permitido:

* download;
* descompressão quando necessária para acessar o conteúdo;
* organização de objetos;
* metadata;
* checksum;
* manifest;
* identificação de origem;
* identificação temporal.

Evitar:

* renomear colunas;
* corrigir tipos;
* preencher nulos;
* remover duplicatas;
* agregar;
* criar indicadores;
* padronizar municípios;
* converter códigos;
* fazer joins;
* aplicar regras de negócio.

Essas transformações pertencem à Silver.

---

# 14. Metadata separada dos dados

Metadata deve preferencialmente permanecer separada do arquivo original.

Exemplo:

```text
bronze/
└── ana/
    └── hidroweb/
        └── 2024-05-01/
            ├── dados.json
            └── manifest.json
```

O arquivo original não deve ser alterado apenas para incorporar metadata.

---

# 15. Checksum

Todo objeto relevante armazenado na Bronze deve possuir checksum.

Preferência:

```text
SHA-256
```

O checksum funciona como uma impressão digital do arquivo.

Ele deve permitir detectar:

* corrupção;
* alteração inesperada;
* downloads diferentes;
* duplicações;
* mudança silenciosa na origem.

---

# 16. Manifest de ingestão

Cada ingestão deve produzir metadata suficiente para reconstruir a execução.

Exemplo conceitual:

```json
{
  "source": "ana_hidroweb",
  "retrieved_at": "...",
  "period_start": "2024-04-27",
  "period_end": "2024-05-27",
  "original_url": "...",
  "format": "json",
  "checksum_sha256": "...",
  "size_bytes": 12345
}
```

Não copiar literalmente esse schema sem avaliar as necessidades reais.

---

# 17. Dois tempos diferentes

Quando a fonte permitir, preservar a distinção entre:

```text
occurred_at
```

e:

```text
observed_at
```

`occurred_at` significa:

> quando o evento ocorreu.

`observed_at` significa:

> quando aquela informação se tornou disponível ou foi publicada.

Exemplo:

```text
rodovia fechou:
08:00

boletim publicado:
11:00
```

Esses horários não devem ser tratados como equivalentes.

Essa informação será fundamental para reconstruções históricas sem Data Leakage.

---

# 18. `retrieved_at`

A ingestão também deve registrar:

```text
retrieved_at
```

que representa:

> quando o projeto obteve aquela informação da fonte.

Portanto, podem existir três tempos distintos:

```text
occurred_at
→ evento real

observed_at
→ publicação/disponibilidade

retrieved_at
→ momento da ingestão
```

Preservar essa distinção sempre que a fonte permitir.

---

# 19. Point-in-time correctness

A Bronze deve preservar informação suficiente para que a Silver consiga reconstruir:

> o que poderia ser conhecido em determinado momento.

Não sobrescrever versões históricas quando uma fonte publica atualizações.

Exemplo:

```text
Boletim 09h
Boletim 12h
Boletim 18h
```

devem permanecer como versões distintas quando representarem estados diferentes.

---

# 20. Imutabilidade da Bronze

Objetos Bronze devem ser tratados como imutáveis.

Após armazenados e validados:

* não sobrescrever;
* não editar manualmente;
* não corrigir internamente;
* não substituir silenciosamente.

Caso a fonte publique uma nova versão:

```text
nova versão
→ novo objeto Bronze
```

A relação entre versões pode ser registrada por metadata.

---

# 21. Idempotência

Sempre que possível, executar a mesma ingestão novamente não deve gerar duplicações desnecessárias.

A estratégia pode utilizar:

* checksum;
* identificador de fonte;
* período;
* URL;
* timestamp;
* chave determinística.

A idempotência não deve apagar versões legítimas diferentes.

---

# 22. Estratégia para grandes volumes

Ao extrair dados, priorizar nesta ordem:

```text
1. dataset completo oficial
2. endpoint com paginação
3. download por lote
4. loop por município
```

Evitar centenas de chamadas individuais quando a fonte disponibilizar uma forma eficiente de recuperar o conjunto completo.

---

# 23. Paginação

Quando APIs forem paginadas:

* respeitar paginação oficial;
* validar término;
* registrar número de páginas;
* detectar páginas ausentes;
* aplicar retry quando necessário;
* evitar loops infinitos.

O resultado final deve permitir verificar se a extração ficou completa.

---

# 24. Rate limiting e retry

Extratores HTTP devem lidar adequadamente com:

* timeout;
* falhas transitórias;
* HTTP 429;
* HTTP 5xx;
* interrupções temporárias.

Retry deve possuir limite.

Não criar loops infinitos de tentativa.

Quando possível, utilizar espera progressiva.

---

# 25. Falhas parciais

Uma ingestão com múltiplos arquivos pode falhar parcialmente.

O sistema deve registrar claramente:

* itens obtidos;
* itens que falharam;
* erros;
* quantidade esperada;
* quantidade concluída.

Não marcar a ingestão como plenamente concluída quando existirem falhas não resolvidas.

---

# 26. Logging

A ingestão deve produzir logs úteis.

Registrar, quando pertinente:

* início;
* fonte;
* período;
* número de registros ou arquivos;
* chamadas relevantes;
* retries;
* sucesso;
* falhas;
* destino;
* checksum;
* duração.

Não registrar:

* secrets;
* tokens;
* credenciais;
* informações sensíveis.

---

# 27. Associação entre fontes e municípios

O código IBGE municipal deve ser a chave geográfica de referência do projeto.

Entretanto, fontes externas podem possuir identificadores diferentes.

Exemplo:

```text
ANA
→ código próprio

IBGE
→ codigo_ibge_municipio
```

A Bronze deve preservar os identificadores originais.

A conversão e conformação das chaves pertencem à Silver.

---

# 28. Hidrologia e geografia

Não assumir automaticamente que:

> a estação hidrológica mais próxima geograficamente representa o município.

Preservar metadata suficiente para permitir análise posterior de:

* rio;
* bacia;
* sub-bacia;
* coordenadas;
* montante;
* jusante;
* relação espacial.

A associação hidrológica correta será definida posteriormente.

---

# 29. Qualidade da fonte na Bronze

A Bronze pode registrar características observáveis sobre a ingestão, como:

* disponibilidade;
* completude do download;
* checksum;
* tamanho;
* formato;
* erros.

Não deve calcular o Data Quality analítico da Silver.

Exemplo:

```text
download concluído
→ Bronze

dados municipais faltantes
→ Silver / Data Quality
```

---

# 30. Data Lineage inicial

Para cada objeto Bronze deve ser possível responder:

```text
de onde veio?
quando foi obtido?
qual fonte?
qual URL?
qual período?
qual arquivo?
qual checksum?
qual execução?
```

Esse é o primeiro nível de Data Lineage do projeto.

---

# 31. Segurança

Nunca versionar:

* `.env`;
* AWS Access Key;
* AWS Secret Key;
* tokens;
* API keys;
* senhas.

Usar:

```text
.env.example
```

apenas com nomes de variáveis e valores fictícios.

---

# 32. Credenciais AWS

O código deve receber credenciais por mecanismos adequados.

Não inserir credenciais diretamente:

```python
aws_access_key_id="..."
```

no código.

Preferir:

* variáveis de ambiente;
* AWS profiles;
* IAM Roles;
* GitHub Secrets quando aplicável.

---

# 33. Estrutura S3

A estrutura de armazenamento deve favorecer:

* origem;
* dataset;
* versão;
* período;
* rastreabilidade.

Exemplo conceitual:

```text
s3://bucket/
└── bronze/
    ├── ibge/
    ├── ana/
    ├── defesa-civil/
    └── logistica/
```

Não criar particionamentos excessivamente complexos sem necessidade.

---

# 34. Testes locais da Bronze

Os testes específicos desta etapa devem permanecer em:

```text
ingestao-bronze/tests/
```

Eles podem abranger:

* configuração;
* YAML loader;
* validação de models;
* extractors;
* paginação;
* retry;
* metadata;
* checksum;
* storage;
* idempotência;
* manifests;
* orchestration.

---

# 35. Testes sem dependências externas desnecessárias

Testes unitários não devem depender diretamente de:

* AWS real;
* APIs reais;
* internet;
* filesystem global.

Utilizar:

* mocks;
* fixtures;
* arquivos temporários;
* responses controladas.

Testes de integração podem utilizar serviços externos quando houver justificativa e configuração adequada.

---

# 36. Testes de contrato

Mudanças que alterem a estrutura entregue à Silver devem ser consideradas mudanças de contrato.

Quando aplicável, validar:

```text
Bronze
→ Silver
```

em:

```text
/testes/contratos/
```

conforme regras globais.

---

# 37. Documentação de testes

A estratégia e resultados dos testes Bronze devem ser documentados em:

```text
docs/testes.md
```

Atualizar quando houver mudanças relevantes em:

* cobertura;
* abordagem;
* contratos;
* mocks;
* cenários;
* critérios de aprovação.

---

# 38. Arquivo `STATUS.md`

Antes de iniciar qualquer tarefa na Bronze, consultar:

```text
STATUS.md
```

Componentes concluídos não devem ser reconstruídos sem necessidade.

Exemplo:

```text
config loader — CONCLUÍDO
checksum — CONCLUÍDO
storage S3 — CONCLUÍDO
ANA — PENDENTE
```

Ao adicionar ANA, reutilizar os componentes concluídos.

Não reconstruir o core da ingestão.

---

# 39. `docs/decisoes.md`

Toda ação relevante nesta etapa deve ser registrada em:

```text
docs/decisoes.md
```

Exemplos:

* escolha de fonte;
* método de extração;
* mudança de endpoint;
* criação de extractor especializado;
* formato de metadata;
* estratégia de particionamento;
* política de idempotência;
* alteração de estrutura S3;
* tratamento de paginação;
* abandono de uma fonte;
* substituição por fonte melhor.

Registrar:

```text
contexto
↓
decisão
↓
motivo
↓
alternativas
↓
impacto
↓
limitações
```

---

# 40. Fontes de dados

Manter:

```text
docs/fontes-de-dados.md
```

atualizado.

Para cada fonte registrar, quando disponível:

* nome;
* instituição responsável;
* URL;
* tipo de acesso;
* período;
* granularidade;
* formato;
* identificadores;
* licença ou termos;
* limitações;
* estratégia de ingestão;
* status no projeto.

---

# 41. Documentação de arquitetura

Mudanças relevantes no funcionamento da ingestão devem atualizar:

```text
docs/arquitetura.md
```

A documentação deve explicar:

* componentes;
* responsabilidades;
* fluxo;
* integração com S3;
* metadata;
* idempotência;
* tratamento de erros.

---

# 42. README global

Sempre verificar se uma alteração relevante da Bronze modifica o conteúdo apresentado em:

```text
/README.md
```

Exemplos:

* nova fonte concluída;
* alteração arquitetural;
* mudança importante de escopo;
* ingestão Bronze concluída;
* mudança do período histórico;
* novo resultado relevante.

---

# 43. CHANGELOG global

Toda mudança relevante da Bronze deve produzir entrada no:

```text
/CHANGELOG.md
```

de acordo com as regras globais.

---

# 44. Adição de uma nova fonte

Antes de implementar uma nova fonte, seguir:

```text
1. verificar se está no escopo
2. registrar fonte
3. analisar formato/acesso
4. verificar extractor existente
5. criar YAML
6. implementar apenas o necessário
7. testar
8. validar objeto Bronze
9. atualizar STATUS
10. atualizar decisoes
11. atualizar docs
12. verificar README
13. atualizar CHANGELOG
```

---

# 45. Regra de reutilização

Uma nova fonte não deve gerar automaticamente um novo pipeline.

Priorizar:

```text
nova configuração
↓
extractor existente
↓
core existente
```

Antes de:

```text
novo pipeline
+
novo código duplicado
+
nova arquitetura
```

---

# 46. Quando criar um extractor especializado

Criar extractor específico somente quando houver necessidade concreta.

Exemplos:

* autenticação diferente;
* protocolo próprio;
* paginação incomum;
* arquivo ZIP complexo;
* endpoint com comportamento particular;
* scraping inevitável;
* PDF estruturado que exija tratamento especial.

Mesmo nesse caso, o extractor deve retornar um resultado compatível com o contrato comum da ingestão.

---

# 47. Ordem recomendada de implementação das fontes

Para reduzir risco, implementar progressivamente.

Ordem conceitual recomendada:

```text
1. IBGE
↓
2. ANA / HidroWeb
↓
3. Defesa Civil
↓
4. Logística
↓
5. demais fontes aprovadas
```

A primeira fonte valida a arquitetura.

A segunda deve demonstrar reutilização.

As seguintes devem exigir alterações progressivamente menores no core.

---

# 48. Critério de maturidade da arquitetura

A arquitetura está funcionando bem quando adicionar uma nova fonte exige principalmente:

```text
novo YAML
+
eventual extractor especializado pequeno
```

e não:

```text
alteração em vários componentes centrais
+
duplicação de código
+
novo pipeline completo
```

Caso cada nova fonte exija mudanças extensas, revisar o acoplamento antes de continuar expandindo.

---

# 49. Automação futura

No MVP histórico:

```text
ingestão sob demanda
```

é suficiente.

Não adicionar automaticamente:

* Airflow;
* Kafka;
* streaming;
* scheduler complexo;
* Lambda recorrente;
* EventBridge;
* infraestrutura distribuída.

Na fase futura, um scheduler poderá chamar o mesmo serviço de ingestão.

---

# 50. Docker

A ingestão deve poder ser executada em ambiente reproduzível.

O `Dockerfile` deve:

* utilizar imagem adequada;
* instalar apenas dependências necessárias;
* evitar secrets;
* executar a aplicação de forma previsível.

Não adicionar complexidade de containerização sem necessidade.

---

# 51. Dependências

Antes de adicionar biblioteca:

1. verificar necessidade;
2. verificar se dependência existente atende;
3. avaliar manutenção;
4. registrar decisão quando relevante.

Evitar dependências grandes para resolver problemas pequenos.

---

# 52. Critério de conclusão de uma fonte

Uma fonte só pode ser marcada como concluída quando:

* configuração estiver criada;
* extração funcionar;
* erros principais forem tratados;
* dados originais forem preservados;
* metadata estiver disponível;
* checksum estiver calculado quando aplicável;
* armazenamento estiver validado;
* testes relevantes passarem;
* `docs/fontes-de-dados.md` estiver atualizado;
* `docs/testes.md` estiver atualizado quando necessário;
* `docs/decisoes.md` possuir o registro;
* `STATUS.md` estiver atualizado;
* README raiz tiver sido verificado;
* CHANGELOG tiver sido atualizado.

---

# 53. Critério de conclusão da etapa Bronze

A Bronze do MVP pode ser considerada concluída quando as fontes aprovadas do escopo estiverem ingeridas e for possível responder:

```text
qual dado foi obtido?
↓
de qual instituição?
↓
de qual endpoint/arquivo?
↓
qual período?
↓
quando foi publicado?
↓
quando foi coletado?
↓
qual seu checksum?
↓
onde está armazenado?
↓
qual execução produziu o objeto?
```

Além disso:

* ingestões devem ser reproduzíveis;
* componentes comuns devem estar testados;
* falhas devem ser observáveis;
* STATUS deve refletir o estado real;
* documentação deve estar sincronizada.

---

# 54. Regra final da Bronze

Antes de implementar:

```text
Prompt
↓
AGENTS raiz
↓
AGENTS Bronze
↓
STATUS
↓
fontes-de-dados
↓
decisões
↓
arquitetura
↓
código existente
```

Durante:

```text
preservar
↓
reutilizar
↓
extrair
↓
rastrear
↓
armazenar
↓
testar
```

Depois:

```text
validar
↓
documentar
↓
STATUS
↓
DECISÕES
↓
testes
↓
README raiz
↓
CHANGELOG
```

A Bronze deve permanecer simples, rastreável e confiável.

Sua função não é tornar o dado inteligente.

Sua função é garantir que todas as etapas seguintes consigam confiar na origem da informação utilizada.

