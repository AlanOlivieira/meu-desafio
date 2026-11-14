# Registro dos experimentos

Este registro reúne os experimentos realizados entre 10 e 12 de novembro de 2026, com as medições e as evidências de cada mudança.

Os números deste documento vêm dos arquivos originais de `resultados/` ou, quando indicado, dos diagnósticos salvos em `diagnostico/`. Os arquivos gerados pela régua foram preservados. As medianas selecionam o valor central das execuções de cada grupo e preservam a precisão dos resumos.

## Procedimento e rastreabilidade

- E0 - linha de base: commit medido `306ae69`; resultados registrados em `0ae6008`.
- E1 - índice dos itens por pedido: implementação em `e5d3100`; commit medido `1ff3416`; resultados registrados em `393f3a8`.
- E2 - índice dos pedidos por cliente, mantendo E1. A implementação está em `048a6f3`. As primeiras três execuções registram `2110249` e estão em `d7a5443`. As duas repetições registram `d7a5443` e estão em `4cc5949`. A conferência do Git confirmou a equivalência dos arquivos executados entre os dois commits medidos.
- As três execuções da referência na tomada mediram o commit `d5794bb`, que reverteu a inclusão do segundo índice. Os resultados estão em `a02e219`.
- E3 adicionou o pool à configuração da referência na tomada. O commit medido `1ef1f09` modificou apenas `api/src/db.js`. O commit `b6f7362` registra os resultados das três rodadas.
- E4 adicionou o índice de pedidos por status em `4cdcb88`. Os planos antes e depois estão em `cf791cb` e `011bbd7`, respectivamente. As três rodadas mediram `011bbd7` e estão registradas em `ba8cb51`.
- E5 reescreveu a consulta do ranking em `c0b4c97`. Os planos antes e depois estão em `e662107` e `ef4bb01`, respectivamente. As três rodadas mediram `ef4bb01` e estão registradas em `c7829ed`.
- E6 adicionou o índice da data do pedido em `27f5bae`. Os planos antes e depois estão em `4bf7284` e `5c692fc`, respectivamente. As três rodadas mediram `5c692fc` e estão registradas em `6c4b1c8`.
- E7 introduziu a busca em lote em `fc49dd2`. O diagnóstico do cliente 42 está em `e4f9aa0`. As três rodadas mediram `fc49dd2` e estão registradas em `9702a6a`.
- A validação de 20 usuários virtuais mediu `306ae69` e `5c692fc` em três pares alternados. O commit `e0fb6c5` contém os 36 arquivos das seis rodadas.
- A validação de 5 usuários virtuais mediu os mesmos commits em três pares alternados. Os 36 arquivos das seis rodadas estão em `a32a5d1`.
- A validação de 40 usuários virtuais mediu os mesmos commits em três pares alternados. Os 36 arquivos das seis rodadas estão em `e88764c`.
- As rodadas usaram `DURACAO=60s`, `AQUECIMENTO=15s` e `SEMENTE=42`. A concorrência foi de 20 usuários virtuais nos experimentos E0 a E7 e na validação principal, de 5 no cenário de menor concorrência e de 40 no de maior concorrência.
- Todos os arquivos `contexto.txt` registram `arquivos alterados sem commit: 0`.
- Os limites permaneceram iguais: banco com `1` CPU e `536870912` bytes de memória; API com `0.5` CPU e `268435456` bytes de memória.
- Todos os arquivos `contrato.txt` confirmam as mesmas `42` respostas do contrato original.
- A conferência dos ZIPs confirmou a preservação das medições anteriores, do contrato, dos scripts, da carga e dos SQLs originais. A reversão retirou `banco/04-indice-pedidos-cliente.sql` da referência na tomada, que voltou à configuração de E1. O ZIP de E3 preserva o conteúdo dos arquivos anteriores, com a alteração em `api/src/db.js`. A comparação dos ZIPs de E3 e E4 confirmou a preservação byte a byte dos 130 arquivos de projeto e evidência anteriores. A comparação entre E4 e E5 encontrou a alteração prevista em `api/src/rotas.js` e preservação byte a byte dos demais arquivos anteriores. A comparação de E5 com E6 confirmou a preservação byte a byte dos 171 arquivos anteriores de código e evidência. Na comparação entre E6 e E7, dos 192 arquivos anteriores, a alteração de conteúdo foi em `api/src/rotas.js`.
- E1 acrescentou somente `banco/03-indice-itens-pedido.sql` à configuração de desempenho. E2 acrescentou somente `banco/04-indice-pedidos-cliente.sql` a E1. Os demais acréscimos foram evidências de diagnóstico e medição.
- A comparação entre o ZIP de E7 e o da validação confirmou a integridade dos 211 arquivos anteriores de projeto e evidência. Os seis diretórios novos foram conferidos com o conteúdo de `e0fb6c5`.
- O ZIP da validação de 5 usuários virtuais preservou os 247 arquivos de projeto e evidência do ZIP de 20. Os seis diretórios novos foram conferidos com o conteúdo de `a32a5d1`.
- O ZIP da validação de 40 usuários virtuais preservou os 283 arquivos de projeto e evidência do ZIP de 5. Os seis diretórios novos foram conferidos com o conteúdo de `e88764c`.

A adaptação da porta externa do banco para `5433` ocorreu antes de E0, no commit `605e972`.

As rodadas P1 a P3 foram executadas com o notebook na bateria, e P4 e P5, na tomada. Durante as repetições, havia mais abas abertas no Chrome e o Explorador de Arquivos estava aberto. Essas observações foram registradas manualmente. A coleta de recursos acompanhou os contêineres do desafio. A condição de energia de E0 e E1 é desconhecida.

## Quadro dos experimentos

| Experimento e fonte | Situação | Antes | Depois | Evidências | Conclusão |
| --- | --- | --- | --- | --- | --- |
| E0 - aplicação original; procedimento do README | Medido, três execuções | Referência inicial | p95 geral `49653.4 ms`; `1.40 req/s` | B1, B2, B3 | Base para comparar as mudanças |
| E1 - índice B-tree em `(pedido_id, id)`; planos SQL e documentação PostgreSQL [1][2][3] | Aplicado e medido, três execuções | E0: p95 `49653.4 ms`; `1.40 req/s`; mediana da latência `3040.9 ms` | E1: p95 `32673.9 ms`; `1.71 req/s`; mediana da latência `3927.1 ms` | I1, I2, I3; D1, D3 e D4; SQL novo | Evidência favorável para p95 e taxa de requisições, com piora da mediana da latência e maior uso de recursos da API |
| E2 - índice dos pedidos por cliente e ordenação, fundamentado nos planos D5 e D6 e na documentação [2][3] | Aplicado e medido em cinco execuções com variação de ambiente | E1 com p95 `32673.9 ms`, `1.71 req/s` e mediana da latência `3927.1 ms` | E2 com p95 `30711.9 ms`, `1.58 req/s` e mediana da latência `4839.0 ms` | P1 a P5, D5 a D7 e SQL do segundo índice | Ganho na consulta isolada. Efeito incremental na API inconclusivo diante da dispersão e da mudança de ambiente |
| Referência na tomada com o índice dos itens | Medida em três execuções com o segundo índice revertido | Configuração de E1 | p95 `23346.4 ms`, `2.74 req/s` e mediana da latência `2398.5 ms` | Tomada 1 a 3 | Referência para medir o efeito do pool |
| E3 - pool de conexões com PostgreSQL [6] | Aplicado e medido em três execuções | Referência na tomada com p95 `23346.4 ms` e `2.74 req/s` | E3 com p95 `24357.9 ms` e `2.83 req/s` | Pool 1 a 3 e implementação em `1ef1f09` | Latência mediana menor, p95 maior e aumento de memória média da API |
| E4 - índice B-tree para pedidos por status e ordenação [2][3][7] | Aplicado e medido em três execuções | E3 com `2.83 req/s`, p50 `2095.5 ms` e p95 `24357.9 ms` | E4 com `3.61 req/s`, p50 `1574.2 ms` e p95 `26459.7 ms` | Status 1 a 3, D8, D9 e `4cdcb88` | Maior vazão e p50 menor. O p95 geral e o uso médio de CPU e memória subiram. |
| E5 - ranking com agregação e limite antes da junção com produtos [1][4][8] | Aplicado e medido em três execuções | E4 com `3.61 req/s`, p50 `1574.2 ms` e p95 `26459.7 ms` | E5 com `4.31 req/s`, p50 `1687.9 ms` e p95 `17109.9 ms` | Ranking 1 a 3, D10, D11 e `c0b4c97` | Maior vazão e p95 menor, com `0.00%` de erros nas três rodadas e p50 geral maior. |
| E6 - índice parcial na expressão `criado_em::date` [9][10] | Aplicado e medido em três execuções | E5 com `4.31 req/s`, p50 `1687.9 ms` e p95 `17109.9 ms` | E6 com `6.53 req/s`, p50 `1297.2 ms` e p95 `10458.9 ms` | Diário 1 a 3, D12, D13 e `27f5bae` | Vazão maior, p50 e p95 menores e `0.00%` de erros nas três rodadas. |
| E7 - busca em lote de itens e produtos [11][12][13] | Aplicado e medido em três execuções | E6 com `6.53 req/s`, p50 `1297.2 ms` e p95 `10458.9 ms` | E7 com `5.19 req/s`, p50 `1588.9 ms` e p95 `13337.7 ms` | Lote 1 a 3, D14 e `fc49dd2` | Menor vazão e maior latência na série medida. O contrato passou nas três rodadas. |
| Validação de 20 usuários virtuais | Medida em três rodadas por versão | Original com `1.36 req/s`, p50 `2375.6 ms` e p95 `50900.5 ms` | Otimizada com `7.32 req/s`, p50 `1628.0 ms` e p95 `8325.2 ms` | Seis rodadas em `e0fb6c5` | Maior vazão e menor p95 nas três rodadas otimizadas sob as mesmas cotas, com maior uso médio de memória e CPU da API. |
| Validação de 5 usuários virtuais | Medida em três rodadas por versão | Original com `0.92 req/s`, p50 `1693.7 ms` e p95 `16215.6 ms` | Otimizada com `4.20 req/s`, p50 `911.2 ms` e p95 `2832.6 ms` | Seis rodadas em `a32a5d1` | Maior vazão e menor p95 nas três rodadas otimizadas sob as mesmas cotas. Zero falhas nas duas versões. |
| Validação de 40 usuários virtuais | Medida em três rodadas por versão | Original com `1.38 req/s`, p95 `59986.4 ms` e `25.00%` de erros | Otimizada com `4.75 req/s`, p95 `26060.0 ms` e `0.00%` de erros | Seis rodadas em `e88764c` | Maior vazão e menor p95 nas três rodadas otimizadas. A original teve 85 falhas durante a carga e a otimizada teve zero. |

O p95 exibido é a mediana dos p95 por execução. As medianas de E2 descrevem o conjunto de condições observadas.

## Execuções e resultados gerais

| ID | Arquivo de origem | Requisições/s | Mediana da latência (ms) | p95 geral (ms) | Erros |
| --- | --- | ---: | ---: | ---: | ---: |
| B1 | [20261110-171634-00-linha-de-base/resumo.txt](resultados/20261110-171634-00-linha-de-base/resumo.txt) | 1.14 | 2791.5 | 50746.3 | 1.94% |
| B2 | [20261110-172205-00-linha-de-base/resumo.txt](resultados/20261110-172205-00-linha-de-base/resumo.txt) | 1.40 | 3040.9 | 49653.4 | 0.87% |
| B3 | [20261110-172503-00-linha-de-base/resumo.txt](resultados/20261110-172503-00-linha-de-base/resumo.txt) | 1.41 | 3436.9 | 48584.5 | 0.00% |
| I1 | [20261110-212550-01-indice-itens-pedido/resumo.txt](resultados/20261110-212550-01-indice-itens-pedido/resumo.txt) | 1.71 | 3927.1 | 35581.4 | 0.00% |
| I2 | [20261110-212821-01-indice-itens-pedido/resumo.txt](resultados/20261110-212821-01-indice-itens-pedido/resumo.txt) | 1.71 | 3597.4 | 31716.6 | 0.79% |
| I3 | [20261110-213056-01-indice-itens-pedido/resumo.txt](resultados/20261110-213056-01-indice-itens-pedido/resumo.txt) | 1.77 | 4347.9 | 32673.9 | 0.00% |
| P1 | [20261110-224519-02-indice-pedidos-cliente/resumo.txt](resultados/20261110-224519-02-indice-pedidos-cliente/resumo.txt) | 1.52 | 5753.0 | 33184.1 | 0.00% |
| P2 | [20261110-224821-02-indice-pedidos-cliente/resumo.txt](resultados/20261110-224821-02-indice-pedidos-cliente/resumo.txt) | 1.34 | 6681.5 | 36654.5 | 0.90% |
| P3 | [20261110-225102-02-indice-pedidos-cliente/resumo.txt](resultados/20261110-225102-02-indice-pedidos-cliente/resumo.txt) | 3.05 | 2202.0 | 19324.3 | 0.00% |
| P4 | [20261110-230602-02-indice-pedidos-cliente/resumo.txt](resultados/20261110-230602-02-indice-pedidos-cliente/resumo.txt) | 2.60 | 2409.8 | 20653.7 | 0.00% |
| P5 | [20261110-231346-02-indice-pedidos-cliente/resumo.txt](resultados/20261110-231346-02-indice-pedidos-cliente/resumo.txt) | 1.58 | 4839.0 | 30711.9 | 0.78% |
| Tomada 1 | [20261111-001913-01-indice-itens-tomada/resumo.txt](resultados/20261111-001913-01-indice-itens-tomada/resumo.txt) | 2.74 | 2292.7 | 23346.4 | 0.00% |
| Tomada 2 | [20261111-002136-01-indice-itens-tomada/resumo.txt](resultados/20261111-002136-01-indice-itens-tomada/resumo.txt) | 2.81 | 2403.2 | 20155.1 | 0.00% |
| Tomada 3 | [20261111-002341-01-indice-itens-tomada/resumo.txt](resultados/20261111-002341-01-indice-itens-tomada/resumo.txt) | 2.44 | 2398.5 | 24549.0 | 0.52% |
| Pool 1 | [20261111-004437-03-pool-conexoes/resumo.txt](resultados/20261111-004437-03-pool-conexoes/resumo.txt) | 2.61 | 2295.5 | 26482.8 | 0.00% |
| Pool 2 | [20261111-004657-03-pool-conexoes/resumo.txt](resultados/20261111-004657-03-pool-conexoes/resumo.txt) | 2.97 | 2006.4 | 24357.9 | 0.44% |
| Pool 3 | [20261111-004903-03-pool-conexoes/resumo.txt](resultados/20261111-004903-03-pool-conexoes/resumo.txt) | 2.83 | 2095.5 | 20975.1 | 0.00% |
| Status 1 | [20261111-011109-04-indice-pedidos-status/resumo.txt](resultados/20261111-011109-04-indice-pedidos-status/resumo.txt) | 3.45 | 1574.2 | 26781.7 | 0.40% |
| Status 2 | [20261111-011349-04-indice-pedidos-status/resumo.txt](resultados/20261111-011349-04-indice-pedidos-status/resumo.txt) | 4.30 | 1287.6 | 20837.0 | 0.00% |
| Status 3 | [20261111-011611-04-indice-pedidos-status/resumo.txt](resultados/20261111-011611-04-indice-pedidos-status/resumo.txt) | 3.61 | 1845.1 | 26459.7 | 0.38% |
| Ranking 1 | [20261111-015733-05-ranking-produtos/resumo.txt](resultados/20261111-015733-05-ranking-produtos/resumo.txt) | 4.31 | 1582.3 | 15175.5 | 0.00% |
| Ranking 2 | [20261111-015941-05-ranking-produtos/resumo.txt](resultados/20261111-015941-05-ranking-produtos/resumo.txt) | 4.54 | 1687.9 | 17913.5 | 0.00% |
| Ranking 3 | [20261111-020132-05-ranking-produtos/resumo.txt](resultados/20261111-020132-05-ranking-produtos/resumo.txt) | 4.13 | 1802.0 | 17109.9 | 0.00% |
| Diário 1 | [20261111-023355-06-indice-vendas-por-dia/resumo.txt](resultados/20261111-023355-06-indice-vendas-por-dia/resumo.txt) | 5.24 | 1392.3 | 15704.2 | 0.00% |
| Diário 2 | [20261111-023539-06-indice-vendas-por-dia/resumo.txt](resultados/20261111-023539-06-indice-vendas-por-dia/resumo.txt) | 6.80 | 1297.2 | 10458.9 | 0.00% |
| Diário 3 | [20261111-023720-06-indice-vendas-por-dia/resumo.txt](resultados/20261111-023720-06-indice-vendas-por-dia/resumo.txt) | 6.53 | 1113.0 | 10245.0 | 0.00% |
| Lote 1 | [20261111-191505-07-pedidos-em-lote/resumo.txt](resultados/20261111-191505-07-pedidos-em-lote/resumo.txt) | 5.53 | 1588.9 | 13315.8 | 0.00% |
| Lote 2 | [20261111-191750-07-pedidos-em-lote/resumo.txt](resultados/20261111-191750-07-pedidos-em-lote/resumo.txt) | 5.16 | 1399.1 | 13803.5 | 0.00% |
| Lote 3 | [20261111-192052-07-pedidos-em-lote/resumo.txt](resultados/20261111-192052-07-pedidos-em-lote/resumo.txt) | 5.19 | 1642.3 | 13337.7 | 0.00% |

Nas execuções observadas, o p95 de E1 foi menor que os p95 de E0, e suas taxas foram maiores. Isso sustenta um resultado favorável nessa carga, sem estabelecer significância estatística ou garantia para outro ambiente. A mediana da latência aumentou nas execuções de E1.

As medianas das taxas de erros foram `0.87%` em E0, `0.00%` em E1, E2, na referência na tomada, em E3, E5, E6 e E7, e `0.38%` em E4. I2 registrou `0.79%` de erros, P2 registrou `0.90%` e P5 registrou `0.78%`. Tomada 3 registrou `0.52%` e Pool 2 registrou `0.44%`, ambos com uma falha em `/relatorios/top-produtos`. Em E4, Status 1 e Status 3 registraram `0.40%` e `0.38%` de erros gerais, respectivamente, com uma falha nessa mesma rota em cada rodada. De E5 a E7, todas as rodadas registraram `0.00%` de erros gerais. As checagens de contrato após a carga passaram nesses testes. O resultado geral é a referência porque algumas rotas tiveram poucas requisições.

A dispersão persistiu nas repetições na tomada. P4 registrou `2.60 req/s` e P5 registrou `1.58 req/s`. A série anterior na bateria inclui P3, com `3.05 req/s`. A causa das diferenças segue indeterminada, pois os testes foram executados em blocos e o ambiente mudou entre os lotes.

Na comparação acumulada com E0, E2 apresentou p95 mediano menor e taxa mediana maior, acompanhados de aumento da mediana da latência. Entre E1 e E2, o p95 mediano caiu e a vazão mediana também caiu. A comparação incremental é descritiva e sensível às condições de execução.

## Recursos e custo

As colunas usam as medianas dos valores de `recursos.txt` em cada grupo. Para CPU e memória média, o valor central vem das médias de cada execução. Para memória máxima, vem dos máximos por execução.

| Indicador | E0 | E1 | E2, cinco execuções | Referência na tomada | E3, pool | E4, índice por status | E5, ranking | E6, índice por dia | E7, busca em lote |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CPU média do banco | 99.9% | 98.7% | 97.1% | 94.4% | 95.1% | 98.4% | 98.9% | 99.8% | 100.5% |
| CPU média da API | 7.7% | 14.9% | 14.0% | 12.9% | 12.1% | 17.0% | 18.6% | 20.0% | 18.7% |
| Memória média do banco | 402.5 MiB | 394.9 MiB | 393.7 MiB | 387.4 MiB | 392.4 MiB | 413.2 MiB | 425.5 MiB | 427.7 MiB | 422.7 MiB |
| Memória média da API | 28.6 MiB | 33.3 MiB | 35.2 MiB | 39.5 MiB | 43.7 MiB | 52.4 MiB | 51.4 MiB | 48.7 MiB | 47.6 MiB |
| Memória máxima do banco | 447.1 MiB | 448.7 MiB | 448.2 MiB | 436.3 MiB | 433.4 MiB | 457.6 MiB | 458.4 MiB | 465.1 MiB | 468.9 MiB |
| Memória máxima da API | 37.1 MiB | 50.4 MiB | 49.6 MiB | 48.2 MiB | 67.2 MiB | 76.2 MiB | 71.8 MiB | 76.7 MiB | 75.2 MiB |

Os arquivos `recursos.txt`, `recursos.csv`, `contexto.txt` e `contrato.txt` ficam ao lado de cada `resumo.txt` indicado na tabela anterior.

O índice acrescentou **33718272 bytes** de armazenamento, conforme [D4](diagnostico/04-custo-indice-itens.txt). O PostgreSQL exibiu esse valor também como `32 MB`, usando sua função de apresentação de tamanho. As cotas de CPU e memória não aumentaram, mas o uso observado da API aumentou. Portanto, o resultado não comprova redução geral de recursos nem economia financeira. O custo de manter o índice em escritas futuras não foi medido.

E2 acrescentou **20299776 bytes** de armazenamento em relação a E1. O diagnóstico confirma os dois índices na versão medida de E2 e exibe `19 MB` para o segundo índice. [D7](diagnostico/07-custo-indices-02.txt)

O índice de E4 acrescentou **22118400 bytes** de armazenamento, exibidos como `21 MB` pelo PostgreSQL. A CPU média e a memória média reportadas aumentaram nos dois contêineres na comparação com E3, sob as mesmas cotas. O custo do índice em escritas segue como questão para outro ensaio. [D9](diagnostico/09-pedidos-status-depois.txt)

O índice de E6 acrescentou **3252224 bytes** de armazenamento, exibidos como `3176 kB` pelo PostgreSQL. Na comparação com E5, subiram a CPU média dos dois contêineres e a memória média do banco. A memória média da API caiu. [D13](diagnostico/13-vendas-por-dia-depois.txt)

O resumo de recursos pode calcular `cpu_max` com comparação textual no trecho `awk`. De E3 a E7, o máximo reportado da API ficou abaixo da própria média nas três rodadas de cada série. Em duas rodadas de E7, a CPU média reportada do banco passou de 100% com cota nominal de 1 CPU. A análise de CPU usa `cpu_media` e considera a variação entre amostras. Os CSVs podem ter uma amostra adicional em relação aos resumos. A régua e os dados originais foram preservados.

## Diagnóstico e interpretação de E1

- [D1 — consulta dos itens antes](diagnostico/01-itens-pedido-antes.txt): `Parallel Seq Scan`, seguido de ordenação; `Execution Time: 5030.303 ms`.
- [D2 — pedidos por cliente antes de E1](diagnostico/02-pedidos-cliente-antes.txt): `Parallel Seq Scan` e ordenação; `Execution Time: 2902.750 ms`.
- [D3 — consulta dos itens depois](diagnostico/03-itens-pedido-depois.txt): `Index Scan using idx_itens_pedido_pedido_id_id`; `Execution Time: 0.877 ms`.
- [D4 — tamanho do índice](diagnostico/04-custo-indice-itens.txt): `33718272 bytes`.
- [Implementação de E1](banco/03-indice-itens-pedido.sql): índice em `itens_pedido (pedido_id, id)`.

Os planos D1 e D3 devolvem os mesmos `3` itens no diagnóstico com `pedido_id = 7`. A mudança de acesso é compatível com a hipótese: a consulta passou a localizar o pedido pelo índice e o plano deixou de mostrar a varredura e a ordenação anteriores. Esses tempos são observações de uma consulta isolada, com condições de cache e concorrência distintas do teste HTTP. O ganho da API é descrito pelos resultados I1–I3, sem extrapolar a diferença entre os tempos SQL.

A explicação técnica é apoiada pela documentação: chaves estrangeiras não criam automaticamente índices nas colunas de referência; as colunas iniciais importam no B-tree composto; e um índice adequado pode fornecer a ordenação solicitada [1][2][3].

## Diagnóstico e interpretação de E2

- [D5 — pedidos do cliente, com o primeiro índice](diagnostico/05-pedidos-cliente-antes-02.txt): `Parallel Seq Scan` com filtro por `cliente_id` e ordenação; `Execution Time: 4628.172 ms`.
- [D6 — pedidos do cliente, com os dois índices](diagnostico/06-pedidos-cliente-depois-02.txt): `Index Scan using idx_pedidos_cliente_criado_id`; `Execution Time: 2.199 ms`.
- [D7 — tamanho dos dois índices](diagnostico/07-custo-indices-02.txt): `33718272 bytes` para itens por pedido e `20299776 bytes` para pedidos por cliente.
- O índice em `pedidos (cliente_id, criado_em DESC, id DESC)` está disponível no histórico pelo comando `git show 048a6f3:banco/04-indice-pedidos-cliente.sql`.

A consulta isolada devolveu `5` pedidos em ambos os planos. Depois da mudança, o plano usou o índice para o filtro, sem o nó de ordenação separado observado em D5. Esse diagnóstico sustenta o mecanismo local descrito em [2][3][4]; não permite extrapolar a diferença de tempos para a API inteira.

## Limites da conclusão

- O ensaio agrupa três execuções em E0, três em E1, cinco em E2, três na referência na tomada, três em E3, três em E4, três em E5, três em E6 e três em E7, em blocos sucessivos. A tomada era a condição planejada para as comparações de E3 a E7. Os parâmetros e os limites dos contêineres estão em `contexto.txt`. A alimentação e os programas abertos foram anotados como condições do teste. Avaliar o modo de energia e a temperatura exigiria medições adicionais.
- A carga tem usuários virtuais que fazem chamadas em sequência. Uma versão mais rápida completa mais chamadas; a semente mantém a sequência por usuário, mas não torna idêntica a quantidade de chamadas concluídas em cada rota.
- O aumento do uso da API pode estar relacionado ao maior trabalho concluído ou a outras condições do ensaio. A causa dessa variação não foi isolada.
- O contrato verifica os casos gravados. Ele não substitui uma demonstração de equivalência para todas as entradas possíveis.
- A instrumentação de `cpu_max` tem a limitação descrita acima.
- As tabelas e os dados são sintéticos; o custo de atualização dos índices e o comportamento com outra distribuição de dados não foram avaliados.

Conclusão de E1: manter como resultado favorável para p95 e requisições/s neste ensaio, apresentando também a piora de p50, o consumo observado e o armazenamento adicional. A solução ainda contém outros candidatos de otimização.

## Referência na tomada

A reversão de `048a6f3` foi registrada em `d5794bb` e retirou o segundo índice da configuração medida. A escolha da versão com um índice é provisória. O efeito incremental de E2 sob carga continuou inconclusivo diante da dispersão e das mudanças de ambiente.

As três rodadas de `01-indice-itens-tomada` estão em `a02e219`. Todas registraram `d5794bb`, árvore de trabalho limpa, os mesmos parâmetros e a confirmação das 42 respostas do contrato. Pelas medianas das rodadas, a referência ficou em `2.74 req/s`, p95 de `23346.4 ms`, mediana da latência de `2398.5 ms` e `0.00%` de erros. A alimentação na tomada foi registrada no planejamento e no rótulo da série.

## E3 — Pool de conexões

A versão de referência abria e fechava uma conexão com PostgreSQL a cada chamada de `consultar`. Uma mesma requisição pode fazer várias dessas chamadas. Em E3, uma instância compartilhada de `pg.Pool` usa `pool.query` para executar a consulta e devolver a conexão ao pool, onde fica disponível para reutilização. O limite escolhido foi de 20 conexões por processo da API para a carga de 20 usuários virtuais. [6]

As três rodadas de E3 registraram o mesmo commit, árvore limpa, os mesmos parâmetros e limites da referência e as 42 respostas do contrato preservadas. A mediana dos p50 caiu de `2398.5 ms` para `2095.5 ms` e a vazão mediana passou de `2.74 req/s` para `2.83 req/s`. A mediana dos p95 subiu de `23346.4 ms` para `24357.9 ms`, e a dos p99, de `35113.5 ms` para `40354.9 ms`. A memória média reportada aumentou na API e no banco. Os p95 das duas séries se sobrepõem entre rodadas. O ensaio observou respostas típicas mais rápidas e um p95 mediano maior.

Em relação à linha de base E0, a configuração acumulada com o índice dos itens e o pool apresentou p95 mediano de `24357.9 ms` frente a `49653.4 ms` e vazão de `2.83 req/s` frente a `1.40 req/s`. Essa comparação abrange as mudanças de configuração e as condições de execução dos lotes. Para avaliar o efeito incremental do pool, a referência é a série `01-indice-itens-tomada`.

## E4 — Índice de pedidos por status

A rota `GET /pedidos?status=&pagina=` responde por 15% das escolhas da carga. Ela conta os pedidos de um status e busca a página ordenada por `criado_em DESC, id DESC`. O índice B-tree em `(status, criado_em DESC, id DESC)` acompanha o filtro e a ordem da consulta. [Implementação de E4](banco/05-indice-pedidos-status.sql)

| Consulta isolada | Antes | Depois | Plano depois |
| --- | ---: | ---: | --- |
| Contagem dos pedidos pagos | 1767.218 ms | 86.252 ms | `Parallel Index Only Scan`, com `Heap Fetches: 0` |
| Página 250 dos pedidos pagos | 301.210 ms | 25.179 ms | `Index Scan` na ordem solicitada |

D8 registrou `Parallel Seq Scan` nas duas consultas e `external merge` em parte da ordenação da página. D9 registrou leitura pelo novo índice nos dois planos. Na contagem, o PostgreSQL consultou o índice com zero buscas de tuplas na tabela. Na paginação, a ordem do índice permitiu que o plano entregasse as linhas ao `Limit` diretamente. Os tempos são diagnósticos pontuais de SQL. [D8 — antes](diagnostico/08-pedidos-status-antes.txt) · [D9 — depois e tamanho do índice](diagnostico/09-pedidos-status-depois.txt) · [2][3][4][7]

Em cada uma das três rodadas de E4, a vazão foi maior e o p50 geral foi menor que em qualquer rodada de E3. Na rota de pedidos por status, a mediana dos p50 das três rodadas caiu de `17276.1 ms` para `2286.2 ms`, e a mediana dos p95 foi de `26157.4 ms` para `16482.8 ms`. Essa observação por rota complementa a comparação geral.

O p95 geral mediano subiu de `24357.9 ms` para `26459.7 ms` e o p99 geral mediano caiu de `40354.9 ms` para `32833.8 ms`. Os p95 por execução apresentam sobreposição. Houve duas falhas em `/relatorios/top-produtos` durante a carga de E4, e as 42 respostas do contrato foram preservadas nas três rodadas.

Em relação à linha de base E0, a configuração acumulada de E4 chegou a `3.61 req/s` ante `1.40 req/s`, e a `p95 de 26459.7 ms` ante `49653.4 ms`. Essa comparação inclui as mudanças acumuladas e a variação de ambiente entre os lotes.

## E5 — Ranking de produtos

A consulta anterior juntava os dados de `produtos` aos itens antes de agregar. A consulta reescrita soma as vendas por `produto_id`, escolhe os primeiros produtos por receita e busca o nome e a categoria de quem entrou no ranking. A chave estrangeira de `itens_pedido.produto_id` para `produtos.id` sustenta a junção após o limite. O desempate pelo ID aparece na seleção e na ordenação do resultado. [Implementação de E5](api/src/rotas.js) · [1][8]

O plano anterior fez um `Hash Join` com `produtos` antes da agregação, com `rows=450000 loops=3` nesse nó. No plano reescrito, o `Limit` entregou 10 linhas ao `Nested Loop` e a leitura de `produtos_pkey` executou `rows=1 loops=10`. O tempo da consulta isolada passou de `4730.858 ms` para `2392.841 ms`. A memória reportada pelo `Finalize HashAggregate` passou de `3089kB` para `2321kB`. [D10 — antes](diagnostico/10-top-produtos-antes.txt) · [D11 — depois](diagnostico/11-top-produtos-depois.txt) · [4]

O p95 geral foi menor em cada rodada de E5 que em qualquer rodada de E4. Pelas medianas, o p95 caiu de `26459.7 ms` para `17109.9 ms`, e a vazão passou de `3.61 req/s` para `4.31 req/s`. O p50 geral subiu de `1574.2 ms` para `1687.9 ms` e o p99 caiu de `32833.8 ms` para `30293.5 ms`. A CPU média reportada subiu nos dois contêineres. A memória média subiu no banco e caiu na API.

O relatório `/relatorios/top-produtos` teve quatro, quatro e três chamadas nas rodadas de E5, com zero falhas registradas. A amostra por rota é pequena. As três rodadas também preservaram as 42 respostas do contrato. A primeira verificação do contrato, logo após reconstruir a imagem da API, retornou `fetch failed`. O contrato passou na segunda tentativa, antes dos testes de carga.

Na comparação acumulada com E0, E5 registrou `4.31 req/s` frente a `1.40 req/s`, p95 de `17109.9 ms` frente a `49653.4 ms` e mediana de erros de `0.00%` frente a `0.87%`. O efeito incremental da reescrita usa E4 como referência. A comparação com E0 inclui as mudanças acumuladas e as condições de execução de cada lote.

## E6 — Índice para vendas por dia

O plano da consulta de sete dias em E5 usou `Parallel Seq Scan` em `pedidos` para aplicar o filtro de data. O índice parcial de E6 registra `criado_em::date` para as linhas em que `status <> 'cancelado'`, as mesmas condições da consulta. O plano de E6 fez `Bitmap Index Scan` no novo índice para localizar os pedidos do período. A consulta devolveu `12945` linhas em cada plano. [Implementação de E6](banco/06-indice-pedidos-dia.sql) · [9][10]

O tempo SQL observado passou de `6090.494 ms` para `17.596 ms`. D12 registrou `shared hit=22906 read=15256` na execução. D13 registrou `shared hit=18322`. Além da mudança do plano, as condições de cache diferiram entre essas duas execuções. Os testes de carga dão a comparação da API. [D12 — antes](diagnostico/12-vendas-por-dia-antes.txt) · [D13 — depois e tamanho do índice](diagnostico/13-vendas-por-dia-depois.txt) · [4]

Todas as rodadas de E6 tiveram vazão maior e p50 geral menor que qualquer rodada de E5. Pelas medianas, a vazão foi de `4.31 req/s` para `6.53 req/s`, o p50 foi de `1687.9 ms` para `1297.2 ms` e o p95 foi de `17109.9 ms` para `10458.9 ms`. O p99 caiu de `30293.5 ms` para `19664.4 ms`. As três rodadas registraram `0.00%` de erros e mantiveram as 42 respostas do contrato.

Na rota `/relatorios/vendas-por-dia`, a mediana dos p95 passou de `31519.9 ms` para `18915.8 ms`. E5 teve 19 ou 20 chamadas dessa rota por rodada. E6 teve 21, 29 e 30 chamadas. A comparação geral continua baseada nas métricas de todas as requisições.

Na comparação acumulada com E0, E6 passou de `1.40 req/s` para `6.53 req/s` e de p95 `49653.4 ms` para `10458.9 ms`. A mediana de erros foi de `0.87%` para `0.00%`. Esses valores descrevem o conjunto de mudanças e as condições em que cada lote foi executado. E5 é a referência direta para o efeito incremental do índice diário.

## E7 — Busca em lote na rota de pedidos do cliente

A rota consultava o cliente, buscava seus pedidos, consultava os itens de cada pedido e buscava um produto para cada item. Para o cliente 42, D14 registrou 5 pedidos e 10 itens. Pelo fluxo do código, esse caso passava por 17 consultas e passou a 3 com a busca em lote. A terceira consulta usa os IDs dos pedidos como parâmetro e junta os itens aos nomes dos produtos. A API agrupa os itens por pedido e calcula os totais na ordem do contrato. [D14 — contagem e plano](diagnostico/14-pedidos-cliente-lote-antes.txt) · [Implementação de E7](api/src/rotas.js) · [11][12][13]

O diagnóstico isolado da busca dos pedidos do cliente 42 registrou `384.358 ms` e `Parallel Seq Scan` em `pedidos`. Essa etapa faz parte do tempo total da rota. A contagem de consultas de E7 descreve o caminho do código para esse cliente. A latência e a vazão foram avaliadas no teste de carga.

A vazão mediana passou de `6.53 req/s` em E6 para `5.19 req/s` em E7. O p50 geral passou de `1297.2 ms` para `1588.9 ms`, o p95 de `10458.9 ms` para `13337.7 ms` e o p99 de `19664.4 ms` para `21836.9 ms`. Na rota de pedidos do cliente, a mediana dos p95 passou de `10458.9 ms` para `14046.7 ms`. As rodadas de E7 incluíram 74, 69 e 70 chamadas dessa rota. Todas preservaram as 42 respostas do contrato e registraram `0.00%` de erros gerais.

E6 e E7 foram medidos em horários distintos no mesmo dia. Os parâmetros da carga e as cotas dos contêineres coincidiram. A diferença de horário limita a atribuição dos resultados à reescrita. Para a comparação final, E6 foi escolhida pela vazão e pelo p95 observados nas séries disponíveis.

## Validação da versão otimizada com 20 usuários virtuais

A versão original corresponde ao commit `306ae69`. A versão otimizada corresponde a `5c692fc`, com os índices de E1, E4 e E6, o pool de E3 e a reescrita do ranking de E5. A conferência do Git confirmou que a régua, a carga, o contrato, os arquivos iniciais do banco e o Compose são iguais nos dois commits.

No mesmo notebook, cada versão usou um projeto Docker Compose e um volume próprios. As versões foram iniciadas e paradas alternadamente, com a original primeiro em cada par. Os seis arquivos `contexto.txt` confirmam 20 usuários virtuais, `60s` de carga, `15s` de aquecimento, semente `42` e `arquivos alterados sem commit: 0`. O banco teve cota de `1` CPU e `512 MiB`, e a API teve cota de `0.5` CPU e `256 MiB` nas seis rodadas.

| Pasta em `resultados/` | Requisições | Req/s | p50 (ms) | p95 (ms) | p99 (ms) | Erros |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [`20261111-221617-08-validacao-original-20vus`](resultados/20261111-221617-08-validacao-original-20vus/resumo.txt) | 100 | 1.22 | 2375.6 | 57015.8 | 59986.7 | 5.00% |
| [`20261111-222012-08-validacao-otimizada-20vus`](resultados/20261111-222012-08-validacao-otimizada-20vus/resumo.txt) | 232 | 3.09 | 2831.3 | 21791.8 | 31818.0 | 0.43% |
| [`20261111-224934-08-validacao-original-20vus`](resultados/20261111-224934-08-validacao-original-20vus/resumo.txt) | 120 | 1.52 | 2651.1 | 44433.8 | 54799.8 | 0.00% |
| [`20261111-225157-08-validacao-otimizada-20vus`](resultados/20261111-225157-08-validacao-otimizada-20vus/resumo.txt) | 466 | 7.51 | 1400.7 | 8024.2 | 15521.8 | 0.00% |
| [`20261111-225344-08-validacao-original-20vus`](resultados/20261111-225344-08-validacao-original-20vus/resumo.txt) | 113 | 1.36 | 2303.8 | 50900.5 | 59486.7 | 1.77% |
| [`20261111-225612-08-validacao-otimizada-20vus`](resultados/20261111-225612-08-validacao-otimizada-20vus/resumo.txt) | 455 | 7.32 | 1628.0 | 8325.2 | 15445.7 | 0.00% |
| **Mediana da original** | **113** | **1.36** | **2375.6** | **50900.5** | **59486.7** | **1.77%** |
| **Mediana da otimizada** | **455** | **7.32** | **1628.0** | **8325.2** | **15521.8** | **0.00%** |

Os valores de `resumo.txt` coincidem com as métricas de `resumo-k6.json` à precisão exibida. A vazão é `http_reqs.rate` do k6. A carga configura `constant-vus` com duração de `60s` e `gracefulStop` de `30s`. O k6 registra o tempo efetivo de cada execução em `testRunDurationMs`.

As três rodadas otimizadas tiveram maior vazão e menor p95 que qualquer rodada da original. Na primeira dupla, o p50 subiu de `2375.6 ms` para `2831.3 ms`. O k6 registrou 5, 0 e 2 falhas na versão original e 1, 0 e 0 na otimizada. O log da primeira rodada otimizada registrou um timeout em `/relatorios/top-produtos`. As 42 respostas gravadas foram confirmadas no contrato após a carga das seis rodadas.

| Recurso, mediana das médias por rodada | Original | Otimizada |
| --- | ---: | ---: |
| CPU do banco | 97.6% | 98.8% |
| Memória do banco | 174.5 MiB | 319.2 MiB |
| CPU da API | 8.5% | 20.9% |
| Memória da API | 26.8 MiB | 39.9 MiB |

A CPU média do banco ficou próxima de uma CPU inteira nas duas versões. A versão otimizada completou mais requisições e usou mais memória nos dois serviços e mais CPU na API sob as mesmas cotas. Os tamanhos dos três índices registrados nos respectivos diagnósticos somam `59088896` bytes. [D4](diagnostico/04-custo-indice-itens.txt) · [D9](diagnostico/09-pedidos-status-depois.txt) · [D13](diagnostico/13-vendas-por-dia-depois.txt)

As médias de `recursos.txt` foram reproduzidas com as primeiras amostras de `recursos.csv`, até a contagem `amostras` de cada serviço. Cada CSV tinha uma amostra adicional por serviço. Os picos reportados apresentam divergências. Na segunda rodada original, por exemplo, `mem_max` do banco aparece como `96.6 MiB` e a maior amostra de memória entre as 39 usadas no resumo é `237.8 MiB`. A comparação de recursos usa as médias conferidas.

A primeira dupla antecedeu o bloco das duas duplas seguintes. A alternância aproxima as condições das duas versões ao longo do teste. O estado do cache, a temperatura e a carga dos demais programas são condições do notebook sem telemetria nos arquivos da régua.

## Validação com 5 usuários virtuais

A sessão de 12/11/2026 começou após um reinício do notebook. Foram três pares alternados de `306ae69` e `5c692fc`, com a original primeiro em cada par. Os arquivos `contexto.txt` confirmam `VUS=5`, `DURACAO=60s`, `AQUECIMENTO=15s`, `SEMENTE=42` e `arquivos alterados sem commit: 0` nas seis rodadas. As cotas foram de `1` CPU e `512 MiB` para o banco e `0.5` CPU e `256 MiB` para a API.

| Pasta em `resultados/` | Requisições | Req/s | p50 (ms) | p95 (ms) | p99 (ms) | Erros |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [`20261112-153542-09-validacao-original-5vus`](resultados/20261112-153542-09-validacao-original-5vus/resumo.txt) | 95 | 1.46 | 1098.2 | 11555.2 | 13348.9 | 0.00% |
| [`20261112-153753-09-validacao-otimizada-5vus`](resultados/20261112-153753-09-validacao-otimizada-5vus/resumo.txt) | 457 | 7.45 | 506.8 | 1627.4 | 5327.8 | 0.00% |
| [`20261112-153942-09-validacao-original-5vus`](resultados/20261112-153942-09-validacao-original-5vus/resumo.txt) | 64 | 0.92 | 1887.9 | 17183.9 | 20398.5 | 0.00% |
| [`20261112-154214-09-validacao-otimizada-5vus`](resultados/20261112-154214-09-validacao-otimizada-5vus/resumo.txt) | 264 | 4.20 | 911.2 | 3376.7 | 7868.5 | 0.00% |
| [`20261112-154432-09-validacao-original-5vus`](resultados/20261112-154432-09-validacao-original-5vus/resumo.txt) | 61 | 0.91 | 1693.7 | 16215.6 | 21111.7 | 0.00% |
| [`20261112-154722-09-validacao-otimizada-5vus`](resultados/20261112-154722-09-validacao-otimizada-5vus/resumo.txt) | 254 | 4.10 | 1000.1 | 2832.6 | 7748.4 | 0.00% |
| **Mediana da original** | 64 | 0.92 | 1693.7 | 16215.6 | 20398.5 | 0.00% |
| **Mediana da otimizada** | 264 | 4.20 | 911.2 | 2832.6 | 7748.4 | 0.00% |

A primeira dupla teve a maior vazão de cada versão. A rodada otimizada de menor vazão ainda superou a melhor rodada original, e o p95 ficou abaixo do menor p95 da original nas três rodadas otimizadas. Os valores de `resumo.txt` coincidem com os de `resumo-k6.json` à precisão exibida. As seis rodadas tiveram zero falhas durante a carga e confirmaram as 42 respostas gravadas no contrato.

| Recurso, mediana das médias por rodada | Original | Otimizada |
| --- | ---: | ---: |
| CPU do banco | 97.3% | 92.4% |
| Memória do banco | 150.3 MiB | 234.2 MiB |
| CPU da API | 6.9% | 19.4% |
| Memória da API | 23.7 MiB | 29.3 MiB |

Sob as mesmas cotas, a otimizada atendeu mais requisições com menor CPU média do banco e maior CPU média da API. O consumo médio de memória subiu nos dois serviços. A conferência reproduziu as médias de `recursos.txt` com as amostras correspondentes de `recursos.csv`. Na segunda rodada original, o máximo de memória do banco aparece como `72.7 MiB` e a maior das 35 amostras usadas no resumo é `208 MiB`. A comparação de recursos usa as médias conferidas.

Os níveis de 5 e 20 usuários virtuais foram executados em sessões distintas. A comparação entre versões usa as rodadas no mesmo nível de carga. O estado do notebook entre sessões é uma possível fonte de variação na comparação entre níveis.

## Validação com 40 usuários virtuais

Em 12/11/2026 foram medidos três pares alternados dos commits `306ae69` e `5c692fc`, com a original primeiro em cada par. Os seis arquivos `contexto.txt` registram `VUS=40`, `DURACAO=60s`, `AQUECIMENTO=15s`, `SEMENTE=42` e `arquivos alterados sem commit: 0`. A cota do banco foi de `1` CPU e `512 MiB`, e a da API, de `0.5` CPU e `256 MiB` nas duas versões.

| Pasta em `resultados/` | Requisições | Req/s | p50 (ms) | p95 (ms) | p99 (ms) | Erros |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [`20261112-160417-10-validacao-original-40vus`](resultados/20261112-160417-10-validacao-original-40vus/resumo.txt) | 146 | 1.62 | 3750.8 | 60008.0 | 60576.7 | 15.75% |
| [`20261112-160821-10-validacao-otimizada-40vus`](resultados/20261112-160821-10-validacao-otimizada-40vus/resumo.txt) | 300 | 4.49 | 4807.1 | 28679.2 | 43534.9 | 0.00% |
| [`20261112-161054-10-validacao-original-40vus`](resultados/20261112-161054-10-validacao-original-40vus/resumo.txt) | 113 | 1.26 | 5489.2 | 59986.4 | 59992.1 | 27.43% |
| [`20261112-161423-10-validacao-otimizada-40vus`](resultados/20261112-161423-10-validacao-otimizada-40vus/resumo.txt) | 381 | 4.90 | 3532.4 | 26060.0 | 31841.0 | 0.00% |
| [`20261112-161648-10-validacao-original-40vus`](resultados/20261112-161648-10-validacao-original-40vus/resumo.txt) | 124 | 1.38 | 6040.7 | 59984.0 | 59984.7 | 25.00% |
| [`20261112-162053-10-validacao-otimizada-40vus`](resultados/20261112-162053-10-validacao-otimizada-40vus/resumo.txt) | 340 | 4.75 | 4096.5 | 24312.6 | 36323.7 | 0.00% |
| **Mediana da original** | 124 | 1.38 | 5489.2 | 59986.4 | 59992.1 | 25.00% |
| **Mediana da otimizada** | 340 | 4.75 | 4096.5 | 26060.0 | 36323.7 | 0.00% |

A original registrou 23, 31 e 31 falhas durante a carga, totalizando 85. Os resumos do k6 registram 56 em `pedidos-do-cliente`, 16 em `pedidos-por-status`, 10 em `vendas-por-dia` e 3 em `top-produtos`. A otimizada teve zero falhas nas três rodadas. O contrato confirmou as 42 respostas gravadas após a carga em todas as execuções. A vazão é a taxa `http_reqs.rate` do k6, e a taxa de erros vem de `http_req_failed`.

| Recurso, mediana das médias por rodada | Original | Otimizada |
| --- | ---: | ---: |
| CPU do banco | 99.4% | 99.5% |
| Memória do banco | 229.3 MiB | 265.4 MiB |
| CPU da API | 10.5% | 26.9% |
| Memória da API | 33.3 MiB | 42.0 MiB |

O banco trabalhou perto da cota de uma CPU nas duas versões. A versão otimizada completou mais requisições sob as mesmas cotas, com maior CPU média da API e maior memória média nos dois serviços. As médias dos resumos foram reproduzidas com as amostras do CSV até a contagem de cada serviço. Na primeira rodada original, o `mem_max` do banco indica `91.6 MiB`, e a maior das 47 amostras usadas no resumo é `301.4 MiB`. A comparação de recursos usa as médias conferidas.

## Comparação dos três níveis de carga

A validação reúne 18 execuções. Em cada nível foram feitas três rodadas de cada versão, com os mesmos parâmetros de carga, cotas e dados iniciais. A tabela apresenta as medianas de cada métrica da original e da otimizada.

| Usuários virtuais | Vazão (req/s) | p50 (ms) | p95 (ms) | p99 (ms) | Erros durante a carga |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 0.92 → 4.20 | 1693.7 → 911.2 | 16215.6 → 2832.6 | 20398.5 → 7748.4 | 0.00% → 0.00% |
| 20 | 1.36 → 7.32 | 2375.6 → 1628.0 | 50900.5 → 8325.2 | 59486.7 → 15521.8 | 1.77% → 0.00% |
| 40 | 1.38 → 4.75 | 5489.2 → 4096.5 | 59986.4 → 26060.0 | 59992.1 → 36323.7 | 25.00% → 0.00% |

Em cada nível, todas as rodadas otimizadas tiveram vazão maior e p95 menor que todas as rodadas originais. A diferença na taxa de erros foi mais pronunciada a 40 usuários virtuais. A mediana de `0.00%` de erros da otimizada com 20 usuários virtuais inclui uma primeira rodada com `0.43%` de falhas. O cenário de 40 usuários virtuais ainda apresentou p95 mediano de `26060.0 ms` na otimizada.

Nos três níveis, o uso médio de memória aumentou nos dois serviços e o de CPU aumentou na API. O desempenho foi medido sob as mesmas cotas de CPU e memória, com o espaço adicional dos três índices documentado em D4, D9 e D13. A avaliação de custo cobre esses recursos e o armazenamento dos índices. [D4](diagnostico/04-custo-indice-itens.txt) · [D9](diagnostico/09-pedidos-status-depois.txt) · [D13](diagnostico/13-vendas-por-dia-depois.txt)

As séries foram executadas em blocos por nível, com o cenário de 20 usuários virtuais na sessão anterior à de 5 e 40. Os efeitos de temperatura, cache e outros processos do notebook podem variar entre blocos. As diferenças de desempenho reportadas são comparações entre versões dentro do mesmo nível de carga.

O código otimizado avaliado está em `5c692fc`. A busca em lote de E7, introduzida em `fc49dd2`, foi revertida em `8e6efb0`. Após a reversão, `git diff --stat 5c692fc -- api banco docker-compose.yml carga scripts contrato` retornou sem diferenças nos arquivos comparados.

## Fontes técnicas abertas

1. [PostgreSQL 16 — Constraints, Foreign Keys](https://www.postgresql.org/docs/16/ddl-constraints.html#DDL-CONSTRAINTS-FK).
2. [PostgreSQL 16 — Multicolumn Indexes](https://www.postgresql.org/docs/16/indexes-multicolumn.html).
3. [PostgreSQL 16 — Indexes and ORDER BY](https://www.postgresql.org/docs/16/indexes-ordering.html).
4. [PostgreSQL 16 — Using EXPLAIN](https://www.postgresql.org/docs/16/using-explain.html).
5. [PostgreSQL 16 — Database Object Size Functions](https://www.postgresql.org/docs/16/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE).
6. [node-postgres — Pooling](https://node-postgres.com/features/pooling).
7. [PostgreSQL 16 — Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/16/indexes-index-only-scans.html).
8. [PostgreSQL 16 — Sorting Rows](https://www.postgresql.org/docs/16/queries-order.html).
9. [PostgreSQL 16 — Indexes on Expressions](https://www.postgresql.org/docs/16/indexes-expressional.html).
10. [PostgreSQL 16 — Partial Indexes](https://www.postgresql.org/docs/16/indexes-partial.html).
11. [Guravannavar e Sudarshan, Rewriting Procedures for Batched Bindings, VLDB 2008](https://www.vldb.org/pvldb/vol1/1453975.pdf).
12. [node-postgres — Queries, Parameterized query](https://node-postgres.com/features/queries).
13. [PostgreSQL 16 — Row and Array Comparisons, ANY](https://www.postgresql.org/docs/16/functions-comparisons.html#FUNCTIONS-COMPARISONS-ANY-SOME).

Os testes foram executados no mesmo notebook. A IA apoiou a leitura do código, a conferência dos arquivos e a comparação das medições.
