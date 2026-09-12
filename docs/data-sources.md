# Inventário de fontes e template de Data Contract

Nenhum dataset foi escolhido. Isso evita apresentar uma fonte não verificada como aprovada. Preencha uma entrada por candidato e registre a justificativa antes da ingestão Bronze.

## Inventário de candidatos

| ID | Dataset | Publicador | Finalidade | Geografia / granularidade | Cobertura temporal | Licença | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A definir | A pesquisar | — | Impacto, demografia, vulnerabilidade, infraestrutura, acesso, recursos ou geografia oficial | — | — | Deve ser verificada | Candidato |

## Critérios de seleção

1. relevância para um cenário histórico de desastre climático;
2. publicador confiável e URL estável;
3. licença ou termos explícitos;
4. cobertura geográfica e temporal suficiente;
5. granularidade, metodologia e unidades documentadas;
6. identificadores oficiais de município para joins;
7. histórico de atualização/revisão e reprodução da obtenção;
8. adequação ética e de privacidade;
9. limitações de missingness, bias, subnotificação e comparabilidade;
10. viabilidade no prazo da v0.1.

## Template do contrato

### Identidade e governança

- **Dataset ID e versão do contrato:**
- **Título:**
- **Publicador / data owner:**
- **Landing page oficial e URL de download:**
- **Licença / URL dos termos e uso permitido:**
- **Contato / documentação:**
- **Obtido em (UTC):**
- **Cadência e política de revisão:**
- **Finalidade / fatores suportados:**
- **Estado de aprovação e responsável pela revisão:**

### Forma e semântica

- **Formato e encoding:**
- **Padrão esperado do nome do arquivo:**
- **Granularidade (uma linha por...):**
- **Primary/candidate key:**
- **Foreign/reference keys:**
- **Nível geográfico e versão do padrão de códigos:**
- **Semântica temporal do evento e observação:**
- **Time zone:**
- **Cobertura geográfica e temporal:**
- **Unidades e definições de categorias:**

| Coluna | Tipo na fonte | Aceita nulo? | Unidade/domínio | Significado | Exemplo não sensível |
| --- | --- | --- | --- | --- | --- |
| A definir | — | — | — | — | — |

### Expectativas de qualidade

- **Colunas obrigatórias:**
- **Expectativa de unicidade:**
- **Ranges/domínios válidos:**
- **Regras entre colunas:**
- **Referências e versões:**
- **Expectativas temporais/freshness:**
- **Mudanças de schema permitidas:**
- **Ação quando o contrato falhar:**

### Limitações, ética e bias

- **Limitações declaradas pelo publicador:**
- **Método de coleta e possível subnotificação:**
- **Populações/geografias possivelmente sub-representadas:**
- **Privacidade ou atributos sensíveis:**
- **Riscos no uso para priorização:**
- **Mitigação e ressalvas obrigatórias na interface:**

### Evidências Bronze

- **S3 URI e versão do objeto:**
- **Nome original e tamanho em bytes:**
- **SHA-256 checksum:**
- **URI do manifest / referência no repositório:**
- **Responsável e horário da ingestão (UTC):**
- **Resultado da verificação:**

## Questões de pesquisa abertas

- Qual desastre histórico e recorte geográfico formam um caso crível e viável?
- Qual versão da referência e dos limites municipais corresponde aos dados?
- Os indicadores foram observados em períodos compatíveis?
- As licenças permitem armazenamento, transformação, screenshots e demonstração pública?

Essas questões são o próximo marco e não bloqueiam a fundação.
