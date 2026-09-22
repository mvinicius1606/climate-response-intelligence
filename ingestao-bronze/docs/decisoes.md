# Decisões técnicas da Ingestão Bronze

Os registros abaixo preservam o contexto de cada ação. Decisões posteriores podem atualizar os critérios anteriores; o estado operacional atual está em [STATUS.md](../STATUS.md).

## Sumário

- [Seleção inicial](#seleção-inicial-de-fontes-oficiais-para-a-reconstrução-histórica-de-2024)
- [Lacunas INMET](#aceitação-das-três-lacunas-do-inmet-com-preservação-do-original)
- [Atualização IBGE](#uso-histórico-da-tabela-ibge-atualizada-em-2026)
- [Implementação funcional](#implementação-funcional-das-oito-fontes-yaml)
- [Validação e recuperação](#validação-de-formatos-e-recuperação-de-carga-parcial)

## ANA mantida como fonte pendente e descartada do uso imediato

**Data:** 22/09/2026

**Status:** Validada

**Origem:** AUTOR + AGENTE

**Prompt relacionado:** “manter a ANA apenas como fonte pendente e descartar seu uso imediato para a enchente do RS enquanto a série histórica não for validada.”

### Contexto

A ANA respondeu com autenticação válida e com inventário de estações no RS, mas a investigação não conseguiu demonstrar série histórica confiável para a janela 27/04/2024 a 27/05/2024. O retorno observado consistiu em metadados de estação, não em chuva, nível ou vazão do evento. A fonte continua relevante como catálogo da rede hidrometeorológica, mas não é adequada para uso analítico imediato no projeto.

### O que foi feito

- validamos a autenticação da API da ANA;
- consultamos o inventário de estações do RS;
- testamos as rotas de série histórica de chuva, cota e vazão;
- confirmamos que os retornos relevantes para o projeto não produziram dados válidos para o período solicitado;
- registramos esse resultado documentando a ANA como fonte pendente e não validada.

### Decisão adotada

1. Manter a ANA como fonte pendente no projeto.
2. Descartar o uso imediato da ANA para a reconstrução da enchente do RS até que a série histórica da janela solicitada seja validada.
3. Usar o inventário apenas como catálogo de estação e como insumo para futuras investigações pontuais, não como dado analítico.
4. Não incluir dados ANA na base do MVP enquanto não houver confirmação real da série histórica do período.

### Por que foi feito

A ANA constitui uma fonte potencial para monitoramento hidrológico, mas a evidência atual não sustenta uso como dado oficial da enchente. O que foi obtido foi uma rede de estações e datas de atualização, e não a medição do evento. Essa distinção é decisiva para evitar construir uma base com dados incompletos ou indevidamente interpretados.

### Áreas afetadas

Documentação da Bronze, inventário de fontes, status da implementação e decisão operacional sobre fontes de dados. Nenhum contrato de Silver/Gold foi alterado.

### Validação

A validação foi feita diretamente nas respostas reais da API da ANA: autenticação 200 OK; inventário de RS retornou 27 itens; rotas de série histórica não produziriam registros confiáveis para 27/04 a 27/05/2024 no contexto da demanda do projeto.

### Limitações

A ANA continua sendo uma fonte potencial e pode ser revisitada em uma próxima investigação com filtros e endpoints específicos. Porém, no estado atual, não há evidência suficiente para incorporá-la ao fluxo analítico do projeto.

### Responsabilidade da decisão

O autor autorizou a manutenção da fonte em estado de investigação. O agente executou a validação e documentou a não-aptidão imediata do dado para a enchente do RS. A origem AUTOR + AGENTE representa essa divisão clara de responsabilidade.

## Seleção inicial de fontes oficiais para a reconstrução histórica de 2024

**Data:** 15/09/2026

**Status:** Validada quanto aos recursos e amostras explicitamente confirmados; validação integral do MVP pendente

**Origem:** AUTOR + AGENTE

**Prompt relacionado:** “Pesquisar, validar e documentar as fontes oficiais de dados necessárias para o MVP histórico”, retomado do zero após a atualização dos AGENTS.md.

### Contexto

O autor definiu os quatro domínios, a janela de 27/04 a 27/05/2024 e a necessidade de preservar point-in-time correctness. Autorizou pesquisa, pequenas amostras, escolha entre fontes oficiais equivalentes, documentação e configurações. A implementação da ingestão permaneceu fora do escopo.

### O que foi feito

Foram examinados catálogos oficiais, descritores, documentação de serviços, publicações e amostras. A evidência, as URLs e o resultado de cada tentativa relevante estão em [dados-de-fonte.md](dados-de-fonte.md).

### Decisão adotada

1. Selecionar as tabelas SIDRA 4714, 9514, 6803, 6805 e 6326 para população/área, idade, água, esgotamento e habitação, respectivamente. Usar a API JSON com referência 2022 e recorte municipal do RS.
2. Selecionar o acervo automático INMET de 2024 como fonte de precipitação horária, com conteúdo validado apenas na estação A801. O domínio hidrometeorológico do prompt já contempla pluviometria oficial.
3. Selecionar os PDFs oficiais das coletivas estaduais de 09 e 10/05/2024 para observações institucionais e rodoviárias pontuais. Reunir os documentos numa configuração compartilhada, pois o mesmo arquivo atende a dois domínios.
4. Selecionar o Decreto 57.614 de 13/05/2024, em cópia oficial preservada pela PGM de Porto Alegre, para classificação municipal naquela publicação.
5. Criar oito YAML descritivos, sem código, manifests ou configuração de fontes ainda não validadas.
6. Não tratar disponibilidade atual de dado histórico como comprovação de que a mesma versão estava disponível durante o evento.

### Por que foi feito

Os recursos selecionados possuem conteúdo e acesso verificáveis, com limites identificados. As APIs do IBGE reduzem o esforço de aquisição e preservam códigos geográficos. O INMET oferece chuva horária confirmada por amostra. Os PDFs e o decreto permitem preservar evidências datadas mesmo diante de falhas no acesso atual a páginas históricas.

A seleção não afirma que os quatro domínios já oferecem cobertura suficiente para uma base municipal completa.

### Alternativas consideradas

- ANA/HidroWebService: documentação e estações identificadas, mas acesso a inventário retornou 401 pois precisa de autorização de acesso da API, tendo que ser realizada pelo Autor posteriormente das outras fontes.
- S2ID: relatórios e filtros oficiais localizados; export municipal e schema não validados. Permanece pendência.
- Boletins HTML e mapas de rodovias: resultados indexados não bastam; houve 404 em acessos diretos e não foi demonstrado histórico dos mapas.
- Rendimento do Censo divulgado em 2025: excluído do recorte de informação disponível em abril/maio de 2024.
- Variáveis adicionais de domicílio: não selecionadas por ausência de necessidade concreta além do recorte inicial.

### Áreas afetadas

Somente documentação e configuração da Bronze. Nenhum contrato executável entre etapas foi alterado. As exigências temporais ficam documentadas para avaliação futura, sem implementar Silver, features ou targets.

### Validação

Consulta HTTP de descritores e pequenas amostras JSON do IBGE; HEAD e leitura parcial via Range do ZIP INMET; leitura do CSV A801; inspeção de conteúdo e HEAD dos PDFs selecionados; consulta de manual/OpenAPI ANA e interfaces S2ID; parsing dos YAML e verificação da coerência dos arquivos na entrega.

O inventário completo de resultados, inclusive falhas e validações não realizadas, está em [dados-de-fonte.md](dados-de-fonte.md#7-configurações-e-validação).

### Limitações

A tabela 4714 informa atualização em 2026 e sua equivalência histórica é pendente. Há três lacunas de precipitação na amostra INMET. Os PDFs não constituem série municipal completa; a extração textual de uma contagem rodoviária exige conferência visual. O decreto confirmado é apenas um ato da sequência. Licenças específicas dos recursos não foram confirmadas.

### Responsabilidade da decisão

O autor definiu objetivo, limites e autorização para seleção. O agente realizou a investigação e escolheu os recursos dentro dessa autorização. A origem AUTOR + AGENTE expressa essa divisão de responsabilidade; não registra uma aprovação posterior do autor que não ocorreu.

A recomendação de primeira ingestão é a tabela 9514, por acesso simples e descritor anterior ao evento. Sua implementação exige nova unidade de trabalho.

## Aceitação das três lacunas do INMET com preservação do original

**Data:** 15/09/2026

**Status:** Validada quanto à autorização do autor; ingestão pendente

**Origem:** AUTOR

**Prompt relacionado:** autorização para prosseguir com os três dados faltantes, mantendo exatamente o conteúdo recebido do site.

### Contexto e decisão adotada

A amostra da estação A801 contém três linhas com campos meteorológicos vazios em 27/05/2024, às 09h, 10h e 11h UTC. O autor aceita essas ausências como não impeditivas para prosseguir com a fonte e determina a preservação integral do arquivo original na Bronze, incluindo campos vazios, linhas, codificação, separadores e horários. Não preencher, interpolar, substituir por zero ou excluir os registros. Documentar a ausência separadamente do dado bruto.

### Validação e limites

Os horários foram identificados na leitura do CSV oficial e apresentados ao autor antes desta autorização. A decisão registra a aceitação das lacunas conhecidas; não demonstra ausência de impacto nos resultados analíticos finais ou completude das demais estações. Nenhum dado foi modificado e nenhuma ingestão foi implementada nesta ação.

### Áreas afetadas

Inventário de fontes e orientação documental da configuração INMET. O estado da implementação permanece pendente.

## Uso histórico da tabela IBGE atualizada em 2026

**Data:** 15/09/2026
**Status:** Validada quanto ao critério de seleção
**Origem:** AUTOR
**Prompt relacionado:** esclarecimento de que a atualização em 2026 é aceitável se os dados históricos estiverem presentes.

### Decisão e validação

Utilizar a referência 2022 da tabela 4714 já confirmada por amostra, sem exigir uma cópia publicada antes das enchentes. O ano de referência e a data de atualização continuam registrados separadamente. A autorização não comprova igualdade com a versão disponível em 2024 e não adiciona novas tabelas ao escopo.

## Implementação funcional das oito fontes YAML

**Data:** 15/09/2026
**Status:** Validada offline; carga integrada no S3 pendente
**Origem:** AUTOR + AGENTE
**Prompt relacionado:** implementar a primeira versão funcional da Bronze somente para os oito YAMLs existentes, com funções simples e validação sem downloads grandes.

### Contexto e decisão adotada

A pesquisa inicial foi seguida por autorização explícita para implementar cinco fontes IBGE, uma INMET e duas RS. Essa ação substitui a recomendação anterior de implementar primeiro apenas a tabela 9514.

O autor definiu a arquitetura funcional: gatilhador, config_loader, extractor, metadata e aws. Foram implementados três mecanismos compartilhados de extração, com retorno em lista de dicts. O ZIP é preservado integralmente, e o manifest reutiliza a configuração original por cópia profunda.

### Por que foi feito

As fontes compartilham mecanismos de acesso. Funções comuns mantêm o fluxo compreensível e evitam duplicação por YAML. HTTP utiliza urllib da biblioteca padrão; PyYAML, boto3 e python-dotenv atendem às demais responsabilidades.

Sem convenção detalhada de chave preexistente, adotou-se source.id/nome-do-arquivo e o sufixo .manifest.json. A exigência de preservar originais motivou uploads condicionais, sem sobrescrita. Para APIs sem nome de arquivo JSON na URL, o nome é source.id.json.

### Áreas afetadas

Implementação, dependências, testes e documentação da Bronze. Nenhuma fonte nova ou etapa posterior foi implementada.

### Validação

Oito testes offline passaram na ação de implementação, verificando oito configurações, nove originais, 18 uploads simulados, dispatch, múltiplos recursos PDF, preservação de bytes, checksum, cópia independente e serialização do manifest, configuração AWS e propagação de falhas. Imports e suporte do SDK instalado a IfNoneMatch foram conferidos. Não houve download completo ou upload real.

### Alternativas consideradas e limitações

Classes por fonte, factories e services foram excluídos pelo autor. Requests não foi necessário diante do acesso HTTP disponível na biblioteca padrão. Não há retry HTTP automático, validação semântica dos arquivos ou recuperação automática de carga parcial.

Os dois uploads não são transacionais. O conteúdo permanece em memória por fonte; repetir uma carga com chaves existentes falha. Essas limitações estão detalhadas em [INGESTAO.md](INGESTAO.md).

### Responsabilidade da decisão

O autor definiu objetivo, arquitetura, mecanismos e preservação dos originais. O agente implementou os detalhes internos, escolheu urllib e a convenção mínima de chaves dentro da autonomia concedida e realizou a validação offline. Não se registra aprovação de uma carga real que não ocorreu.

## Validação de formatos e recuperação de carga parcial

**Data:** 15/09/2026
**Status:** Validada offline; integração real pendente por HTTP 403 no IBGE
**Origem:** AUTOR + AGENTE
**Prompt relacionado:** corrigir os problemas encontrados na vistoria e documentar conforme os AGENTS.

### Contexto

A vistoria demonstrou aceitação de HTML como JSON e impossibilidade de retomar um original cujo manifest falhou. O autor autorizou corrigir os pontos e realizar a validação pendente. Esta decisão atualiza os limites operacionais da primeira implementação, preservando os registros anteriores como histórico.

### Decisão adotada e motivo

Validar minimamente o formato sem modificar os bytes: JSON parseável e não vazio, rejeição de objetos de erro, estrutura ZIP e assinatura/terminador PDF. A validação não certifica qualidade analítica.

Manter uploads condicionais. Acrescentar metadata ingestion e hash da configuração ao objeto bruto para recuperar manifests ausentes com o timestamp original e configuração compatível. Reler bruto e manifest no S3; comparar tamanho, checksum e conteúdo do manifest. Preservar pares existentes compatíveis e bloquear divergências, sem exclusão ou sobrescrita.

### Validação

Dez testes offline passaram. A regressão de retomada simula falha do manifest, repete com outro timestamp, confirma preservação da aquisição original e rejeita bytes diferentes. A regressão de formato rejeita HTML para os três mecanismos e JSON inválido ou de erro.

HEAD do bucket configurado foi bem-sucedido. A execução real de 15/09/2026 foi interrompida no primeiro download IBGE com HTTP 403, repetido em consulta com identificação explícita do cliente. Nenhum upload foi realizado nessa execução. A integração completa não está validada.

### Áreas afetadas e limites

Extractor, persistência AWS, testes e documentação. Nenhum YAML de fonte, dado original ou etapa posterior foi alterado. A retomada exige bytes idênticos, metadata de recuperação e permissões de leitura. Não existe recuperação automática para originais legados sem essa metadata. Os uploads não são transacionais; a releitura aumenta tráfego e memória.

### Responsabilidade da decisão

O autor autorizou a correção e a documentação. O agente definiu os detalhes de validação e recuperação dentro da arquitetura funcional existente, executou os testes e relatou o bloqueio externo. Não se presume conclusão da carga real ou mudança do escopo de fontes.
