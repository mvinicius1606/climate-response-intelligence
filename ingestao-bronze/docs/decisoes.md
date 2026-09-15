# Decisões técnicas da Ingestão Bronze

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
