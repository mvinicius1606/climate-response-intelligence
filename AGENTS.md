# AGENTS.md

## 1. Finalidade deste arquivo

Este arquivo define as regras globais de desenvolvimento, organização e documentação do projeto **Climate Response Intelligence**.

Estas instruções devem ser consideradas em qualquer tarefa realizada neste repositório.

Cada etapa principal do projeto possui seu próprio `AGENTS.md`, responsável por complementar estas regras com orientações específicas daquela área.

As instruções locais podem detalhar comportamentos, estruturas e tecnologias próprias da etapa, mas devem preservar os princípios globais definidos neste arquivo.

---

## 2. Idioma do projeto

O projeto deve ser desenvolvido prioritariamente em **português brasileiro**.

Devem permanecer em inglês apenas termos técnicos, nomes de ferramentas, comandos, conceitos consolidados ou nomenclaturas cujo uso em português seja incomum ou prejudique a compreensão.

Exemplos que podem permanecer em inglês:

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

A prioridade é utilizar a forma mais natural e reconhecida no contexto profissional brasileiro.

---

## 3. Estilo de documentação

Toda documentação deve seguir uma estrutura próxima de um **trabalho acadêmico ou relatório técnico**, porém sem utilizar linguagem excessivamente rebuscada.

A escrita deve apresentar:

* linguagem formal;
* linguagem natural;
* clareza;
* objetividade;
* continuidade entre as ideias;
* utilização adequada de conectivos;
* explicações contextualizadas;
* leitura agradável e envolvente;
* profundidade proporcional à importância do assunto.

Evitar:

* frases excessivamente fragmentadas;
* linguagem artificial;
* repetição desnecessária;
* excesso de termos técnicos sem explicação;
* documentação formada apenas por listas;
* textos excessivamente burocráticos.

O texto deve explicar não apenas **o que foi feito**, mas, quando relevante:

* por que foi feito;
* qual problema resolve;
* como funciona;
* quais decisões foram tomadas;
* quais limitações existem.

---

## 4. Organização da documentação

Os conteúdos devem ser organizados utilizando títulos e subtítulos hierárquicos.

Exemplo:

```text
1. Assunto principal
   1.1. Contexto
   1.2. Implementação
   1.3. Decisões
   1.4. Limitações
```

Documentações extensas devem possuir **sumário** no início do arquivo.

O sumário deve fornecer acesso rápido às principais seções do documento.

Documentações pequenas não precisam receber um sumário artificial apenas para cumprir esta regra.

A estrutura deve acompanhar o tamanho e a complexidade real do conteúdo.

---

## 5. Estrutura geral do projeto

O projeto é dividido em **quatro etapas principais**.

Cada etapa possui uma pasta mãe própria, responsável por concentrar:

* código;
* configurações;
* documentação;
* dependências;
* arquivos auxiliares;
* decisões específicas;
* `AGENTS.md` da etapa.

A estrutura conceitual principal é:

```text
climate-response-intelligence/
│
├── ingestao-bronze/
├── etl-silver/
├── inteligencia-gold/
├── app/
│
├── README.md
├── CHANGELOG.md
├── AGENTS.md
└── demais arquivos globais
```

As quatro etapas representam responsabilidades diferentes do sistema.

### 5.1. `ingestao-bronze/`

Responsável pela obtenção dos dados externos, metadata, rastreabilidade e armazenamento na camada Bronze.

### 5.2. `etl-silver/`

Responsável pela transformação, padronização, integração e Data Quality necessárias para produzir dados confiáveis.

### 5.3. `inteligencia-gold/`

Responsável pela camada analítica e de inteligência, incluindo indicadores, features, scoring, algoritmos, Machine Learning e mecanismos de apoio à decisão quando aplicáveis.

### 5.4. `app/`

Responsável pela camada de apresentação e interação com o usuário.

A interface não deve concentrar regras de negócio que pertençam às etapas anteriores.

---

## 6. Independência entre etapas

Cada pasta mãe deve ser tratada como uma área de responsabilidade própria.

Ao trabalhar em uma etapa:

1. ler primeiro o `AGENTS.md` da raiz;
2. ler o `AGENTS.md` específico daquela etapa;
3. inspecionar a implementação existente;
4. preservar estruturas já validadas;
5. limitar alterações à etapa solicitada sempre que possível.

Não modificar outras etapas apenas por preferência estética ou conveniência.

Alterações entre etapas devem ocorrer somente quando existir uma dependência real.

---

## 7. `AGENTS.md` específicos

Cada uma das quatro etapas deve possuir seu próprio:

```text
AGENTS.md
```

O `AGENTS.md` local deve conter somente regras específicas daquela etapa, como:

* arquitetura interna;
* tecnologias;
* convenções;
* responsabilidades;
* testes;
* padrões de código;
* estrutura de documentação;
* decisões já consolidadas.

Evitar repetir integralmente regras já existentes no `AGENTS.md` raiz.

O arquivo raiz define o comportamento global.

O arquivo local especializa esse comportamento.

---

## 8. README principal

O `README.md` localizado na raiz do repositório é a **porta de entrada do projeto**.

Ele deve permitir que uma pessoa compreenda rapidamente:

1. qual problema o projeto resolve;
2. qual é a proposta da solução;
3. como o sistema está organizado;
4. quais são as principais etapas;
5. qual é o estado atual do desenvolvimento;
6. quais resultados já foram alcançados;
7. onde encontrar informações mais detalhadas.

O README raiz não deve concentrar toda a documentação técnica.

Ele deve funcionar como um **resumo executivo e índice de navegação**.

Informações detalhadas devem permanecer nas documentações específicas de cada etapa.

O README deve possuir links diretos para essas documentações.

Exemplo conceitual:

```text
README
│
├── Ingestão Bronze → documentação detalhada
├── ETL Silver → documentação detalhada
├── Inteligência Gold → documentação detalhada
└── Aplicação → documentação detalhada
```

---

## 9. Sincronização obrigatória do README

Sempre que uma documentação relevante for criada, removida, renomeada ou alterada em qualquer uma das quatro etapas, verificar se o `README.md` raiz também precisa ser atualizado.

O README deve permanecer sincronizado com o estado real do projeto.

Isso inclui, quando aplicável:

* novos links;
* alterações arquiteturais;
* mudanças de escopo;
* funcionalidades concluídas;
* mudanças de status;
* novos resultados;
* alteração de nomenclaturas;
* novas etapas ou componentes importantes.

Não deixar o README descrevendo uma arquitetura antiga.

O código, a documentação detalhada e o README devem representar o mesmo estado do projeto.

---

## 10. CHANGELOG global

O arquivo:

```text
CHANGELOG.md
```

localizado na raiz deve registrar a evolução do **projeto**, e não apenas alterações administrativas do repositório.

Toda ação relevante que modifique o projeto deve gerar uma nova entrada.

Cada entrada deve possuir obrigatoriamente:

* título;
* data;
* hora;
* descrição objetiva do que foi alterado.

Formato recomendado:

```markdown
## Implementação da ingestão do IBGE

**Data:** 12/09/2026  
**Hora:** 16:35

Foi adicionada a primeira fonte oficial do IBGE à camada de ingestão Bronze. A alteração incluiu configuração YAML, mecanismo de extração, geração de metadata e armazenamento no Amazon S3.

Também foram adicionados os respectivos testes e atualizada a documentação da etapa.
```

---

## 11. O que deve ser registrado no CHANGELOG

Registrar alterações como:

* implementação de uma nova fonte;
* conclusão de uma etapa;
* criação de um componente;
* refatoração relevante;
* mudança arquitetural;
* alteração de regra de negócio;
* inclusão de Data Quality;
* criação ou mudança de modelos dbt;
* implementação de scoring;
* inclusão ou alteração de Machine Learning;
* mudanças relevantes na interface;
* correções que alterem comportamento;
* mudanças importantes de documentação;
* alteração de dependências relevantes;
* mudança de estratégia ou escopo.

Não é necessário criar entrada para ações puramente administrativas sem impacto no projeto, como:

* correção de pequeno erro ortográfico;
* reorganização visual sem mudança de significado;
* alteração irrelevante de formatação;
* operações internas do Git.

O `CHANGELOG.md` deve representar a evolução técnica e funcional do projeto.

---

## 12. Atualizações relacionadas

Ao concluir uma alteração relevante, verificar sempre se é necessário atualizar:

```text
código
↓
documentação específica
↓
README raiz
↓
CHANGELOG
```

Esses elementos devem permanecer sincronizados.

Uma funcionalidade não deve ser considerada completamente documentada quando apenas o código foi alterado.

Da mesma forma, a documentação não deve afirmar que existe uma funcionalidade que ainda não está implementada.

---

## 13. Estado real versus planejamento

Diferenciar claramente:

* implementado;
* em desenvolvimento;
* planejado;
* futuro.

Nunca apresentar uma funcionalidade planejada como se estivesse implementada.

Quando necessário, utilizar indicações claras de status, como:

```text
✅ Implementado
🚧 Em desenvolvimento
📋 Planejado
🔮 Fase futura
```

A documentação deve refletir o estado real do projeto no momento da alteração.

---

## 14. Preservação do trabalho existente

Antes de modificar uma área:

1. inspecionar os arquivos existentes;
2. identificar o que já foi implementado;
3. identificar decisões documentadas;
4. consultar o `CHANGELOG.md`;
5. consultar o `AGENTS.md` específico da etapa;
6. preservar soluções funcionais e já validadas.

Não reconstruir uma etapa do zero quando ela já estiver implementada.

Prefira alterações incrementais.

Refatorações maiores devem possuir uma justificativa concreta.

---

## 15. Datas de conclusão e validação

Quando uma etapa ou componente importante for concluído, registrar sua data de conclusão ou última validação na documentação apropriada.

Exemplo:

```text
Status: CONCLUÍDO
Data de conclusão: 12/09/2026
Última validação: 12/09/2026
```

Essas informações devem ajudar agentes e desenvolvedores futuros a identificar componentes consolidados que não precisam ser reconstruídos.

---

## 16. Filosofia geral

O projeto deve permanecer compreensível tanto para pessoas que desejam apenas conhecer a solução quanto para profissionais que desejam investigar sua implementação.

Por isso, a documentação possui diferentes níveis de profundidade:

```text
README raiz
→ visão geral e navegação

documentação de cada etapa
→ detalhes técnicos

código
→ implementação

AGENTS.md
→ regras de desenvolvimento e manutenção

CHANGELOG.md
→ evolução histórica
```

A organização deve favorecer progressivamente a descoberta de informações, sem obrigar o leitor a compreender todo o sistema para encontrar um assunto específico.

---

## 17. Regra final para agentes

Antes de encerrar qualquer tarefa relevante no projeto:

1. validar as alterações realizadas;
2. verificar se a documentação específica precisa ser atualizada;
3. verificar se o README raiz continua correto;
4. adicionar a entrada apropriada ao `CHANGELOG.md`;
5. preservar as regras do `AGENTS.md` global;
6. preservar as regras do `AGENTS.md` local;
7. informar claramente o que foi alterado;
8. informar qualquer pendência ou limitação identificada.

Uma tarefa relevante não deve ser considerada concluída enquanto código, documentação e histórico do projeto estiverem inconsistentes entre si.

