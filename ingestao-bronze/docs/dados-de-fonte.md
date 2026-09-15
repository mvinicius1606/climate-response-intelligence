# Fontes de dados do MVP histórico

| Domínio | Instituição | Dataset selecionado | Papel | Granularidade | Formato | Status |
| --- | --- | --- | --- | --- | --- | --- |
| IBGE | IBGE | SIDRA 4714: população, área e densidade | FEATURE ESTRUTURAL | Município / Censo 2022 | JSON | Acesso e amostra confirmados; versão de 2024 pendente |
| IBGE | IBGE | SIDRA 9514: população por idade | FEATURE ESTRUTURAL | Município × idade / 2022 | JSON | Acesso e amostra confirmados |
| IBGE | IBGE | SIDRA 6803: abastecimento de água | FEATURE ESTRUTURAL | Município × categoria / 2022 | JSON | Acesso e amostra confirmados |
| IBGE | IBGE | SIDRA 6805: esgotamento sanitário | FEATURE ESTRUTURAL | Município × categoria / 2022 | JSON | Acesso e amostra confirmados |
| IBGE | IBGE | SIDRA 6326: tipo de domicílio | FEATURE ESTRUTURAL | Município × categoria / 2022 | JSON | Acesso e amostra confirmados |
| Hidrometeorologia | INMET | Acervo automático anual de 2024 | FEATURE TEMPORAL | Estação × hora | ZIP / CSV | Índice e amostra A801 confirmados |
| Defesa Civil / logística | Governo RS / Secom | Coletivas de 09 e 10/05/2024 | GROUND TRUTH, REFERÊNCIA, LOGÍSTICA | Totais estaduais e trechos pontuais / publicação | PDF | Dois documentos confirmados; série completa pendente |
| Defesa Civil | Governo RS / DOE | Decreto 57.614 de 13/05/2024 | REFERÊNCIA, GROUND TRUTH institucional | Município / ato | PDF | Conteúdo e cópia oficial confirmados |

**Verificação:** 15/09/2026. **Janela de interesse:** 27/04/2024 a 27/05/2024, inclusive. A seleção acima permite iniciar a aquisição de recortes verificáveis, mas **não demonstra ainda a viabilidade de uma reconstrução municipal completa com antecedência temporal**. ANA, S2ID, histórico rodoviário detalhado e versões disponíveis em cada momento possuem pendências explícitas.

**Atualização operacional de 15/09/2026:** a tentativa de carga real falhou com HTTP 403 na URL completa de ibge-abastecimento-agua, inclusive em segunda consulta com User-Agent explícito. As amostras históricas documentadas não comprovam disponibilidade atual dessa consulta. HEAD do bucket funcionou, mas nenhum upload foi realizado nessa execução. O executor agora valida formatos e recupera cargas parciais, com dez testes offline aprovados; detalhes em [INGESTAO.md](INGESTAO.md).
## Sumário

1. [Escopo e método](#1-escopo-e-método)
2. [IBGE — dados estruturais](#2-ibge--dados-estruturais)
3. [Hidrometeorologia — ANA e INMET](#3-hidrometeorologia--ana-e-inmet)
4. [Defesa Civil e S2ID](#4-defesa-civil-e-s2id)
5. [Logística](#5-logística)
6. [Rastreabilidade temporal](#6-rastreabilidade-temporal)
7. [Configurações e validação](#7-configurações-e-validação)
8. [Pendências e primeira ingestão recomendada](#8-pendências-e-primeira-ingestão-recomendada)

## 1. Escopo e método

A pesquisa inicial tratou de descoberta, validação documental e por amostragem, seleção e configuração. Em ação posterior autorizada, o executor das oito fontes foi implementado e validado por oito testes offline. Não houve carga real completa no S3. Este inventário mantém as evidências da pesquisa; implementação e limites operacionais estão em [INGESTAO.md](INGESTAO.md) e [ARCHTETURE.md](ARCHTETURE.md).

Foram lidos os `AGENTS.md` da raiz e da Bronze atualizados pelo autor. No início desta rodada, `STATUS.md` não existia; `config/config.yml`, os documentos técnicos da Bronze e os arquivos Python consultados estavam vazios. Não havia documentação equivalente de fontes a consolidar. Os placeholders foram preservados.

A prioridade de acesso foi API, endpoint de dados, download oficial, arquivo publicado e, por último, página HTML. A inspeção de páginas e pequenas amostras serviu apenas à validação; não constitui implementação de scraping. Resultados de busca ajudaram a localizar recursos, mas um resultado indexado não foi considerado prova de que o download continua disponível.

Neste documento, **confirmado** significa que o acesso e o conteúdo especificado foram verificados, dentro do recorte descrito. Não significa completude estadual, ausência de revisões ou adequação automática a uma simulação histórica. **NÃO CONFIRMADO** identifica informação ausente ou não verificável nesta rodada.

## 2. IBGE — dados estruturais

### 2.1. Acesso e características comuns

**Instituição:** Instituto Brasileiro de Geografia e Estatística. **Pesquisa:** Censo Demográfico 2022. **Método escolhido:** API SIDRA, GET público, retorno JSON com cabeçalho descritivo. A [documentação da API](https://apisidra.ibge.gov.br/home/ajuda) confirma a seleção de municípios de uma UF por `n6/in n3 43`; o espaço é codificado como `%20`. O período é `p/2022`, e não a janela meteorológica de 2024. A API limita cada consulta a 100 mil valores.

**Cobertura espacial:** nível municipal nacional disponível, com seleção do RS, UF 43. Foram consultadas amostras de Porto Alegre, código `4314902`. A completude de todos os municípios será medida na ingestão; as estimativas de volume abaixo usam 497 municípios como referência de dimensionamento, não como contagem de registros baixados.

**Granularidade e frequência:** referência censitária estática; o metadado “anual” não indica uma observação anual nova entre 2022 e 2024. Categorias acrescentam dimensões à linha.

**Identificadores e campos originais:** `D1C` é o código IBGE municipal, `D1N` o nome; `D2C/D2N` identificam a variável; `D3C/D3N`, o ano. `V` contém o valor, `MC/MN`, a unidade. As dimensões posteriores dependem da tabela. O nome futuro `codigo_ibge_municipio` não é um campo original da API. A Bronze deverá preservar códigos como texto, valores, cabeçalho e símbolos de ausência, sem renomear nem agregar.

**Licença/termos:** [Termo de Uso e Política de Privacidade do Portal IBGE](https://www.ibge.gov.br/acesso-informacao/acoes-e-programas/politica-de-privacidade.html) localizado. Licença específica de reutilização por tabela: **NÃO CONFIRMADO**; não atribuir automaticamente CC BY ou domínio público.

**Observações para aquisição futura:** guardar os descritores junto à resposta e registrar a versão consultada. As URLs completas ficam nos YAML. As amostras usaram a mesma API com `n6/4314902` e poucas categorias; não foi baixado o recorte completo do RS.

### 2.2. SIDRA 4714 — identificação, população, área e densidade

- **Dataset e URL oficial:** [tabela 4714](https://sidra.ibge.gov.br/tabela/4714); [descritor JSON](https://apisidra.ibge.gov.br/DescritoresTabela/t/4714).
- **Objetivo / papel:** fornecer identificação e contexto de escala municipal; FEATURE ESTRUTURAL.
- **Acesso / formato:** API SIDRA / JSON; ano 2022; município × variável; referência estática.
- **Campos selecionados:** variável `93`, população em pessoas; `6318`, área em km²; `614`, densidade em habitantes/km². Identificadores comuns da seção 2.1, sem classificação adicional.
- **Amostra:** Porto Alegre retornou população `1332845`, área `495.390` e densidade `2690.50`. São os valores disponíveis na consulta atual.
- **Volume:** aproximadamente 1.491 valores no RS, excluindo cabeçalho.
- **Limitação temporal:** o descritor atual informa `DataAtualizacao=2026-05-07 16:37:12` e `DataLiberacao=2026-05-07 16:37:10`. A nota da tabela menciona revisões de 2023. Isso comprova que o ano de referência e a data da versão são coisas diferentes; não demonstra quais campos do RS mudaram.
- **Status:** acesso, schema e amostra confirmados. O autor aceita a atualização em 2026 para uso histórico da referência 2022. Equivalência à versão acessível em abril de 2024: **NÃO CONFIRMADO**, sem bloquear o uso autorizado; só é necessária caso uma futura avaliação exija reproduzir a informação disponível naquele momento.
- **Configuração:** [ibge-populacao-area.yml](../config/ibge-populacao-area.yml). Termos e preservação: seção 2.1.

### 2.3. SIDRA 9514 — população por idade

- **Dataset e URL oficial:** [tabela 9514](https://sidra.ibge.gov.br/tabela/9514); [descritor JSON](https://apisidra.ibge.gov.br/DescritoresTabela/t/9514).
- **Objetivo / papel:** disponibilizar faixas etárias para análise posterior de necessidades de crianças e idosos; FEATURE ESTRUTURAL.
- **Acesso / formato / cobertura:** API / JSON; municípios, incluindo RS; referência 2022.
- **Seleção:** população `93`; sexo `c2/6794` (total); declaração da idade `c286/113635` (total); 21 grupos etários nativos de 0–4 a 95–99 e 100 anos ou mais. Os códigos estão na URL do YAML.
- **Identificadores adicionais:** `D4C` sexo, `D5C` idade e `D6C` declaração da idade.
- **Amostra:** Porto Alegre, 0–4 anos: `64258`; 60–64 anos: `82145`.
- **Disponibilidade:** descritor atualizado em 22/12/2023, anterior ao evento. Ainda se deve preservar o descritor consultado como evidência da versão.
- **Volume:** cerca de 10.437 valores para 497 municípios × 21 categorias.
- **Limitações:** os grupos escolhidos não fixam uma definição de “criança” ou “idoso”. Um corte que atravesse uma faixa exigirá idades simples em ação futura. Não somar simultaneamente grupos, idades simples e totais. Sexo não foi desagregado por falta de necessidade específica autorizada.
- **Status:** fonte e amostra confirmadas. **Configuração:** [ibge-demografia.yml](../config/ibge-demografia.yml). Termos e preservação: seção 2.1.

### 2.4. SIDRA 6803 — abastecimento de água

- **Dataset e URL oficial:** [tabela 6803](https://sidra.ibge.gov.br/tabela/6803); [descritor JSON](https://apisidra.ibge.gov.br/DescritoresTabela/t/6803).
- **Objetivo / papel:** caracterizar condições estruturais de acesso à água; FEATURE ESTRUTURAL.
- **Acesso / formato / cobertura:** API / JSON; município × categoria, RS; Censo 2022, estático.
- **Campos:** variável `381`, domicílios particulares permanentes ocupados; classificação `1821`, ligação à rede e forma principal de abastecimento; `D4C/D4N` identificam a categoria. O YAML mantém as categorias nativas da classificação.
- **Amostra:** Porto Alegre: total `558252`; ligação à rede usada como forma principal `553331`; sem ligação à rede `3431`.
- **Disponibilidade:** descritor com liberação e atualização em 23/02/2024 às 10h.
- **Volume:** 18 categorias retornadas na amostra; aproximadamente 8.946 valores para 497 municípios. Inclui categorias hierárquicas.
- **Limitações:** ligação à rede não mede disponibilidade de água durante a enchente. Existem totais e subcategorias sobrepostos; não somá-los indiscriminadamente. Esta tabela não substitui uma medida de renda.
- **Status:** fonte e amostra confirmadas. **Configuração:** [ibge-abastecimento-agua.yml](../config/ibge-abastecimento-agua.yml). Termos e preservação: seção 2.1.

### 2.5. SIDRA 6805 — esgotamento sanitário

- **Dataset e URL oficial:** [tabela 6805](https://sidra.ibge.gov.br/tabela/6805); [descritor JSON](https://apisidra.ibge.gov.br/DescritoresTabela/t/6805).
- **Objetivo / papel:** caracterizar condições sanitárias municipais; FEATURE ESTRUTURAL.
- **Acesso / formato / cobertura:** API / JSON; município × categoria, RS; 2022, estático.
- **Campos:** variável `381`, classificação `11558`; `D4C/D4N` para esgotamento. Há rede, fossas, vala, lançamento em corpos hídricos, outra forma e ausência de banheiro/sanitário.
- **Amostra:** Porto Alegre: total `558252`; fossa rudimentar ou buraco `6412`.
- **Disponibilidade:** liberação e atualização em 23/02/2024 às 10h.
- **Volume:** dez categorias retornadas na amostra; aproximadamente 4.970 valores para 497 municípios.
- **Limitações:** o estado de 2022 não representa danos em 2024; nenhuma categoria foi convertida em score. Preservar hierarquias e totais.
- **Status:** fonte e amostra confirmadas. **Configuração:** [ibge-esgotamento.yml](../config/ibge-esgotamento.yml). Termos e preservação: seção 2.1.

### 2.6. SIDRA 6326 — características habitacionais

- **Dataset e URL oficial:** [tabela 6326](https://sidra.ibge.gov.br/tabela/6326); [descritor JSON](https://apisidra.ibge.gov.br/DescritoresTabela/t/6326).
- **Objetivo / papel:** disponibilizar tipos de moradia, incluindo estruturas degradadas ou inacabadas, como contexto habitacional; FEATURE ESTRUTURAL.
- **Acesso / formato / cobertura:** API / JSON; município × tipo, RS; 2022, estático.
- **Campos:** variável `381`, classificação `125`, sete categorias incluindo total; `D4C/D4N` identificam o tipo.
- **Amostra:** Porto Alegre: total `558252`; estrutura residencial permanente degradada ou inacabada `109`.
- **Disponibilidade:** liberação e atualização em 23/02/2024 às 10h.
- **Volume:** cerca de 3.479 valores no RS.
- **Limitações:** cobre domicílios particulares permanentes ocupados; não equivale ao universo de moradias improvisadas nem mede diretamente resistência a inundação. Tipo de moradia não determina vulnerabilidade individual.
- **Status:** fonte e amostra confirmadas. **Configuração:** [ibge-habitacao.yml](../config/ibge-habitacao.yml). Termos e preservação: seção 2.1.

### 2.7. Renda e alternativas não selecionadas

A [tabela 10295](https://sidra.ibge.gov.br/tabela/10295) foi identificada e teve [metadados consultados](https://servicodados.ibge.gov.br/api/v3/agregados/10295/metadados): renda domiciliar per capita média (`13431`) e mediana (`13534`), com nível municipal e referência 2022. A divulgação de [Trabalho e Rendimento do Censo](https://www.ibge.gov.br/estatisticas/Sociais/populacao/22827-censo-demografico-2022.html?edicao=44663) é de 2025. O [calendário oficial](https://www.ibge.gov.br/calendario/mensal.html?ano=2025&mes=4) também situa o rendimento do responsável pelo domicílio em 30/04/2025.

**Decisão:** não selecionar renda divulgada após a enchente como informação que estaria disponível em abril/maio de 2024. Não há YAML dessa alternativa; amostra de valores não foi necessária para a exclusão temporal. Renda municipal compatível com o corte histórico permanece **PENDENTE**. Saneamento e habitação cobrem dimensões distintas e não substituem renda.

A [listagem oficial de características dos domicílios](https://sidra.ibge.gov.br/pesquisa/censo-demografico/demografico-2022/universo-caracteristicas-dos-domicilios) também oferece canalização, lixo e cruzamentos por moradores. Não foram acrescentados para evitar redundância e expansão indiscriminada. Malhas e setores censitários não foram selecionados nesta ação.

## 3. Hidrometeorologia — ANA e INMET

### 3.1. ANA — inventário e séries do HidroWebService

**Instituição / objetivo / papel:** ANA; localizar estações e séries de chuva, cota e vazão; FEATURE TEMPORAL e REFERÊNCIA espacial. [Swagger oficial](https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html) e [manual de 20/02/2026](https://www.gov.br/ana/pt-br/assuntos/monitoramento-e-eventos-criticos/monitoramento-hidrologico/orientacoes-manuais/manuais/manual-hidrowebservice_publica.pdf) foram consultados.

**Acesso documentado:** API REST/JSON autenticada. O manual exige cadastro solicitado à ANA. A consulta pública de inventário para `87450004` retornou HTTP 401, sem dados. Nenhuma credencial foi procurada ou inserida.

**Schema documentado:** código e nome de estação, coordenadas, área de drenagem, bacia, município e datas de operação; nas séries adotadas, chuva em mm, cota em cm, vazão em m³/s, flags de qualidade, `Data_Hora_Medicao` e `Data_Atualizacao`. O `Municipio_Codigo` do Hidro **não é código IBGE**. O exemplo do manual é de outra região; não valida cobertura do RS.

O Swagger anuncia inventário, rios, bacias e sub-bacias; séries convencionais de chuva/cotas/vazão e séries telemétricas adotadas/detalhadas. A versão v1 limita séries telemétricas a 30 dias por consulta e convencionais a 366; v2 anuncia consulta adotada para até dez estações. Essas rotas foram verificadas no OpenAPI, sem executar séries. O limite de busca não prova frequência de medição.

**Cobertura do evento:** a [comunicação da ANA de 07/05/2024](https://www.gov.br/ana/pt-br/assuntos/noticias-e-eventos/noticias/ana-divulga-dados-de-monitoramento-de-niveis-de-agua-do-lago-guaiba-do-rio-uruguai-e-da-lagoa-dos-patos-rs) identifica Cais Mauá C6 (`87450004`), Arambaré (`87540000`), Laranjal (`87955000`), Rio Grande/Regatas (`87980000`) e São Lourenço (`87921000`). Informa disponibilização horária no Guaíba e início de disponibilização de quatro estações da lagoa dos Patos em 05/05. Também registra interrupções em sete estações das bacias Taquari-Antas e Caí.

Isso confirma monitoramento durante o desastre, mas a recuperação das séries de 27/04 a 27/05, sua completude, vazões efetivamente presentes, frequência por estação, fuso e histórico anterior suficiente para referências permanecem **NÃO CONFIRMADOS**.

**Limitações e aquisição futura:** medições diárias convencionais não sustentam variações de 6h/12h; serão necessárias séries subdiárias. Coordenadas, rio, bacia, sub-bacia e área de drenagem devem subsidiar a relação espacial futura; proximidade não basta. Dados consistidos ou atualizados posteriormente não demonstram disponibilidade operacional histórica.

**Alternativa legada:** o [aviso da ANA](https://telemetriaws1.ana.gov.br/Dados.aspx) informa prazo de manutenção do serviço antigo até 30/06/2026. Não se presume que permaneça operacional em setembro de 2026. O [portal HidroWeb](https://www.snirh.gov.br/hidroweb/) é alternativa oficial para consulta/download manual; exportação específica do período não validada nesta rodada.

**Volume:** NÃO CONFIRMADO para o recorte; depende de estações, frequência e lacunas. **Licença específica:** NÃO CONFIRMADO. **Status:** documentação e estações candidatas identificadas; dados históricos ainda não validados. **Configuração:** não criada.

### 3.2. INMET — precipitação horária

**Instituição:** Instituto Nacional de Meteorologia. **Dataset:** dados históricos anuais de estações automáticas, ano 2024. **Objetivo / papel:** complementar a pluviometria oficial, dentro do domínio hidrometeorológico autorizado; FEATURE TEMPORAL. Não substitui cota ou vazão da ANA.

**URLs:** [catálogo oficial](https://portal.inmet.gov.br/dadoshistoricos) e [ZIP 2024](https://portal.inmet.gov.br/uploads/dadoshistoricos/2024.zip). **Método:** download direto; ZIP contendo CSV. O catálogo anual foi preferido a endpoints meteorológicos não documentados para reconstrução histórica.

**Validação:** HEAD retornou 200, `application/zip`, 102.772.199 bytes (aproximadamente 98 MiB). Consultas HTTP Range retornaram 206; foram lidos apenas o final do ZIP, seu índice e o membro A801 comprimido, total inferior a 400 KB transferidos nessa inspeção. O ZIP completo não foi baixado.

O índice contém 565 entradas, das quais 44 arquivos com prefixo `INMET_S_RS_`. A presença no índice não confirma completude de suas medições.

**Amostra:** `INMET_S_RS_A801_PORTO ALEGRE - JARDIM BOTANICO_01-01-2024_A_31-12-2024.CSV`; 227.967 bytes comprimidos e 838.928 descomprimidos. Cabeçalho: região S, UF RS, código rotulado `CODIGO (WMO): A801`, latitude `-30,05361111`, longitude `-51,17472221`, altitude `41,18`. Campos: `Data`, `Hora UTC` e `PRECIPITAÇÃO TOTAL, HORÁRIO (mm)`. CSV com separador ponto e vírgula e vírgula decimal; a leitura Windows-1252 preservou os acentos da amostra.

**Cobertura / granularidade / frequência:** estação × hora, arquivo anual de 2024. Entre 27/04/2024 00h e 27/05/2024 23h UTC foram encontradas 744 linhas, com três registros sem precipitação informada segundo a verificação de vazio/sentinela. Não houve cálculo de acumulados. A janela por datas locais exige conversão explícita e conferência das bordas, pois o arquivo usa UTC.

**Lacunas identificadas e aceitas pelo autor:** em 27/05/2024, às `0900 UTC`, `1000 UTC` e `1100 UTC` (06h, 07h e 08h de Brasília), as linhas da estação A801 existem, mas seus campos meteorológicos estão vazios. São 741 registros com precipitação preenchida e três sem valor no recorte de 744 horas. O autor autorizou prosseguir com a fonte apesar dessas três ausências, preservando exatamente o conteúdo original do INMET.

**Preservação na Bronze:** manter os bytes dos arquivos adquiridos e os campos vazios de origem, sem substituir por zero, interpolar, preencher, excluir linhas ou regravar o CSV com outra codificação, separador ou horário. A descrição das lacunas deve permanecer separada do dado bruto. A aceitação dessas três ausências não representa validação do impacto analítico final nem da completude das demais estações. O executor implementado preserva o ZIP nacional integralmente, sem abrir ou regravar CSVs; a carga real permanece pendente.
**Identificadores:** código da estação no cabeçalho e data/hora nas linhas; código IBGE municipal ausente. O nome de estação não é chave municipal. Rio, bacia e sub-bacia não constam no cabeçalho examinado.

**Volume futuro:** dezenas de CSV no RS; a amostra sugere ordem de dezenas de MB descomprimidos. É estimativa, não medição de todo o conjunto. O catálogo oferece anos anteriores, mas seu conteúdo e cobertura local não foram validados.

**Licença/termos:** licença específica do arquivo NÃO CONFIRMADA no catálogo consultado.

**Limitações:** somente uma estação teve conteúdo examinado. Valores ausentes não são chuva zero. O arquivo anual retrospectivo não informa quando cada observação se tornou pública nem preserva revisões anteriores. A API/portal disponibilizar hoje uma medição de 2024 não comprova point-in-time correctness. Uma tentativa inicial via Python teve conexão reiniciada mesmo após repetição fora do ambiente restrito; a leitura limitada via HTTP Range/.NET funcionou.

**Status:** acesso, índice, campos, frequência e cobertura da amostra confirmados; cobertura das demais estações e disponibilidade histórica operacional pendentes. **Configuração:** [inmet-precipitacao.yml](../config/inmet-precipitacao.yml).


## 4. Defesa Civil e S2ID

### 4.1. Coletivas oficiais — documentos acessíveis

**Instituição:** Governo RS/Secom, com dados atribuídos à Defesa Civil estadual. **Dataset:** apresentações de 09 e 10/05/2024. **Objetivo / papel:** preservar observações institucionais contemporâneas; GROUND TRUTH agregado e REFERÊNCIA. Os mesmos PDFs contêm logística; não devem ser adquiridos em duplicidade por dois extractors futuros.

**Acesso / URLs / volume:** download direto oficial de [09/05](https://www.estado.rs.gov.br/upload/arquivos/202405/2024-05-09-govrs-coletiva-atualizacao-chuvas-medidas-v1.pdf), 24 páginas e 8.705.753 bytes; [10/05](https://www.estado.rs.gov.br/upload/arquivos/202405/2024-05-10-govrs-coletiva-site-saude-13-esc-tje-itcdm-v2.pdf), 20 páginas e 6.467.666 bytes. Conteúdo textual examinado pelo navegador de pesquisa; HEAD direto confirmou 200 e PDF para ambos.

**Campos / cobertura:** número de municípios afetados, pessoas em abrigos, desalojados, afetados, feridos, desaparecidos e óbitos. Em 09/05 a referência da Defesa Civil é 12h; em 10/05, 9h. Na seção de 10/05 constam 435 municípios afetados e 113 óbitos.

**Granularidade / frequência / identificadores:** totais do RS por publicação; URL, data da coletiva e página/seção. Código IBGE ausente. Horários internos são referências da informação; hora exata da publicação do arquivo NÃO CONFIRMADA. O número de municípios afetados não é uma lista municipal nem distribuição dos danos.

**Licença:** específica dos PDFs NÃO CONFIRMADA. Os [termos do portal RS](https://www.estado.rs.gov.br/termos-de-uso) consultados tratam de navegação e não estabelecem uma licença de dados.

**Limitações / status:** dois documentos confirmados, insuficientes para uma série diária completa. Não mapear automaticamente “pessoas em abrigos” para toda a categoria de desabrigados. Preservar termos originais e eventuais divergências. **Configuração:** [rs-coletivas.yml](../config/rs-coletivas.yml).

### 4.2. Boletins HTML históricos — existência documentada, acesso atual pendente

Foram encontrados boletins oficiais de [13/05 às 9h](https://www.defesacivil.rs.gov.br/defesa-civil-atualiza-balanco-das-enchentes-no-rs-13-5-9h) e [13/05 às 12h](https://www.defesacivil.rs.gov.br/defesa-civil-atualiza-balanco-das-enchentes-no-rs-13-5-12h). O conteúdo indexado registra publicação às 09h04 e 12h07, respectivamente, e três edições diárias então previstas. O [boletim de 23/05](https://defesacivil.rs.gov.br/defesa-civil-atualiza-balanco-das-enchentes-no-rs-22-5-18h-664f353266e07) anuncia duas edições, 9h e 18h. Logo, a frequência não deve ser fixada em toda a janela.

No acesso direto, o boletim de 13/05 às 9h e o de 23/05 retornaram 404; o das 12h teve falha de obtenção no navegador de pesquisa. O conteúdo indexado não foi promovido a uma URL operacional validada. Os links anunciados para municípios afetados e óbitos não comprovam que anexos preservem a versão de cada boletim.

**Instituição / papel:** Defesa Civil RS / Secom; GROUND TRUTH e REFERÊNCIA. **Formato original:** HTML com links; formatos e conteúdo dos anexos municipais NÃO CONFIRMADOS. **Granularidade confirmada no texto indexado:** totais estaduais por boletim, sem código IBGE no corpo. **Cobertura integral, volume total e licença específica:** NÃO CONFIRMADOS. **Status:** recuperação histórica pendente; sem YAML.

### 4.3. Decreto estadual 57.614 — classificação municipal

**Instituição:** Governo do Estado/DOE; cópia oficial preservada pela Procuradoria-Geral do Município de Porto Alegre. **Dataset e acesso:** [PDF do Decreto 57.614, de 13/05/2024](https://legislacao.portoalegre.rs.gov.br/media/sapl/public/normajuridica/2024/48475/decreto_no_57.614.pdf), download direto, 11 páginas, 69.469 bytes; HEAD 200 e conteúdo conferido.

**Objetivo / papel:** referência da classificação administrativa municipal em uma data; REFERÊNCIA e GROUND TRUTH institucional, sem equivalência a colapso.

**Campos / identificadores:** número e data do decreto; nomes municipais nos anexos I e II, respectivamente calamidade e emergência; protocolo DOE `2024000999537`; publicação em 13/05/2024, a partir da página 20. Não há código IBGE; números ordinais dos anexos não são códigos municipais. Constam 46 municípios no anexo I e 320 no II.

**Cobertura / granularidade / frequência:** municípios listados do RS, por ato; não é cadastro de todos os municípios nem série de danos humanos. O ato informa evento iniciado em 24/04, anterior à janela inicial do projeto. Essa data deve ser preservada na origem, sem alterar silenciosamente o recorte.

**Limitações / termos:** confirmação restrita ao ato de 13/05. Cópia em órgão público distinta do publicador original, explicitamente identificada; licença de reutilização específica NÃO CONFIRMADA. A sequência completa de atos ainda precisa ser recuperada.

O [portal estadual noticia a alteração pelo Decreto 57.626](https://www.estado.rs.gov.br/decreto-amplia-numero-de-municipios-em-estado-de-calamidade-e-em-situacao-de-emergencia): publicação em 21/05 com efeitos retroativos a 13/05. Seu [link original no DOE](https://www.diariooficial.rs.gov.br/materia?id=1000161) exige JavaScript e o conteúdo integral não foi recuperado nesta rodada; a notícia também retornou 404 no acesso direto. O ato 57.626 permanece candidato, sem YAML. A evidência indexada indica por que vigência retroativa não pode ser confundida com conhecimento disponível em 13/05.

**Status:** 57.614 confirmado; cadeia de reclassificações pendente. **Configuração:** [rs-decreto-57614.yml](../config/rs-decreto-57614.yml).

### 4.4. S2ID — danos informados e reconhecimento federal

**Instituição:** MIDR/SEDEC. **Datasets candidatos:** Relatório Gerencial — Danos informados e relatórios de Reconhecimento Federal. **Objetivo / papel:** danos por município/evento e referência administrativa; GROUND TRUTH e REFERÊNCIA.

**URLs oficiais:** [relatórios S2ID](https://s2id.mi.gov.br/paginas/relatorios/index.xhtml?retorno=painel); [catálogo de dados abertos do MIDR](https://www.gov.br/mdr/pt-br/acesso-a-informacao/dados-abertos), que aponta para [S2ID — Dados Informados](https://dadosabertos.mdr.gov.br/dataset/s2id_sedec).

**Acesso confirmado na interface:** formulários, filtros de período, UF e tipologia, exportação CSV/XLS/PDF conforme o relatório; período máximo anunciado de 365 dias em danos informados. O catálogo de dados retornou “Request Rejected”. Não foi obtido um arquivo exportado do RS para a janela.

**Cobertura / granularidade / campos:** a interface permite selecionar RS e o ano de interesse em relatórios anuais. Granularidade efetiva do arquivo, código IBGE, protocolo, COBRADE, nomes exatos das colunas de danos, datas de reconhecimento e quantidade de registros do evento: **NÃO CONFIRMADOS por amostra**. A descrição do sistema não basta para prometer esses campos no export escolhido.

**Frequência / histórico / volume / licença:** NÃO CONFIRMADOS para o recurso efetivo. Não há evidência de snapshots intradiários ou de histórico de cada revisão. Um export atual pode refletir dados consolidados muito depois da ocorrência.

**Status:** candidato identificado; exportação, schema e cobertura pendentes; sem YAML. Próxima validação é obter pequeno recorte real pela interface oficial e confrontar datas, município e protocolo, sem confundir reconhecimento federal com decreto estadual.

## 5. Logística

### 5.1. Dados confirmados nas coletivas

**Instituição:** Governo RS/Secom; seções atribuídas a DAER, PRF e concessionárias. **Dataset / acesso / formato / volume / termos:** os dois PDFs da seção 4.1. **Papel:** LOGÍSTICA e REFERÊNCIA. **Cobertura:** pontos selecionados e totais do RS em 09 e 10/05; frequência por coletiva.

**Campos confirmados:** contagens de bloqueios totais, parciais e liberados, horário de referência, rodovia, km e localidade em exemplos pontuais. Na página 7 do PDF de 09/05, a ERS-122 aparece entre km 39 e 51, de Nova Milano/Farroupilha a São Vendelino, com bloqueio total por queda de barreiras e rompimento de pista. A referência da seção é 12h.

**Identificadores:** denominação da rodovia e quilometragem; não há chave estável de incidente nem código IBGE. Trecho pode envolver mais de um município.

**Limitação de qualidade:** a extração textual da página 5 de 09/05 traz total 131 e componentes 95 e 38, cuja soma difere. Não corrigir silenciosamente. A captura visual pelo navegador falhou; a divergência exige conferência manual no original. Em 10/05 o documento apresenta 91 totais, 39 parciais e 158 liberados, com referência 09h45.

**Status:** fonte confirmada para observações pontuais; não sustenta inventário completo por trecho. **Configuração compartilhada:** [rs-coletivas.yml](../config/rs-coletivas.yml).

### 5.2. Boletins de infraestrutura e mapas — histórico não demonstrado

Foram examinados os textos oficiais indexados de [08/05 às 18h](https://www3.estado.rs.gov.br/atualizacao-dos-servicos-de-infraestrutura-do-rs-8-5-18h), [22/05 às 18h](https://www.estado.rs.gov.br/atualizacao-dos-servicos-de-infraestrutura-do-rs-22-5-18h) e [23/05 às 9h](https://www.estado.rs.gov.br/atualizacao-dos-servicos-de-infraestrutura-do-rs-23-5-9h). Informam retomada do monitoramento em 30/04 e divulgação às 9h e 18h. A amostra de 08/05 retornou 404 no acesso direto; não se presume funcionamento atual das demais.

As páginas atribuem os dados a DAER/CRBM, incluindo rodovias concedidas e EGR. Contêm totais e links para [mapa de bloqueios](https://www.google.com/maps/d/u/0/viewer?mid=1ZlKA__gK8tH-WY6mbDeQzltsiwao7Q8) e [rotas alternativas do CRBM](https://crbm.app.br/gestao-de-rotas/index.php?class=RotaCardList). O vínculo institucional vem da página governamental; o domínio externo, sozinho, não seria suficiente.

**Resultado da comparação:** não foi localizada API ou export oficial com versões históricas verificáveis por trecho para abril/maio de 2024. Os mapas tiveram falhas de leitura ou ausência de conteúdo legível; não foi confirmado um arquivo de mudanças. Uma página de 2024 que aponta para mapa mutável não congela o estado desse mapa em 2024.

**Campos ainda necessários:** lista exaustiva de rodovia/trecho/km/município, tipo e causa do bloqueio, ponte, alagamento/deslizamento, liberação e rota alternativa com data/hora. **Identificadores, formato de export, volume e licença específica do histórico:** NÃO CONFIRMADOS. **Status:** pendente; sem YAML operacional para mapas ou HTML.

Ausência de registro não significa via disponível; queda nas contagens não demonstra liberação de um trecho específico. Não é possível concluir isolamento municipal apenas com totais estaduais ou um bloqueio próximo.

## 6. Rastreabilidade temporal

A aquisição futura deverá preservar separadamente:

| Conceito | Significado | Cuidado |
| --- | --- | --- |
| `occurred_at` | Momento do fenômeno ou ocorrência | Pode ser desconhecido ou apenas uma data |
| `observed_at` | Horário da medição ou referência do boletim | Pode diferir entre seções do mesmo documento |
| `published_at` | Quando a informação foi publicada | Não derivar do nome da URL, diretório ou data de medição |
| `retrieved_at` | Quando o projeto obteve o recurso | Será registrado na aquisição real, não simulado nesta ação |
| Atualização / revisão | Alteração posterior da informação | Não implica preservação do valor antes da revisão |
| Vigência administrativa | Efeito declarado de um ato | Retroatividade não retroage sua publicação |

Estas são orientações documentais, não um schema ou manifest implementado. Horários sem fuso explícito devem permanecer com essa incerteza. No INMET, o fuso de origem é UTC. Nos PDFs estaduais, horários de referência não comprovam hora de publicação.

Para responder “o que se sabia naquele momento”, será necessário conhecer a disponibilização de cada versão. Uma base retrospectiva pode servir à descrição do desastre e ainda ser inadequada a uma avaliação de antecipação. As três lacunas de chuva, as falhas de estações e as ausências de boletins não devem ser preenchidas com zero por conveniência.

Janelas futuras de 72h exigirão observações anteriores a 27/04; referências históricas exigirão anos anteriores. Nenhuma dessas features ou extensões de aquisição foi implementada.

## 7. Configurações e validação

Foram preparados oito YAML, um por tabela ou recurso/coletânea com mecanismo comum. `rs-coletivas.yml` reúne dois documentos da mesma série e atende a Defesa Civil e logística, evitando configurações duplicadas do mesmo arquivo.

Os YAML descrevem acesso, escopo e identificação. Não contêm transformações, thresholds, joins, credenciais ou regras analíticas. `status: validated` significa validação de acesso/conteúdo no recorte deste documento, não ingestão executada ou cobertura integral. O config loader implementado lê essas configurações e valida os mecanismos suportados antes dos acessos externos.

Não há parâmetro bronze_prefix nos YAMLs. A implementação usa source.id/nome-do-arquivo para o bruto e o sufixo .manifest.json para o manifest. O config.yml vazio, se existir, é ignorado pelo carregador.

### Evidências e limites dos checks

| Verificação | Resultado | Limite |
| --- | --- | --- |
| Domínios e origem | IBGE, INMET, Governo RS, ANA e S2ID identificados em portais oficiais | Links externos dependem de vínculo institucional explícito |
| IBGE | GET dos metadados/descritores e seleções finais limitadas a Porto Alegre: 3, 21, 18, 10 e 7 valores nas tabelas 4714, 9514, 6803, 6805 e 6326 | Não baixado o recorte completo dos municípios |
| Datas IBGE | Descritores atuais examinados | 4714 atualizada em 2026; referência 2022 aceita pelo autor, sem comprovação de igualdade com versão de 2024 |
| INMET | HEAD, Range 206, índice e CSV A801 examinados | Uma estação, 744 linhas da janela em UTC, três lacunas |
| ANA | OpenAPI/manual e códigos oficiais; inventário respondeu 401 | Séries não acessadas |
| RS PDFs | Conteúdo e HEAD 200 nos dois PDFs e no decreto | Cobertura pontual; captura visual das coletivas falhou |
| Boletins HTML | Existência em conteúdo oficial indexado | Amostras retornaram 404; recuperação operacional pendente |
| S2ID | Interface e catálogo consultados | Export e schema real não confirmados |
| Configuração | Parsing YAML e coerência com seleção/documento verificados na entrega | O executor foi posteriormente validado offline; carga real pendente |

As falhas de obtenção não demonstram que a instituição perdeu o dado; apenas limitam o que esta rodada conseguiu confirmar. As verificações são documentais, HTTP e de estrutura. Na ação posterior de implementação, oito testes offline passaram; eles não substituem as amostras reais registradas acima nem comprovam carga integrada. Consulte [validação da implementação](INGESTAO.md#validação-e-limites).

## 8. Pendências e primeira ingestão recomendada

| Pendência | Motivo / impacto | Próxima validação necessária |
| --- | --- | --- |
| Séries ANA no evento e histórico de referência | Acesso autenticado não disponível; lacunas conhecidas | Acesso concedido pela ANA e amostras de estações, frequência, fuso e revisões |
| Renda anterior ao evento | Divulgações localizadas são posteriores | Investigar alternativa municipal historicamente elegível em nova ação |
| Versão 2024 da tabela 4714, somente para simulação estrita futura | Não bloqueia o uso autorizado da referência 2022 | Comparar versões apenas se uma avaliação exigir informação disponível em 2024 |
| Chuva nas demais estações | Apenas A801 examinada | Matriz estação/período/variável e bordas de fuso, sem assumir representatividade |
| Impactos municipais ao longo do tempo | HTML/anexos e export S2ID não recuperados | Pequeno export real e inventário de versões dos boletins |
| Cadeia de decretos e reconhecimento federal | Confirmado apenas 57.614 em conteúdo integral | Recuperar atos anteriores/posteriores e distinguir publicação de vigência |
| Logística por trecho | Mapas sem histórico demonstrado | Arquivos oficiais datados ou registro de alterações do órgão |
| Licenças específicas | Não explicitadas nos recursos examinados | Localizar termos do dataset antes de definir redistribuição |

**Recomendação da pesquisa inicial, substituída pela implementação autorizada das oito fontes:** SIDRA **9514**, inicialmente um município e depois RS, mantendo os grupos de idade nativos. É JSON público, usa a chave IBGE, tem volume pequeno e descritor com atualização anterior ao desastre. A tabela 4714 também é simples, mas sua versão atual exige cuidado adicional para uso point-in-time.

O executor atual percorre os oito YAMLs existentes, sem reduzir automaticamente o recorte IBGE a um município. A próxima validação operacional é a carga real; nenhuma execução adicional está implícita nesta documentação. A validação integral da base temporal municipal permanece pendente. A pesquisa alternativa do histórico rodoviário aguarda confirmação do autor.
