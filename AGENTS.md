# AGENTS.md

## 1. Finalidade

Este arquivo define as regras globais de desenvolvimento, documentação, organização, manutenção e trabalho assistido por agentes no projeto **Climate Response Intelligence**.

As instruções deste arquivo se aplicam a todo o repositório.

Cada uma das quatro etapas principais do projeto possui também um `AGENTS.md` próprio, responsável por complementar estas regras com orientações específicas daquela etapa.

A hierarquia conceitual de instruções é:

```text
Prompt atual
↓
AGENTS.md da raiz
↓
AGENTS.md da etapa
↓
STATUS.md da etapa
↓
documentação da etapa
↓
código existente
↓
histórico e decisões
```

O agente deve compreender o estado atual antes de realizar alterações.

---

# 2. Idioma do projeto

O projeto deve ser desenvolvido prioritariamente em **português brasileiro**.

Devem permanecer em inglês os termos técnicos, ferramentas, comandos e conceitos cujo uso em inglês seja padrão no contexto profissional.

Exemplos:

* Python;
* SQL;
* dbt;
* Docker;
* GitHub Actions;
* Machine Learning;
* Data Quality;
* Data Lineage;
* Data Lake;
* Bronze;
* Silver;
* Gold;
* staging;
* models;
* tests;
* features;
* scoring;
* API;
* endpoint;
* commit;
* pull request.

Não traduzir termos técnicos apenas para manter uniformidade linguística.

A prioridade é utilizar a forma mais natural e reconhecida no mercado brasileiro.

---

# 3. Estilo de escrita e documentação

A documentação deve seguir uma estrutura próxima à utilizada em trabalhos acadêmicos e relatórios técnicos.

A linguagem deve ser:

* formal;
* natural;
* clara;
* objetiva;
* explicativa;
* profissional;
* agradável de ler.

Evitar linguagem excessivamente complexa ou artificial.

O texto deve utilizar conectivos e apresentar continuidade lógica entre os assuntos.

Sempre que relevante, explicar:

1. o contexto;
2. o problema;
3. a solução adotada;
4. como a solução funciona;
5. por que essa solução foi escolhida;
6. suas limitações;
7. possíveis evoluções.

Evitar documentação composta somente por listas desconectadas.

---

# 4. Estrutura da documentação

Os documentos devem ser organizados por tópicos e subtópicos hierárquicos.

Exemplo:

```text
1. Assunto principal

1.1. Contexto

1.2. Arquitetura

1.3. Implementação

1.4. Decisões

1.5. Limitações
```

Documentos extensos devem possuir **sumário**.

Documentos pequenos não precisam possuir sumário apenas para cumprir formalidade.

A profundidade da estrutura deve acompanhar a complexidade real do assunto.

---

# 5. Estrutura global do projeto

O projeto é dividido em quatro etapas principais.

```text
climate-response-intelligence/
│
├── ingestao-bronze/
├── etl-silver/
├── inteligencia-gold/
├── app/
├── testes/
│
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── ROADMAP.md
└── demais arquivos globais
```

Cada etapa possui sua própria pasta mãe e deve concentrar os componentes relacionados àquela responsabilidade.

A pasta `testes/` da raiz possui responsabilidade transversal e não representa uma quinta etapa do pipeline.

---

# 6. As quatro etapas

## 6.1. `ingestao-bronze/`

Responsável por:

* obtenção dos dados externos;
* integração com fontes;
* metadata;
* checksum;
* Data Lineage inicial;
* rastreabilidade;
* armazenamento na camada Bronze.

---

## 6.2. `etl-silver/`

Responsável por:

* transformação;
* tipagem;
* padronização;
* integração entre fontes;
* Data Quality;
* validações;
* modelagem dos dados confiáveis;
* processamento dbt quando aplicável.

---

## 6.3. `inteligencia-gold/`

Responsável por:

* indicadores;
* feature engineering;
* scoring;
* algoritmos;
* modelos analíticos;
* Machine Learning;
* Decision Intelligence;
* explicabilidade.

---

## 6.4. `app/`

Responsável pela apresentação e interação com o usuário.

A aplicação não deve concentrar regras de negócio pertencentes às outras camadas.

---

# 7. Estrutura mínima de cada etapa

Cada pasta mãe deve possuir, quando aplicável:

```text
etapa/
│
├── AGENTS.md
├── STATUS.md
│
├── docs/
│   ├── decisoes.md
│   ├── testes.md
│   └── demais documentações
│
├── tests/
│
└── implementação da etapa
```

Os arquivos e diretórios possuem responsabilidades diferentes.

---

# 8. Papel do `AGENTS.md`

O `AGENTS.md` define:

> Como o agente deve trabalhar.

O `AGENTS.md` raiz contém as regras globais.

O `AGENTS.md` de cada etapa contém somente regras específicas daquela área.

Exemplos:

```text
ingestao-bronze/AGENTS.md
→ regras de ingestão

etl-silver/AGENTS.md
→ regras de dbt e Data Quality

inteligencia-gold/AGENTS.md
→ regras de scoring, algoritmos e ML

app/AGENTS.md
→ regras da interface
```

Evitar copiar todo o conteúdo do `AGENTS.md` raiz para os arquivos locais.

Os arquivos locais devem complementar as regras gerais.

---

# 9. Papel do `STATUS.md`

O `STATUS.md` representa:

> Qual é o estado atual da etapa.

Ele deve indicar claramente:

* componentes concluídos;
* componentes em desenvolvimento;
* componentes pendentes;
* componentes planejados;
* data da última atualização;
* data da última validação relevante.

Exemplo:

```text
# Status da Ingestão Bronze

Status geral: EM DESENVOLVIMENTO

Última atualização: 12/09/2026 16:40
Última validação: 12/09/2026 16:30

## Componentes

Arquitetura base — CONCLUÍDA
Loader YAML — CONCLUÍDO
Metadata — CONCLUÍDO
Storage S3 — CONCLUÍDO
IBGE População — CONCLUÍDO
IBGE Renda — PENDENTE
Defesa Civil — PENDENTE
```

O `STATUS.md` não é histórico.

Ele deve representar somente o estado atual.

---

# 10. Componentes concluídos

Componentes marcados como:

```text
CONCLUÍDO
```

não devem ser reconstruídos sem necessidade.

Antes de alterar um componente concluído, o agente deve:

1. verificar o motivo da alteração;
2. inspecionar a implementação existente;
3. preservar as partes funcionais;
4. realizar alterações incrementais;
5. documentar a justificativa.

`CONCLUÍDO` significa:

> Não reconstruir.

Não significa:

> Nunca modificar.

Exemplo:

Se a arquitetura Bronze estiver concluída e uma nova fonte precisar ser adicionada, o agente deve utilizar a arquitetura existente em vez de reconstruí-la.

---

# 11. Papel de `docs/decisoes.md`

Cada etapa deve possuir:

```text
docs/decisoes.md
```

Esse documento responde:

> O que foi decidido, para quê e por quê?

Toda ação relevante realizada naquela etapa deve gerar uma entrada em `decisoes.md`.

Isso permite compreender não apenas o estado final do projeto, mas também o raciocínio por trás de sua construção.

Cada registro deve informar, quando aplicável:

* data;
* ação realizada;
* decisão tomada;
* problema ou necessidade;
* solução escolhida;
* motivo da escolha;
* alternativas consideradas;
* impacto esperado;
* possíveis limitações.

Exemplo:

```markdown
## Uso de configuração YAML por fonte

**Data:** 12/09/2026

### Contexto

A ingestão utilizará aproximadamente cinco fontes públicas diferentes.

### Decisão

Cada fonte possuirá seu próprio arquivo YAML de configuração.

### Motivo

A separação permite adicionar novas fontes sem modificar o núcleo do serviço de ingestão.

### Alternativas consideradas

Manter todas as fontes dentro de um único arquivo Python.

### Motivo da rejeição

Essa abordagem aumentaria o acoplamento e repetiria um problema observado anteriormente em projetos com arquivos de ingestão extensos.
```

---

# 12. Decisões de continuidade

Nem toda ação exige uma nova arquitetura.

Mesmo assim, se uma ação relevante mantiver uma decisão anterior, registrar brevemente essa continuidade.

Exemplo:

```markdown
## Inclusão da fonte Defesa Civil

**Data:** 13/09/2026

A nova fonte foi integrada utilizando a arquitetura declarativa existente.

Não foi necessária alteração estrutural no serviço de ingestão.

A decisão foi manter o padrão atual por já atender adequadamente ao novo dataset.
```

Dessa forma, `decisoes.md` também demonstra que a ausência de mudança arquitetural foi uma escolha consciente.

---

# 13. Papel do `CHANGELOG.md`

O `CHANGELOG.md` localizado na raiz representa:

> O que mudou no projeto ao longo do tempo.

Ele possui escopo global.

Cada ação relevante no projeto deve gerar uma entrada contendo:

* título;
* data;
* hora;
* descrição da mudança.

Exemplo:

```markdown
## Implementação da ingestão IBGE População

**Data:** 12/09/2026  
**Hora:** 17:15

Foi implementada a primeira fonte oficial da camada Bronze utilizando configuração YAML, extração HTTP, geração de metadata e armazenamento no Amazon S3.

Também foram atualizados os testes, documentação da ingestão, STATUS da etapa e README principal.
```

---

# 14. Diferença entre STATUS, DECISÕES e CHANGELOG

Esses arquivos não devem ser tratados como equivalentes.

```text
STATUS.md
→ onde estamos agora

docs/decisoes.md
→ por que estamos fazendo dessa forma

CHANGELOG.md
→ o que mudou ao longo do tempo
```

Exemplo:

```text
STATUS:
IBGE População — CONCLUÍDO

DECISÕES:
A fonte IBGE foi integrada utilizando configuração YAML porque...

CHANGELOG:
12/09/2026 17:15 — Implementada ingestão IBGE População.
```

---

# 15. Fluxo obrigatório de leitura para agentes

Antes de executar uma tarefa, o agente deve seguir esta sequência.

## 15.1. Entender o pedido

Ler o prompt atual e identificar:

* objetivo;
* etapa envolvida;
* escopo;
* restrições;
* critério de conclusão.

---

## 15.2. Ler as regras globais

Consultar:

```text
/AGENTS.md
```

---

## 15.3. Identificar a etapa responsável

Exemplo:

```text
ingestão
→ ingestao-bronze/

transformação
→ etl-silver/

inteligência
→ inteligencia-gold/

interface
→ app/
```

---

## 15.4. Ler as regras locais

Consultar:

```text
etapa/AGENTS.md
```

antes de modificar arquivos da etapa.

---

## 15.5. Consultar o estado atual

Ler:

```text
etapa/STATUS.md
```

e identificar:

* o que já está concluído;
* o que está em andamento;
* o que ainda está pendente.

Não reconstruir componentes concluídos sem necessidade.

---

## 15.6. Consultar documentação relevante

Ler somente os documentos necessários para compreender a tarefa.

Evitar carregar documentação não relacionada sem necessidade.

---

## 15.7. Inspecionar o código existente

O agente deve verificar a implementação real antes de escrever código novo.

O código executável representa a **verdade operacional** do sistema.

Quando documentação e código divergirem, investigar a divergência antes de assumir qual está correto.

---

## 15.8. Consultar decisões anteriores

Antes de realizar mudanças arquiteturais ou estruturais, consultar:

```text
etapa/docs/decisoes.md
```

para evitar contradizer decisões anteriores sem necessidade.

---

## 15.9. Consultar o CHANGELOG quando necessário

O `CHANGELOG.md` deve ser utilizado para compreender:

* evolução histórica;
* momento em que componentes foram adicionados;
* grandes alterações anteriores.

Ele não deve ser utilizado como única fonte para determinar o estado atual.

---

# 16. Fluxo obrigatório de execução

Após compreender o contexto, o agente deve:

```text
entender
↓
inspecionar
↓
implementar
↓
testar
↓
validar
↓
documentar
↓
atualizar status
↓
registrar decisão
↓
atualizar README
↓
atualizar CHANGELOG
```

---

# 17. Fluxo obrigatório de atualização

Ao concluir uma ação relevante, verificar nesta ordem:

## 17.1. Código

A implementação foi realizada corretamente?

---

## 17.2. Testes

Os testes relevantes foram executados?

---

## 17.3. Documentação local

A documentação da etapa continua correta?

---

## 17.4. STATUS

O estado atual mudou?

Se sim:

```text
etapa/STATUS.md
```

deve ser atualizado.

---

## 17.5. Decisões

Registrar a ação e o raciocínio correspondente em:

```text
etapa/docs/decisoes.md
```

---

## 17.6. README raiz

Verificar obrigatoriamente se:

```text
README.md
```

precisa ser atualizado.

---

## 17.7. CHANGELOG

Registrar a mudança relevante no:

```text
CHANGELOG.md
```

---

# 18. README raiz

O `README.md` raiz é a **porta de entrada do projeto**.

Ele deve funcionar como:

* apresentação;
* resumo;
* visão executiva;
* índice de navegação.

O README não deve conter toda a documentação técnica.

Ele deve apresentar resumidamente:

1. problema;
2. proposta;
3. arquitetura;
4. etapas;
5. estado atual;
6. tecnologias principais;
7. resultados;
8. links para documentação detalhada.

---

# 19. README como mapa documental

O README deve possuir links diretos para as documentações principais.

Exemplo:

```text
README
│
├── Bronze
│   └── ingestao-bronze/docs/
│
├── Silver
│   └── etl-silver/docs/
│
├── Gold
│   └── inteligencia-gold/docs/
│
└── Aplicação
    └── app/docs/
```

O leitor deve conseguir começar pelo README e aprofundar progressivamente o conhecimento.

---

# 20. Sincronização obrigatória do README

Sempre que uma documentação relevante for:

* criada;
* removida;
* renomeada;
* reorganizada;
* significativamente alterada;

verificar se o README raiz precisa ser atualizado.

Também atualizar o README quando houver mudança relevante em:

* arquitetura;
* status;
* funcionalidades;
* resultados;
* escopo;
* nomenclatura;
* etapas.

Não deixar o README representar uma versão antiga do projeto.

---

# 21. Estado real versus planejamento

Diferenciar claramente:

```text
✅ Implementado
🚧 Em desenvolvimento
📋 Planejado
🔮 Futuro
```

Nunca apresentar como implementado algo que existe somente no planejamento.

A documentação deve refletir o estado real do projeto.

---

# 22. Preservação do trabalho existente

Antes de modificar qualquer componente:

1. inspecionar arquivos existentes;
2. verificar `STATUS.md`;
3. consultar decisões anteriores;
4. identificar componentes funcionais;
5. preservar soluções válidas.

Não reescrever componentes inteiros apenas porque outra solução parece mais elegante.

Refatorações devem possuir necessidade concreta.

---

# 23. Escopo das tarefas

O agente deve permanecer dentro do escopo solicitado.

Não utilizar uma tarefa pequena como oportunidade para:

* reorganizar outras pastas;
* alterar arquitetura global;
* adicionar ferramentas;
* trocar bibliotecas;
* refatorar componentes não relacionados.

Melhorias adicionais podem ser registradas como recomendação ou pendência.

---

# 24. Dependências

Não adicionar uma nova biblioteca, framework, serviço ou ferramenta sem necessidade concreta.

Antes de adicionar dependências:

1. verificar se já existe solução no projeto;
2. verificar se Python ou ferramenta atual já atende;
3. avaliar impacto;
4. justificar a decisão em `decisoes.md`.

---

# 25. Simplicidade arquitetural

Quando houver múltiplas soluções possíveis, priorizar nesta ordem:

1. correção;
2. clareza;
3. manutenção;
4. testabilidade;
5. simplicidade;
6. performance quando necessária;
7. sofisticação arquitetural.

Evitar overengineering.

---

# 26. Separação de responsabilidades

Código deve possuir responsabilidades claras.

Evitar:

* arquivos excessivamente grandes;
* classes responsáveis por muitas funções independentes;
* repetição significativa;
* forte acoplamento entre componentes.

Quando um arquivo crescer significativamente, avaliar se existem responsabilidades distintas que justificam refatoração.

---

# 27. Testabilidade

Código novo deve ser criado de forma testável.

Sempre que possível, separar:

* acesso externo;
* regras de negócio;
* transformação;
* armazenamento;
* configuração.

Evitar funções que dependam simultaneamente de:

```text
API real
+
AWS
+
filesystem
+
regra de negócio
```

quando essas dependências puderem ser isoladas.

---

# 28. Estratégia global de testes

Os testes devem acompanhar a responsabilidade do componente testado.

A estratégia adotada é híbrida:

```text
testes específicos
→ permanecem dentro da própria etapa

testes transversais
→ permanecem na pasta /testes da raiz
```

O objetivo é preservar a propriedade dos testes locais sem perder a visão sistêmica do projeto.

---

# 29. Testes específicos de cada etapa

Cada uma das quatro etapas deve possuir uma pasta de testes própria quando houver código ou comportamento testável.

Exemplos:

```text
ingestao-bronze/tests/
etl-silver/tests/
inteligencia-gold/tests/
app/tests/
```

Esses diretórios devem conter a implementação real dos testes específicos daquela etapa.

Exemplos:

### Bronze

* carregamento de configuração;
* validação YAML;
* extractors;
* checksum;
* metadata;
* storage;
* orquestração da ingestão.

### Silver

* testes dbt;
* `not_null`;
* `unique`;
* `relationships`;
* `accepted_values`;
* testes customizados de Data Quality;
* regras de negócio da camada Silver.

### Gold

* feature engineering;
* scoring;
* regras determinísticas;
* métricas;
* algoritmos;
* Machine Learning quando implementado.

### App

* apresentação;
* contratos de entrada;
* integração com serviços;
* comportamento da interface quando aplicável.

---

# 30. Documentação de testes por etapa

Cada etapa deve possuir:

```text
docs/testes.md
```

Esse arquivo deve explicar de forma detalhada a estratégia de testes daquela etapa.

Quando relevante, documentar:

* objetivo dos testes;
* componentes cobertos;
* tipos de testes;
* cenários validados;
* casos de falha;
* mocks ou fixtures;
* critérios de aprovação;
* limitações;
* dependências externas;
* resultados relevantes;
* data da última validação.

Não utilizar `docs/testes.md` como substituto da implementação dos testes.

Ele documenta a estratégia e os resultados; os testes reais permanecem em `tests/`.

---

# 31. Papel da pasta `/testes` da raiz

A pasta:

```text
/testes
```

não deve ser utilizada como depósito central de todos os testes do projeto.

Ela é reservada principalmente para testes que atravessam mais de uma etapa.

Estrutura conceitual:

```text
testes/
├── README.md
├── matriz-testes.md
├── contratos/
├── integracao/
└── end-to-end/
```

A estrutura pode evoluir conforme a necessidade real do projeto.

---

# 32. Testes de contratos

A pasta:

```text
testes/contratos/
```

deve conter validações relacionadas aos contratos entre etapas.

Exemplos:

```text
Bronze
→ entrega schema compatível com Silver?

Silver
→ entrega campos e granularidade esperados pela Gold?

Gold
→ entrega contrato esperado pelo App?
```

Mudanças incompatíveis devem ser detectáveis sempre que possível.

---

# 33. Testes de integração

A pasta:

```text
testes/integracao/
```

deve ser utilizada quando a validação depender da interação entre múltiplas partes do sistema.

Exemplos:

* Bronze + S3;
* Bronze → Silver;
* Silver → Gold;
* Gold → App;
* componentes internos que precisam funcionar conjuntamente.

Testes puramente locais devem continuar dentro da etapa responsável.

---

# 34. Testes end-to-end

A pasta:

```text
testes/end-to-end/
```

deve ser utilizada futuramente para validações do fluxo completo.

Exemplo conceitual:

```text
fonte externa
↓
Bronze
↓
Silver
↓
Gold
↓
resultado final
↓
App
```

Não criar testes end-to-end apenas por formalidade enquanto o pipeline ainda não justificar esse nível de validação.

---

# 35. `testes/README.md`

O arquivo:

```text
testes/README.md
```

deve explicar a estratégia global de qualidade do projeto.

Deve permitir compreender:

* quais tipos de testes existem;
* onde cada tipo de teste deve morar;
* quando cada conjunto deve ser executado;
* quais etapas possuem cobertura;
* como interpretar falhas;
* como executar as validações globais quando aplicável.

Evitar duplicar nesse documento detalhes já existentes em `etapa/docs/testes.md`.

---

# 36. `testes/matriz-testes.md`

O arquivo:

```text
testes/matriz-testes.md
```

deve fornecer uma visão consolidada dos testes do projeto.

Exemplo:

```markdown
# Matriz de Testes

| Etapa | Tipo | Status | Última execução |
| --- | --- | --- | --- |
| Bronze | Unitário | ✅ | 12/09/2026 |
| Bronze | Integração S3 | ✅ | 12/09/2026 |
| Silver | dbt tests | 🚧 | - |
| Gold | Unitário | 📋 | - |
| App | Integração | 📋 | - |
| Bronze → Silver | Contrato | 📋 | - |
| Pipeline completo | End-to-End | 📋 | - |
```

A matriz é um resumo.

Ela não substitui:

* os testes reais;
* `docs/testes.md`;
* `STATUS.md`.

---

# 37. Atualização da documentação de testes

Sempre que uma alteração relevante:

* criar novos testes;
* remover testes;
* alterar comportamento testado;
* modificar critérios de aprovação;
* alterar contratos entre etapas;
* mudar cobertura relevante;

verificar se é necessário atualizar:

```text
etapa/docs/testes.md
+
testes/matriz-testes.md
+
STATUS.md
+
CHANGELOG.md
```

Também registrar a decisão em `docs/decisoes.md` quando existir mudança relevante na estratégia de validação.

---

# 38. Testes antes da conclusão

Uma mudança de código só deve ser considerada concluída após a execução das validações relevantes disponíveis.

Quando existirem:

* testes unitários;
* testes de integração;
* testes de contratos;
* testes end-to-end;
* lint;
* formatter;
* compile;
* dbt test;
* dbt compile;

executá-los conforme o contexto.

Se algum teste não puder ser realizado, informar explicitamente:

* qual teste não foi executado;
* motivo;
* impacto;
* necessidade de validação futura.

Nunca apresentar uma validação como concluída quando ela não tiver sido executada.

---

# 39. Falhas de teste

Uma falha de teste não deve ser ocultada apenas para concluir uma tarefa.

O agente deve:

1. identificar a causa;
2. determinar se a falha foi causada pela alteração atual;
3. corrigir quando estiver dentro do escopo;
4. documentar limitações quando não puder corrigir;
5. não modificar testes válidos apenas para fazer o pipeline passar.

Testes não devem ser enfraquecidos sem justificativa técnica registrada.

---

# 40. Erros

Não esconder falhas silenciosamente.

Evitar:

```python
except Exception:
    pass
```

Erros relevantes devem:

* ser registrados;
* possuir contexto;
* ser tratados de acordo com sua criticidade.

---

# 41. Segurança

Nunca versionar:

* `.env`;
* credenciais AWS;
* tokens;
* senhas;
* API keys;
* secrets;
* chaves privadas.

Utilizar:

* `.env.example`;
* variáveis de ambiente;
* GitHub Secrets;
* mecanismos de autenticação adequados.

---

# 42. Dados

Não versionar datasets grandes ou dados sensíveis.

Evitar incluir no Git:

* dumps;
* arquivos Bronze completos;
* artefatos binários grandes;
* resultados intermediários volumosos;
* modelos pesados.

Dados utilizados no projeto devem possuir origem e condições de uso documentadas quando relevante.

---

# 43. Contratos entre etapas

As etapas possuem dependências entre si.

Mudanças em:

```text
Bronze
↓
Silver
↓
Gold
↓
App
```

podem quebrar consumidores posteriores.

Alterações em:

* nomes de campos;
* granularidade;
* tipos;
* chaves;
* schemas;
* formatos de saída;

devem ser tratadas como mudanças potencialmente incompatíveis.

Essas alterações devem ser documentadas em:

* documentação da etapa;
* `decisoes.md`;
* `CHANGELOG.md`;
* README quando relevante;
* testes de contrato quando aplicável.

---

# 44. Fonte da verdade

Nenhum arquivo deve ser considerado isoladamente como verdade absoluta.

A interpretação correta deve considerar:

```text
prompt atual
+
AGENTS
+
STATUS
+
documentação
+
código
+
decisões
+
histórico
```

Entretanto, para comportamento executável, o código existente representa a verdade operacional.

Se houver inconsistência, o agente deve identificar e corrigir a documentação ou implementação correspondente.

---

# 45. Critério global de conclusão

Uma tarefa relevante somente pode ser considerada concluída quando:

* a implementação estiver realizada;
* os testes relevantes tiverem sido executados;
* o comportamento esperado tiver sido validado;
* a documentação específica estiver atualizada;
* `docs/testes.md` estiver atualizado quando necessário;
* `testes/matriz-testes.md` estiver atualizado quando necessário;
* o `STATUS.md` estiver atualizado quando necessário;
* `docs/decisoes.md` possuir o registro correspondente;
* o README raiz tiver sido verificado;
* o `CHANGELOG.md` possuir a entrada apropriada;
* limitações conhecidas estiverem documentadas;
* nenhuma pendência estiver sendo apresentada como concluída.

---

# 46. Filosofia documental

Cada tipo de arquivo possui uma responsabilidade distinta.

```text
README.md
→ apresenta o projeto

AGENTS.md
→ define como trabalhar

STATUS.md
→ mostra onde estamos

docs/
→ explica profundamente

docs/decisoes.md
→ registra o raciocínio das escolhas

docs/testes.md
→ explica a estratégia de validação da etapa

testes/matriz-testes.md
→ mostra a visão consolidada da qualidade

CHANGELOG.md
→ registra a evolução histórica

código
→ implementa o sistema

tests/
→ valida o comportamento
```

Essa separação deve ser preservada.

---

# 47. Filosofia de desenvolvimento

A tecnologia deve seguir a necessidade.

A ordem de raciocínio esperada é:

```text
problema
↓
requisito
↓
decisão
↓
arquitetura
↓
implementação
↓
validação
```

Evitar:

```text
tecnologia
↓
procurar um problema para utilizá-la
```

---

# 48. Regra final para agentes

Antes de iniciar:

```text
Prompt
↓
AGENTS raiz
↓
AGENTS local
↓
STATUS
↓
docs necessários
↓
código
↓
decisões anteriores
```

Durante a execução:

```text
preservar
↓
implementar
↓
testar
↓
validar
```

Antes de concluir:

```text
documentação
↓
documentação de testes
↓
STATUS
↓
DECISÕES
↓
matriz de testes
↓
README
↓
CHANGELOG
```

O objetivo não é apenas produzir código funcional.

O objetivo é manter um projeto:

* compreensível;
* rastreável;
* documentado;
* testado;
* consistente;
* evolutivo;
* tecnicamente justificável.

O agente deve deixar o projeto em um estado mais claro e mais confiável do que encontrou.
