# AGENTS.md — Ingestão Bronze

## 1. Finalidade

Este arquivo complementa o `AGENTS.md` da raiz com regras específicas da etapa:

```text
ingestao-bronze/
```

O **Prompt Inicial** define a ação atual, o escopo, os arquivos que podem ser alterados, as validações necessárias e quais documentações devem ser atualizadas.

Este arquivo define somente o padrão de implementação da Bronze.

Não define automaticamente a próxima tarefa.

---

# 2. Responsabilidade da Bronze

A camada Bronze é responsável por:

```text
fonte externa
↓
extração
↓
preservação dos bytes originais
↓
metadata / manifest
↓
armazenamento S3
```

A Bronze deve preservar o dado recebido da fonte da forma mais próxima possível do original.

Não pertencem à Bronze:

* limpeza analítica;
* padronização de negócio;
* joins;
* preenchimento de nulos;
* feature engineering;
* agregações analíticas;
* conversão para modelos Silver;
* Machine Learning.

Essas responsabilidades pertencem às etapas posteriores.

---

# 3. Princípio de simplicidade

A implementação deve favorecer o código mais simples que resolva corretamente o problema atual.

Não criar abstrações antecipadamente.

Evitar:

* classes por fonte;
* Factory;
* Strategy;
* interfaces sem necessidade real;
* services apenas para aumentar separação;
* models para estruturas simples que podem ser `dict`;
* uma função diferente para cada YAML quando várias fontes usam o mesmo mecanismo;
* módulos vazios criados apenas para obedecer uma estrutura teórica.

Adicionar novas abstrações somente quando surgir uma necessidade concreta.

---

# 4. Arquitetura atual da Bronze

A arquitetura definida atualmente é:

```text
gatilhador.py
    ↓
config_loader.py
    ↓
configs YAML → dict Python
    ↓
extractor.py
    ↓
bytes originais
    ↓
metadata.py
    ↓
manifest
    ↓
aws.py
    ↓
S3 Bronze
```

Estrutura esperada:

```text
ingestao-bronze/
│
├── gatilhador.py
├── config/
│   └── *.yml
│
├── src/
│   ├── config_loader.py
│   ├── extractor.py
│   ├── metadata.py
│   └── aws.py
│
├── tests/
├── docs/
├── requirements.txt
└── Dockerfile
```

Essa estrutura pode evoluir quando uma necessidade real aparecer.

Não expandi-la preventivamente.

---

# 5. `gatilhador.py`

`gatilhador.py` é o ponto de entrada da aplicação e o orquestrador do fluxo.

Sua lógica deve permanecer simples e legível.

Modelo conceitual:

```python
configs = carregar_configs()

for config in configs:
    arquivos = extrair(config)

    for arquivo in arquivos:
        manifest = gerar_manifest(config, arquivo)
        enviar_aws(arquivo, manifest)
```

Responsabilidades:

* iniciar a execução;
* obter as configurações;
* percorrer as fontes;
* chamar extração;
* chamar geração de metadata;
* chamar persistência;
* informar início, erro e término da execução.

Não deve implementar diretamente:

* HTTP;
* parsing de YAML;
* cálculo de checksum;
* regras específicas de download;
* chamadas detalhadas do boto3.

---

# 6. `config_loader.py`

Responsável exclusivamente por transformar os arquivos YAML em estruturas Python utilizáveis pelo restante da aplicação.

Fluxo:

```text
arquivo .yml
↓
yaml.safe_load
↓
dict Python
```

Deve:

* localizar os YAMLs válidos em `config/`;
* ignorar arquivos que não representam fontes;
* carregar YAML com segurança;
* retornar estruturas Python;
* validar somente o mínimo necessário para impedir configurações inválidas de seguirem no fluxo.

Não deve:

* acessar internet;
* baixar arquivos;
* gerar manifest;
* acessar AWS.

---

# 7. Configurações YAML

Cada YAML representa uma fonte ou recurso de dados.

Os YAMLs devem concentrar principalmente informações descritivas e parâmetros de acesso, como:

```yaml
source:
access:
scope:
granularity:
identifiers:
status:
```

Exemplo de acesso:

```yaml
access:
  type: "API"
  method: "GET"
  url: "..."
  format: "JSON"
```

O YAML informa ao Python os parâmetros da fonte.

A lógica de execução permanece no código Python.

Evitar colocar nomes de funções Python ou lógica complexa dentro do YAML.

Exemplo a evitar:

```yaml
function: extrair_ibge_demografia
```

A configuração deve indicar características da fonte, não acoplar o YAML a uma implementação específica.

---

# 8. `extractor.py`

`extractor.py` é responsável somente por obter os dados externos.

O número de funções deve acompanhar os **mecanismos de extração**, e não a quantidade de fontes.

Exemplo:

```text
5 YAMLs IBGE
↓
1 mecanismo API

1 YAML INMET
↓
1 mecanismo ZIP

2 YAMLs RS
↓
1 mecanismo PDF
```

Portanto, a implementação atual pode possuir:

```python
extrair_api(config)
extrair_zip(config)
extrair_pdf(config)
extrair(config)
```

A função principal pode realizar dispatch simples:

```python
if tipo/formato corresponde a API:
    ...
elif corresponde a ZIP:
    ...
elif corresponde a PDF:
    ...
else:
    ...
```

Não criar:

```python
extrair_ibge_demografia()
extrair_ibge_habitacao()
extrair_ibge_esgotamento()
extrair_decreto_rs()
extrair_coletiva_rs()
```

quando essas fontes compartilham o mesmo mecanismo.

---

# 9. Retorno do extractor

O extractor deve fornecer uma estrutura simples para as etapas seguintes.

Como uma configuração pode produzir um ou vários arquivos, o retorno pode ser normalizado como lista.

Exemplo:

```python
[
    {
        "content": bytes,
        "filename": "...",
        "source_url": "...",
        "resource_id": None
    }
]
```

Não criar classes ou models apenas para representar essa estrutura enquanto um `dict` for suficiente.

---

# 10. Preservação do dado bruto

Os bytes recebidos da fonte devem ser preservados.

Na Bronze, não:

* converter JSON para CSV;
* converter arquivos para Parquet;
* abrir PDFs para tratamento analítico;
* modificar campos;
* preencher valores ausentes;
* alterar unidades;
* normalizar nomes;
* filtrar conteúdo apenas por conveniência analítica.

Se uma fonte disponibiliza um ZIP, preservar o ZIP original quando essa for a decisão definida no Prompt Inicial.

Transformações pertencem à Silver.

---

# 11. `metadata.py`

O manifest deve reutilizar a configuração existente.

Princípio:

```text
YAML original
+
informações geradas durante a execução
=
manifest
```

Não duplicar manualmente no código metadata já existente no YAML.

A implementação deve copiar a configuração original e adicionar metadata dinâmica da ingestão.

Exemplos:

```text
retrieved_at
filename
source_url
size_bytes
sha256
s3_key
```

O checksum deve ser calculado a partir dos bytes efetivamente obtidos.

Não modificar o objeto de configuração original.

O resultado deve ser serializável em JSON.

---

# 12. Manifest

O YAML descreve:

> qual é a fonte e como ela está configurada.

O manifest registra:

> o que efetivamente aconteceu naquela ingestão.

Portanto:

```text
configuração
= informação conhecida antes da execução

manifest
= configuração + resultado concreto da execução
```

---

# 13. `aws.py`

`aws.py` é responsável pela persistência no S3 usando `boto3`.

As credenciais e configurações AWS devem vir do ambiente existente.

Nunca colocar credenciais diretamente no código.

Nunca versionar:

* AWS Access Key;
* AWS Secret Access Key;
* AWS Session Token;
* outros secrets.

O módulo pode:

* criar sessão/cliente necessário;
* identificar o bucket configurado;
* enviar arquivo bruto;
* enviar manifest;
* retornar a chave S3 utilizada.

Não criar abstração de storage genérica enquanto somente S3 for uma necessidade real do projeto.

Não criar `LocalStorage`, `StorageInterface` ou equivalentes apenas por possibilidade futura.

---

# 14. Organização das chaves S3

Usar uma estrutura simples e previsível.

Priorizar identificação por:

```text
source.id
+
nome original do arquivo
```

Evitar estruturas excessivamente profundas ou particionamentos não necessários para a Bronze atual.

Se já existir uma convenção válida documentada no projeto, preservá-la.

---

# 15. Logging

Usar `logging` padrão do Python.

Não criar infraestrutura própria de logging sem necessidade.

O logging deve permitir acompanhar eventos importantes, como:

```text
🚀 início
⚙️ configuração carregada
🌐 requisição
📥 download concluído
🧾 manifest criado
☁️ upload S3
⚠️ warning
❌ erro
✅ sucesso
🏁 fim
```

Os emojis são opcionais e servem apenas para facilitar leitura visual.

Não registrar:

* conteúdo completo dos arquivos;
* credenciais;
* tokens;
* conteúdo do `.env`;
* headers de autenticação.

Logs devem informar contexto útil, como:

```text
source
file
url
size
destination
```

Sem tornar a implementação excessivamente complexa.

---

# 16. Erros

Não esconder exceções.

Evitar:

```python
except Exception:
    pass
```

Quando uma falha ocorrer:

* registrar contexto suficiente;
* preservar o erro original;
* interromper ou continuar conforme definido no Prompt Inicial.

Mensagens de erro de configuração devem identificar, quando possível:

```text
source.id
access.type
access.format
```

---

# 17. Retry

Retry só deve existir quando houver necessidade concreta.

Se implementado:

* usar limite explícito;
* evitar loops infinitos;
* registrar as tentativas;
* preservar o erro final quando todas falharem.

Não adicionar bibliotecas ou mecanismos sofisticados apenas para retry simples.

---

# 18. Dependências

Adicionar somente bibliotecas realmente utilizadas.

Para a implementação atual, exemplos possíveis são:

```text
PyYAML
requests
boto3
python-dotenv
```

Não adicionar automaticamente:

* pandas;
* awswrangler;
* pandera;
* Spark;
* Airflow;
* bibliotecas de framework;

quando não forem necessárias para a tarefa atual.

---

# 19. OOP

O uso de orientação a objetos não é obrigatório.

Funções são preferíveis quando:

* não existe estado relevante compartilhado;
* o fluxo permanece claro;
* o código fica mais fácil de entender e testar.

Criar classe somente quando houver benefício concreto.

Não criar classes apenas para tornar o código aparentemente mais arquitetado.

---

# 20. Evolução de novas fontes

Quando uma nova fonte for adicionada:

```text
1. verificar se utiliza um mecanismo de extração existente
2. tentar resolver diferenças por configuração
3. se necessário, adicionar comportamento genérico reutilizável
4. somente em último caso criar lógica específica da fonte
```

Quantidade de fontes não determina quantidade de funções.

Exemplo:

```text
8 YAMLs
≠
8 extractors
```

---

# 21. Testes e validação

Testes devem acompanhar a complexidade real do código.

Sempre que possível:

* testar parsing dos YAMLs sem internet;
* testar dispatch do extractor;
* testar metadata e checksum isoladamente;
* mockar chamadas HTTP e AWS quando apropriado.

Não executar downloads grandes ou integrações reais sem que o Prompt Inicial determine isso.

Especialmente em arquivos grandes, evitar consumo de rede desnecessário apenas para provar que o código compila.

---

# 22. Documentação

Não atualizar documentação automaticamente apenas porque código foi alterado.

O Prompt Inicial define quais documentos devem ser modificados.

`STATUS.md` deve refletir somente o que foi realmente implementado e validado.

Não marcar uma ingestão como concluída quando:

* existe apenas código;
* ainda não houve validação necessária;
* a execução falhou;
* depende de recurso externo ainda indisponível.

---

# 23. Escopo

O agente deve executar somente o trabalho autorizado no Prompt Inicial.

Não avançar automaticamente para:

* novas fontes;
* ANA;
* S2ID;
* logística;
* Silver;
* Gold;
* Machine Learning;
* app;
* novas abstrações arquiteturais.

Se uma necessidade fora do escopo for descoberta, informar ao final sem implementá-la automaticamente.

---

# 24. Regra final

Na Bronze, o modelo mental principal é:

```text
YAML
↓
config_loader
↓
dict Python
↓
extractor
↓
bytes originais
↓
metadata / manifest
↓
AWS S3
↓
próxima configuração
```

O código deve permanecer:

* simples;
* legível;
* rastreável;
* modular na medida necessária;
* fácil de testar;
* fácil de explicar.

A prioridade é uma ingestão funcional e compreensível.

Não transformar um fluxo simples em uma arquitetura complexa sem uma necessidade real.
