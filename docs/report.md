# Análise de Code Reviews de Repositórios Populares de Código Aberto no GitHub

## 1. Introdução

Neste trabalho, realizamos uma análise da atividade de code review desenvolvida em repositórios populares do GitHub. O objetivo principal é identificar variáveis que influenciam no merge de um Pull Request (PR) submetido nesses repositórios. Para isso, utilizamos um conjunto de PRs de repositórios populares do GitHub, filtrados por critérios específicos, a fim de responder às seguintes questões de pesquisa:

- **RQ 01**: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
- **RQ 02**: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
- **RQ 03**: Qual a relação entre a descrição dos PRs e o feedback final das revisões?
- **RQ 04**: Qual a relação entre as interações nos PRs e o feedback final das revisões?
- **RQ 05**: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
- **RQ 06**: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
- **RQ 07**: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
- **RQ 08**: Qual a relação entre as interações nos PRs e o número de revisões realizadas?


## 2. Hipóteses Informais

Com base nas características dos repositórios populares analisados, foram formuladas, de forma preliminar, as seguintes hipóteses, que serão validadas ao longo do estudo:

- Espera-se que PRs com menor quantidade de arquivos e linhas alteradas tenham maior probabilidade de serem aceitos
- Espera-se que PRs analisados por mais tempo tendam a ter maior chance de rejeição
- Espera-se que PRs com descrições detalhadas apresentem feedback mais positivo por tornarem mais claro o entendimento da mudança
- Espera-se que PRs com maior número de interações tenham maior probabilidade de serem aceitos em função do processo colaborativo de revisão
- Espera-se que PRs com maior quantidade de arquivos e linhas alteradas necessitem de um número maior de revisões
- Espera-se que PRs analisados por mais tempo tendam a passar por mais revisões antes de uma decisão final
- Espera-se que PRs com descrições mais detalhadas apresentem menor o número de revisões por tornarem mais claro o entendimento da mudança e reduzirem necessidade de análises subsequentes
- Espera-se que PRs com maior número de interações apresentem maior número de, já que discussões extensas frequentemente resultam em ajustes e revisões adicionais


## 3. Metodologia

### 3.1. Criação do Dataset

A coleta de dados foi realizada a partir da API do GitHub e implementada via GraphQL, buscando os 200 repositórios com maior número de estrelas, filtrados a partir dos seguintes critérios de seleção:

- Repositórios com pelo menos 100 PRs (mergeados ou fechados).
- PRs com status de `MERGED` ou `CLOSED`, que passaram por pelo menos uma revisão (campo `review` com valor maior que zero).
- PRs cuja revisão tenha levado mais de uma hora, eliminando assim revisões automáticas (como bots ou ferramentas de CI/CD).

### 3.2. Definição de Métricas

Para cada pergunta de pesquisa, utilizamos as seguintes métricas para avaliar as correlações:

- **Tamanho do PR**: número de arquivos modificados e total de linhas adicionadas e removidas
- **Tempo de Análise**: intervalo de tempo entre a criação do PR e sua última atividade (merge ou fechamento)
- **Descrição**: número de caracteres no 'body' da descrição do PR (em markdown)
- **Interações**: número de participantes no PR e o número de comentários feitos

## 4. Resultados
## 5. Análise de resultados