# Próximos testes

Os testes do GIN e da cota de `0,4 CPU` já têm resultados e deram origem a novas perguntas de investigação. [Experimentos realizados](experimentos.md) · [Limites do estudo](artigo/artigo.md#7-limites-e-testes-futuros)

## Como comparar

Para mudanças compatíveis com a API atual, usar `5c692fc` como referência, variar um fator por vez e manter os demais parâmetros iguais. Confirmar as 42 respostas do contrato antes e depois da carga. Usar o notebook na tomada, com 20 usuários virtuais, 15 s de aquecimento, 60 s de carga e semente 42. Quando houver mais de um nível de carga, comparar as versões dentro de cada nível. Alternar a ordem das versões, fazer pelo menos três rodadas por configuração e comparar as medianas de vazão, p95, erros, CPU e memória. Guardar os arquivos de cada rodada em `resultados/` e os planos e demais diagnósticos em `diagnostico/`. [Como medir](README.md#como-medir) · [Kalibera e Jones, 2013](https://kar.kent.ac.uk/33611/)

## 1. Índice por expressão para a busca por e-mail

- **Hipótese.** Um índice em `lower(email)` pode acelerar a consulta de clientes por e-mail. A rota tem peso de 15% na carga e p50 mediano de 3.599,9 ms na linha de base. [Consulta](api/src/rotas.js) · [Linha de base](experimentos.md#execuções-e-resultados-gerais) · [PostgreSQL 16, índices por expressão](https://www.postgresql.org/docs/16/indexes-expressional.html)
- **Como testar.** Obter planos com `EXPLAIN (ANALYZE, BUFFERS)` para um e-mail existente e um ausente. Se houver varredura, comparar com um índice na expressão, preservando a ordenação por ID. Medir p95 da rota e da API, vazão e espaço em disco.
- **O que é necessário.** Registrar os planos e, para testar o índice, criar um novo script SQL e recriar o banco com os mesmos dados.

## 2. Redução da cota de memória da API

- **Hipótese.** A API pode sustentar a carga com um limite de 128 MiB. A maior amostra de memória da API nas três rodadas da referência complementar foi de 81,12 MiB. [Amostras da referência](resultados/20261114-220214-11-referencia-otimizada-20vus/recursos.csv) · [Docker, limites de memória](https://docs.docker.com/engine/containers/resource_constraints/#memory)
- **Como testar.** Comparar 256 e 128 MiB com 20 e 40 usuários virtuais, mantendo a API em `0,5 CPU`. Acompanhar vazão, p95, erros, pico de memória e encerramentos por falta de memória.
- **O que é necessário.** Alterar apenas o limite de memória da API no Compose e registrar o limite efetivo e o estado do contêiner ao fim de cada rodada. [Configuração atual](docker-compose.yml)

## 3. Diagnóstico da limitação de CPU da API

- **Hipótese.** A API pode atingir o teto de `0,4 CPU` em rajadas, mesmo com uso médio de 21,7% de um núcleo. O diagnóstico verifica se a limitação aumenta quando a cota diminui. [Experimentos realizados](experimentos.md) · [Linux, controle de CPU](https://docs.kernel.org/scheduler/sched-bwc.html)
- **Como testar.** Comparar `5c692fc` com `4678071` e coletar `cpu.stat` do contêiner da API durante a carga. Comparar os incrementos de `nr_periods`, `nr_throttled` e do tempo de limitação em janelas equivalentes, junto de p95, vazão e erros.
- **O que é necessário.** Identificar a versão de cgroup usada pelo Docker e registrar a coleta como diagnóstico. O campo de tempo é `throttled_usec` no cgroup v2 e `throttled_time` no v1. [Linux, cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) · [Linux, estatísticas da cota](https://docs.kernel.org/scheduler/sched-bwc.html#statistics)

## 4. Ajuste de `work_mem`

- **Hipótese.** Aumentar `work_mem` pode reduzir o uso de arquivos temporários em ordenações que ainda recorrem a disco na versão final. Cada operação pode usar essa memória, e o consumo pode crescer com consultas simultâneas. [PostgreSQL 16, consumo de recursos](https://www.postgresql.org/docs/16/runtime-config-resource.html)
- **Como testar.** Rodar `EXPLAIN` na versão `5c692fc` para verificar se ainda há ordenações em disco. O plano da página 250 registrado após a criação do índice por status já exibia `Index Scan`. Ao encontrar uma ordenação em disco, variar apenas `work_mem` e registrar o uso de temporários, p95, vazão e memória do banco. [Plano da página 250](diagnostico/09-pedidos-status-depois.txt)
- **O que é necessário.** Aplicar o parâmetro com `-c work_mem=...` no serviço do banco, preservar a cota de 512 MiB e guardar os planos de antes e depois.

## 5. View materializada para o ranking

- **Hipótese.** Armazenar os totais por produto pode reduzir o trabalho de recalcular a receita a cada chamada de `/relatorios/top-produtos`. Quando os dados mudam, o ranking pode ficar defasado até a próxima atualização. [PostgreSQL 16, views materializadas](https://www.postgresql.org/docs/16/rules-materializedviews.html)
- **Como testar.** Comparar a consulta atual com uma leitura da view sobre os mesmos dados. Preservar a exclusão dos pedidos cancelados, os limites e a ordem por receita e ID. Medir p95 e vazão sob carga, espaço em disco e tempo de criação. Em um ensaio com escritas, medir a defasagem do ranking, o custo de atualização da view e o efeito sobre as leituras. [Plano atual do ranking](diagnostico/11-top-produtos-depois.txt) · [PostgreSQL 16, REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/16/sql-refreshmaterializedview.html)
- **O que é necessário.** Criar a view em um novo script SQL e adaptar apenas a rota do ranking. Preencher a view na inicialização para o ensaio com dados fixos. Para o ensaio com escritas, definir a frequência de atualização e a tolerância a dados defasados.

## 6. Paginação por cursor

- **Hipótese.** Para avançar entre páginas, um cursor com a data e o ID do último pedido pode reduzir o trabalho de descartar linhas no `OFFSET`. A paginação atual permite saltar diretamente para uma página pelo número e devolve também a contagem total. [Plano da página 250](diagnostico/09-pedidos-status-depois.txt) · [PostgreSQL 16, LIMIT e OFFSET](https://www.postgresql.org/docs/16/queries-limit.html) · [GitLab, paginação por cursor](https://docs.gitlab.com/development/database/keyset_pagination/)
- **Como testar.** Em um protótipo separado, comparar a mesma sequência de páginas com `OFFSET` e com cursor. Verificar IDs e ordem por `criado_em DESC, id DESC`, inclusive em empates de data. Medir a consulta de paginação e o custo da contagem total separadamente. Para medir a navegação pela API, usar uma carga própria do protótipo.
- **O que é necessário.** Usar a mesma base, o mesmo filtro de status e o índice de pedidos por status. O protótipo precisa de um cliente que mantenha o cursor entre chamadas. [GitLab, diretrizes de paginação](https://docs.gitlab.com/development/database/pagination_guidelines/)

## Reavaliação de mudanças já medidas

### GIN sob carga mista

- **Hipótese.** O ganho no p95 da busca pode se repetir com vazão geral comparável à referência em uma série maior.
- **Como testar.** Comparar `5c692fc` e `70042d9` em mais de três pares alternados na mesma sessão, com a carga completa. Medir p95 da busca e da API, vazão, erros e recursos.
- **O que é necessário.** Usar os mesmos dados, cotas e parâmetros de carga. Guardar as rodadas e os planos SQL para investigar a diferença de vazão. [Documentação do pg_trgm](https://www.postgresql.org/docs/16/pgtrgm.html) · [Experimentos realizados](experimentos.md)

### Índice e busca em lote de pedidos por cliente

O índice de pedidos por cliente teve ganho no SQL isolado e resultados mistos sob carga. A busca em lote reduziu o número de consultas no caso do cliente 42. Na série medida com a busca em lote, em outro horário, a vazão foi menor e o p95 foi maior. Para investigar esses resultados, comparar a configuração validada com cada uma das duas mudanças separadamente, em rodadas alternadas na mesma sessão. Registrar p95 geral e da rota de pedidos do cliente, vazão e consumo de recursos. [Experimentos E2 e E7](experimentos.md) · [Diagnóstico do cliente 42](diagnostico/14-pedidos-cliente-lote-antes.txt)

## Custo dos índices nas escritas

Um ensaio com inserções e atualizações concorrentes pode medir o custo de manter os índices. Em um ambiente de teste separado, comparar a mesma base sintética com e sem os índices acrescentados neste trabalho. Medir p95 das escritas, vazão de leitura e espaço em disco sob uma carga auxiliar com leituras e escritas. [PostgreSQL 16, custos dos índices](https://www.postgresql.org/docs/16/indexes-intro.html)
