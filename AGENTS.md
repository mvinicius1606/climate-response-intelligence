# AGENTS.md

## 1. Finalidade

Este arquivo define as regras globais de desenvolvimento, documentação, validação e trabalho assistido por agentes no projeto **Climate Response Intelligence**.

As regras deste arquivo se aplicam a todo o repositório.

O projeto deve ser desenvolvido em **pequenas unidades de trabalho**, iniciadas por um **Prompt Inicial**.

O `AGENTS.md` não define qual será a próxima tarefa.

Ele define:

> **como uma tarefa autorizada deve ser executada.**

As etapas do projeto podem possuir `AGENTS.md` próprios para complementar estas regras com instruções técnicas específicas.

A hierarquia de contexto é:

```text
Prompt Inicial
↓
AGENTS.md raiz
↓
AGENTS.md da etapa
↓
STATUS.md
↓
documentação necessária
↓
código existente
↓
decisões e histórico
```

---

# 2. Filosofia de trabalho

O desenvolvimento deve seguir:

```text
entender
↓
executar uma ação limitada
↓
validar
↓
compreender
↓
documentar
↓
atualizar o estado
↓
definir a próxima ação
```

O agente não deve transformar uma tarefa limitada em uma expansão geral do projeto.

A próxima ação pertence ao autor, salvo quando o próprio Prompt Inicial conceder autonomia explícita.

---

# 3. Prompt Inicial

O **Prompt Inicial** é o gatilhador de cada unidade de trabalho.

Ele deve definir, quando aplicável:

```text
AÇÃO

OBJETIVO

CONTEXTO

DOCUMENTAÇÃO EXISTENTE

FONTES OU SITES A CONSULTAR

ESCOPO

AUTONOMIA AUTORIZADA

O QUE NÃO FAZER

ENTREGÁVEIS

VALIDAÇÕES

DOCUMENTAÇÃO DA AÇÃO

CRITÉRIO DE CONCLUSÃO
```

Nem todos os campos precisam existir em tarefas simples.

A profundidade do prompt deve acompanhar a complexidade da ação.

O Prompt Inicial é a autoridade da tarefa atual quanto a:

* objetivo;
* escopo;
* restrições;
* autonomia;
* entregáveis;
* validações;
* critério de conclusão.

Ele não substitui regras permanentes de segurança, integridade e qualidade definidas nos `AGENTS.md`.

---

# 4. Escopo

O agente deve permanecer dentro do escopo autorizado.

Não utilizar uma tarefa pequena como oportunidade para:

* alterar arquitetura global;
* reorganizar componentes não relacionados;
* adicionar ferramentas;
* trocar bibliotecas;
* substituir tecnologias;
* expandir funcionalidades;
* implementar etapas futuras;
* refatorar código sem necessidade;
* modificar decisões já validadas.

Melhorias fora do escopo devem ser apresentadas como recomendação, não implementadas automaticamente.

---

# 5. Autonomia

A autonomia do agente deve ser determinada pelo Prompt Inicial.

Exemplos de níveis possíveis:

### Autonomia restrita

O agente executa decisões já definidas.

Mudanças arquiteturais ou estruturais devem apenas ser relatadas.

### Autonomia técnica limitada

O agente pode decidir detalhes internos da implementação, desde que preserve:

* arquitetura;
* contratos;
* escopo;
* comportamento esperado.

### Autonomia investigativa

O agente pode:

* pesquisar;
* comparar alternativas;
* recomendar soluções;
* justificar tecnicamente.

A decisão ainda precisa ser validada conforme o Prompt Inicial.

### Autonomia ampliada

Somente existe quando declarada explicitamente.

O agente nunca deve presumir autonomia ampliada.

---

# 6. Mudanças que exigem autorização explícita

Sem autorização clara, o agente não deve:

* substituir arquitetura existente;
* trocar tecnologias principais;
* alterar contratos entre etapas;
* adicionar fontes ao escopo;
* remover componentes concluídos;
* realizar mudanças destrutivas;
* alterar regras de negócio;
* alterar targets ou critérios de Machine Learning;
* substituir modelos;
* apagar histórico;
* expandir o projeto para além da ação atual.

Caso essa necessidade apareça, deve ser relatada.

---

# 7. Modo de aprendizagem

Este projeto utiliza agentes para reduzir trabalho operacional e repetitivo, não para substituir a compreensão do autor.

As tarefas devem ser divididas em unidades suficientemente pequenas para que o autor consiga:

* revisar;
* compreender;
* questionar;
* testar;
* explicar;

antes de avançar.

O agente não deve antecipar etapas futuras apenas porque parecem relacionadas.

Ao concluir uma implementação relevante, deve ser capaz de explicar:

* quais arquivos foram alterados;
* responsabilidade de cada componente;
* fluxo implementado;
* entradas e saídas;
* decisões técnicas;
* validações realizadas;
* limitações existentes.

---

# 8. Não avançar implicitamente

Concluir uma ação não autoriza automaticamente a próxima.

Exemplo:

```text
Implementar ingestão IBGE
```

não autoriza:

```text
implementar ANA
+
criar Silver
+
implementar Gold
```

A próxima unidade de trabalho exige novo Prompt Inicial, salvo autorização explícita.

---

# 9. Idioma

O projeto deve ser desenvolvido prioritariamente em **português brasileiro**.

Termos técnicos, ferramentas e conceitos normalmente utilizados em inglês devem permanecer em inglês.

Exemplos:

* Python;
* SQL;
* dbt;
* Docker;
* Machine Learning;
* Data Quality;
* Data Lineage;
* Bronze;
* Silver;
* Gold;
* staging;
* tests;
* features;
* API;
* endpoint;
* logging;
* storage;
* manifest;
* checksum;
* retry.

Priorizar naturalidade e uso profissional.

---

# 10. Estilo de documentação

A documentação deve possuir estilo próximo a:

* trabalhos acadêmicos;
* relatórios técnicos;
* documentação profissional.

A escrita deve ser:

* formal;
* natural;
* clara;
* objetiva;
* explicativa;
* tecnicamente justificável.

Quando relevante, explicar:

1. contexto;
2. problema;
3. objetivo;
4. solução;
5. funcionamento;
6. motivo da escolha;
7. validação;
8. limitações;
9. possíveis evoluções.

Evitar:

* linguagem artificial;
* repetições;
* excesso de jargões;
* listas desconectadas;
* documentação criada apenas por formalidade.

---

# 11. Estrutura da documentação

Documentos devem utilizar hierarquia clara de títulos e subtítulos.

Documentos extensos devem possuir **sumário**.

Documentos pequenos não precisam de sumário apenas por formalidade.

Não criar arquivos vazios para completar uma estrutura idealizada.

Detalhes específicos de uma etapa devem permanecer na documentação daquela etapa.

---

# 12. Estrutura global

O projeto possui quatro etapas principais:

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
└── demais arquivos globais
```

Responsabilidades gerais:

```text
ingestao-bronze/
→ aquisição e preservação dos dados

etl-silver/
→ transformação, conformação e Data Quality

inteligencia-gold/
→ indicadores, algoritmos, ML e Decision Intelligence

app/
→ apresentação e interação
```

Regras técnicas específicas pertencem aos `AGENTS.md` dessas etapas.

---

# 13. AGENTS locais

Os `AGENTS.md` locais complementam este arquivo.

Eles devem conter somente regras específicas daquela etapa.

Não repetir integralmente as regras globais.

Exemplo:

```text
/AGENTS.md
→ método global de trabalho

ingestao-bronze/AGENTS.md
→ regras da Bronze

etl-silver/AGENTS.md
→ regras da Silver

inteligencia-gold/AGENTS.md
→ regras da Gold

app/AGENTS.md
→ regras do App
```

---

# 14. STATUS.md

Cada etapa deve possuir, quando aplicável:

```text
STATUS.md
```

Ele representa:

> **onde estamos agora.**

Não é histórico.

Estados recomendados:

```text
CONCLUÍDO
EM DESENVOLVIMENTO
PENDENTE
PLANEJADO
```

O `STATUS.md` deve informar apenas o estado real.

Arquivo existente ou placeholder não significa funcionalidade implementada.

---

# 15. Componentes concluídos

`CONCLUÍDO` significa:

> implementado e validado conforme os critérios existentes naquele momento.

Não significa:

> nunca modificar.

Componentes concluídos não devem ser reconstruídos sem necessidade explícita.

Quando uma alteração for autorizada:

1. inspecionar implementação existente;
2. preservar partes funcionais;
3. verificar contratos;
4. realizar mudança incremental;
5. validar novamente.

---

# 16. Atualização do STATUS

Atualizar `STATUS.md` quando uma ação validada mudar efetivamente o estado de um componente.

Exemplo:

```text
Extractor IBGE — EM DESENVOLVIMENTO
```

após validação:

```text
Extractor IBGE — CONCLUÍDO
```

Pesquisa exploratória sem mudança real não exige alteração automática de status.

---

# 17. docs/decisoes.md

Cada etapa deve possuir, quando necessário:

```text
docs/decisoes.md
```

O documento registra decisões técnicas, arquiteturais ou de modelagem realmente adotadas.

Ele deve responder:

> O que foi decidido, por que, quais áreas foram afetadas e como foi validado?

Não utilizar `decisoes.md` como diário de toda alteração pequena.

---

# 18. Registro após validação

A ordem preferencial é:

```text
ação
↓
implementação ou análise
↓
validação
↓
decisão confirmada
↓
registro em decisoes.md
```

Hipóteses e experimentos ainda não validados não devem ser apresentados como decisões definitivas.

Alternativas rejeitadas podem ser mencionadas quando relevantes.

---

# 19. Estrutura das decisões

Cada decisão deve registrar, quando aplicável:

```markdown
## Título

**Data:** DD/MM/AAAA
**Status:** Validada
**Origem:** ...
**Prompt relacionado:** ...

### Contexto

### O que foi feito

### Por que foi feito

### Decisão adotada

### Áreas afetadas

### Validação

### Alternativas consideradas

### Limitações

### Responsabilidade da decisão
```

Campos irrelevantes podem ser omitidos.

---

# 20. Origem da decisão

Utilizar uma das categorias:

```text
AUTOR
```

Decisão definida pelo autor.

```text
AUTOR + AGENTE
```

Decisão construída conjuntamente.

```text
AGENTE, APROVADO PELO AUTOR
```

O agente investigou ou propôs a solução dentro da autonomia concedida, posteriormente validada pelo autor.

O objetivo é transparência sobre o processo de desenvolvimento.

---

# 21. Documentação específica da ação

O Prompt Inicial pode determinar criação ou atualização de documentos específicos.

Exemplos:

* `fontes-de-dados.md`;
* `arquitetura.md`;
* `ingestao.md`;
* `metadata-lineage.md`;
* `testes.md`;
* `modelo-de-dados.md`;
* `features.md`.

Se a ação deixar documentação existente incorreta, atualizar somente os documentos realmente afetados.

---

# 22. README.md

O README é a porta de entrada do projeto.

Deve apresentar de forma resumida:

* problema;
* objetivo;
* arquitetura;
* etapas;
* estado de alto nível;
* tecnologias;
* resultados relevantes;
* links para documentação.

Não deve conter toda a documentação técnica.

---

# 23. Atualização do README

Não atualizar o README a cada microação.

Atualizar quando houver mudança relevante, como:

* conclusão de parte significativa;
* novo fluxo ponta a ponta;
* nova fonte principal concluída;
* mudança arquitetural;
* mudança de escopo;
* novo resultado;
* milestone.

Ajustes internos pequenos normalmente não exigem atualização.

---

# 24. CHANGELOG.md

O `CHANGELOG.md` registra evolução relevante do projeto.

Não registrar cada pequena edição.

Registrar principalmente:

* conclusão de componentes importantes;
* milestones;
* mudanças arquiteturais;
* novas funcionalidades relevantes;
* mudanças importantes de contrato;
* alterações significativas de escopo.

---

# 25. Estado real versus planejamento

Diferenciar claramente:

```text
IMPLEMENTADO
EM DESENVOLVIMENTO
PLANEJADO
FUTURO
```

Nunca apresentar planejamento, documentação ou placeholder como funcionalidade implementada.

---

# 26. Fonte da verdade

A compreensão correta do estado considera:

```text
Prompt Inicial
+
AGENTS
+
STATUS
+
documentação
+
código
+
testes
+
decisões
+
histórico
```

Para comportamento executável, o código representa a verdade operacional.

Se houver divergência, investigar e reconciliar.

---

# 27. Preservação do trabalho existente

Antes de alterar código:

1. inspecionar arquivos relacionados;
2. consultar STATUS;
3. consultar documentação necessária;
4. verificar decisões relevantes;
5. identificar componentes funcionais;
6. preservar soluções válidas.

Não refatorar apenas por preferência estética.

---

# 28. Simplicidade

Priorizar:

1. correção;
2. clareza;
3. manutenção;
4. testabilidade;
5. simplicidade;
6. rastreabilidade;
7. performance quando necessária;
8. sofisticação.

Evitar overengineering.

A tecnologia deve seguir a necessidade.

---

# 29. Separação de responsabilidades

Código deve possuir responsabilidades claras.

Evitar:

* arquivos excessivamente grandes;
* classes com múltiplas funções independentes;
* duplicação;
* acoplamento excessivo;
* acesso externo misturado com regra de negócio;
* configuração espalhada.

Modularização não significa fragmentar código sem motivo.

---

# 30. Testabilidade

Sempre que possível separar:

```text
acesso externo
configuração
transformação
regra de negócio
storage
orquestração
```

Evitar componentes que dependam simultaneamente de:

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

# 31. Testes

Testes específicos devem permanecer próximos da etapa responsável:

```text
ingestao-bronze/tests/
etl-silver/tests/
inteligencia-gold/tests/
app/tests/
```

Testes transversais podem permanecer em:

```text
/testes
```

para casos como:

* contratos;
* integração entre etapas;
* end-to-end.

Detalhes de testes específicos pertencem aos `AGENTS.md` locais ou documentação da etapa.

---

# 32. Validação

Uma implementação só pode ser considerada concluída após as validações relevantes.

Podem incluir:

* testes unitários;
* testes de integração;
* testes de contrato;
* smoke tests;
* lint;
* compile;
* `dbt compile`;
* `dbt test`;
* comparação com fonte oficial;
* validação manual.

O Prompt Inicial deve especificar validações quando necessário.

---

# 33. Validação não executada

Se uma validação necessária não puder ser realizada, informar:

* qual;
* motivo;
* impacto;
* risco;
* validação futura necessária.

Nunca declarar algo como validado sem ter executado a validação correspondente.

---

# 34. Erros e falhas

Não esconder erros silenciosamente.

Evitar:

```python
except Exception:
    pass
```

Falhas devem possuir contexto e tratamento proporcional à criticidade.

Testes válidos não devem ser enfraquecidos apenas para obter sucesso.

---

# 35. Dependências

Não adicionar bibliotecas, frameworks, serviços ou ferramentas sem necessidade concreta.

Antes de adicionar:

1. verificar recursos existentes;
2. verificar recursos nativos;
3. avaliar manutenção;
4. avaliar impacto;
5. justificar quando relevante.

---

# 36. Segurança

Nunca versionar:

* `.env`;
* credenciais AWS;
* AWS Session Token;
* tokens;
* senhas;
* API keys;
* secrets;
* chaves privadas.

Utilizar mecanismos apropriados, como:

* `.env.example`;
* variáveis de ambiente;
* AWS profiles;
* IAM;
* GitHub Secrets.

---

# 37. Dados

Não versionar datasets grandes, sensíveis ou desnecessários.

Evitar no Git:

* Bronze completo;
* dumps;
* caches;
* arquivos temporários;
* artefatos volumosos;
* grandes Parquets;
* modelos pesados.

As fontes utilizadas devem possuir origem documentada quando relevante.

---

# 38. Contratos entre etapas

Alterações em:

* nomes;
* tipos;
* chaves;
* granularidade;
* schema;
* formato;
* semântica;

podem quebrar consumidores posteriores.

Não modificar contratos sem autorização adequada e validação de impacto.

---

# 39. Pesquisa não implica implementação

Uma ação de pesquisa não autoriza automaticamente implementação.

Exemplo:

```text
Pesquisar APIs oficiais da ANA
```

não significa:

```text
escolher
+
implementar
+
alterar arquitetura
```

salvo se autorizado no Prompt Inicial.

---

# 40. Critério de conclusão

Uma ação é concluída quando:

* o objetivo do Prompt Inicial foi atendido;
* os entregáveis existem;
* as validações previstas foram executadas;
* falhas relevantes foram resolvidas ou documentadas;
* a documentação afetada está consistente;
* o estado real está corretamente representado.

Não existe obrigação de atualizar todos os documentos em toda tarefa.

---

# 41. Documentação proporcional

A documentação deve acompanhar o impacto real.

Exemplos:

```text
correção de typo
→ sem decisão arquitetural
```

```text
mudança da estratégia de storage
→ decisão documentada
```

```text
conclusão da ingestão IBGE
→ STATUS
→ decisão
→ possível CHANGELOG
→ possível README
```

---

# 42. Fluxo antes da execução

Antes de agir:

```text
1. Ler Prompt Inicial.

2. Identificar:
   ação
   objetivo
   escopo
   autonomia
   restrições
   entregáveis
   validação
   documentação

3. Ler AGENTS raiz.

4. Ler AGENTS local, quando existir.

5. Consultar STATUS.

6. Consultar somente a documentação necessária.

7. Inspecionar código relacionado.

8. Consultar decisões anteriores quando relevante.
```

---

# 43. Fluxo durante a execução

```text
preservar escopo
↓
pesquisar ou implementar
↓
testar
↓
validar
↓
identificar limitações
```

Não iniciar automaticamente a próxima ação.

---

# 44. Fluxo após validação

Quando aplicável:

```text
resultado validado
↓
documentação específica
↓
decisão
↓
STATUS
↓
CHANGELOG
↓
README
```

Cada atualização é condicional ao impacto real.

---

# 45. Relatório final

Ao concluir uma tarefa relevante, informar:

* o que foi feito;
* arquivos criados;
* arquivos alterados;
* validações realizadas;
* testes executados;
* decisões registradas;
* limitações;
* pendências;
* recomendações não implementadas.

Quando houver código, explicar o fluxo de forma compatível com o modo de aprendizagem.

---

# 46. Papel do autor

O autor permanece responsável por:

* definir objetivos;
* controlar escopo;
* aprovar mudanças relevantes;
* compreender a arquitetura;
* revisar decisões;
* validar aprendizados;
* definir a próxima ação.

---

# 47. Papel do agente

O agente pode atuar como:

* executor;
* pesquisador;
* revisor;
* parceiro técnico;
* explicador;
* auxiliar de documentação;
* suporte de validação.

Não deve atuar como gerente autônomo do projeto sem autorização explícita.

---

# 48. Regra final

O Prompt Inicial define:

> **o que fazer agora.**

O `AGENTS.md` raiz define:

> **como trabalhar no projeto.**

O `AGENTS.md` local define:

> **como trabalhar naquela etapa.**

O `STATUS.md` mostra:

> **onde estamos.**

A documentação explica:

> **como e por que construímos.**

O código mostra:

> **o que realmente foi implementado.**

Os testes demonstram:

> **o que foi validado.**

As decisões registram:

> **o que foi adotado, por quê e com qual participação do autor e do agente.**

O agente deve executar somente a unidade de trabalho autorizada, preservar o aprendizado do autor, validar antes de declarar conclusão e deixar o projeto mais claro e confiável do que encontrou.
