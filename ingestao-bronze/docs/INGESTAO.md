# Execução da ingestão Bronze

## Fluxo

O executor percorre oito YAMLs validados e produz nove originais e nove manifests numa carga completa. A arquitetura e o lineage estão em [ARCHTETURE.md](ARCHTETURE.md); decisões e autoria estão em [decisoes.md](decisoes.md).

A aquisição preserva os bytes de JSON, ZIP e PDF. Antes do envio, verifica JSON parseável e não vazio (rejeitando objetos de erro), estrutura ZIP e assinatura/terminador PDF. Essa inspeção não regrava JSON, não extrai CSVs e não trata o conteúdo dos PDFs. Não certifica schema, completude, CRC de todos os membros ZIP ou validade de todas as estruturas PDF.

## Executar

No diretório ingestao-bronze:

```powershell
python -m pip install -r requirements.txt
python gatilhador.py
```

O comando baixa arquivos reais, incluindo o ZIP nacional INMET. As variáveis locais são BUCKET_BRONZE, AWS_REGION, AWS_ACESS_KEY_ID e AWS_SECRET_ACCESS_KEY. O nome padrão AWS_ACCESS_KEY_ID e AWS_SESSION_TOKEN também são aceitos. O ambiente prevalece sobre os arquivos .env da etapa e da raiz. Nunca versionar credenciais.

O bucket deve existir. A execução requer s3:PutObject e s3:GetObject; para distinguir objeto ausente de acesso negado, s3:ListBucket pode ser necessário. Erros de autorização são propagados, não tratados como ausência.

## Preservação, verificação e retomada

As chaves continuam source.id/filename e source.id/filename.manifest.json. A API sem nome JSON na URL usa source.id.json.

1. O original é enviado com IfNoneMatch="*", metadata ingestion e hash da configuração.
2. O objeto é relido: tamanho e SHA-256 devem corresponder ao conteúdo adquirido.
3. Um manifest existente compatível é preservado, inclusive seu timestamp e configuração históricos.
4. Se estiver ausente, a metadata do original fornece retrieved_at da primeira aquisição; o hash da configuração deve coincidir antes de reconstruí-lo.
5. O manifest é enviado sem sobrescrita e relido para conferência.

Uma repetição com os mesmos bytes pode completar uma carga parcial ou reconhecer um par existente. Conteúdo diferente, configuração divergente durante recuperação ou manifest incompatível interrompem a execução sem apagar objetos. Originais legados sem metadata de recuperação exigem análise manual; não se inventa o timestamp original.

Os envios continuam não transacionais. A retomada exige que a fonte volte a fornecer os mesmos bytes e que ninguém altere os objetos por outro cliente. Não há Object Lock, versionamento automático ou retry HTTP. A configuração histórica do manifest existente não é substituída pela atual.

## Validação e limites

```powershell
python -B -m unittest discover -s tests -v
```

Dez testes offline passaram após as correções, incluindo rejeição de respostas incompatíveis e retomada após falha do manifest, com preservação de timestamp e bloqueio de conteúdo diferente. Os testes anteriores de carregamento, dispatch, múltiplos PDFs, bytes, checksum, serialização, configuração AWS e orquestração continuam aprovados.

Em 15/09/2026, o HEAD do bucket configurado foi bem-sucedido. A execução real parou na primeira fonte, ibge-abastecimento-agua, por HTTP 403. Uma segunda consulta à mesma URL com User-Agent explícito também retornou 403. Nenhum objeto foi enviado por essa execução. Não foi demonstrada permissão real de PutObject/GetObject nem a conclusão da carga.

Próxima validação necessária: resolver o acesso à URL IBGE e repetir a execução, conferindo os nove pares no S3. ANA permanece fora do escopo. As três ausências INMET e a referência IBGE 2022 atualizada em 2026 continuam aceitas.

O conteúdo é mantido em memória por fonte; a releitura do original acrescenta memória e tráfego proporcionais ao arquivo.
