# Próximos testes

As três primeiras fichas registram alternativas pesquisadas para testes futuros. A última reúne duas mudanças já medidas que ficaram fora da configuração escolhida e indica como repetir a comparação. [Experimentos realizados](experimentos.md) · [Limites do estudo](artigo/artigo.md#7-limites-e-testes-futuros)

## Como comparar

Para mudanças compatíveis com a API atual, a referência será o código validado em `5c692fc`. Aplicar uma mudança por vez, manter dados, parâmetros e cotas dos contêineres e confirmar as 42 respostas do contrato antes da carga. Usar o mesmo notebook na tomada, com 20 usuários virtuais, 15 s de aquecimento, 60 s de carga e semente 42. Alternar as versões em três pares e comparar as medianas de vazão, p95, taxa de erros e uso médio de CPU e memória. Guardar os arquivos de cada rodada em `resultados/`. [Como medir](README.md#como-medir) · [Kalibera e Jones, 2013](https://kar.kent.ac.uk/33611/)

## 1. Índice GIN para a busca de produtos

- **Hipótese.** Um índice GIN com `pg_trgm` pode localizar candidatos para a busca por trechos de nomes feita com `ILIKE`. O ganho esperado é reduzir o p95 da rota `/produtos/busca`, preservando os resultados e a ordem por nome e ID. [PostgreSQL 16, pg_trgm](https://www.postgresql.org/docs/16/pgtrgm.html)
- **Como testar.** Comparar o plano com `EXPLAIN (ANALYZE, BUFFERS)` para termos da carga, como `cadeira` e `modelo 12`. Conferir o contrato e comparar o p95 da busca, o p95 geral e a vazão da API. Registrar o tamanho do índice e o número de chamadas da rota por rodada.
- **O que é necessário.** Habilitar a extensão e criar o índice sobre `produtos.nome` em um novo script SQL. Medir também o tempo de criação. O custo de manutenção em escritas exige um ensaio próprio. [PostgreSQL 16, custos dos índices](https://www.postgresql.org/docs/16/indexes-intro.html)

## 2. View materializada para o ranking

- **Hipótese.** Armazenar os totais por produto pode reduzir o trabalho de recalcular a receita a cada chamada de `/relatorios/top-produtos`. Quando os dados mudam, o ranking pode ficar defasado até a próxima atualização. [PostgreSQL 16, views materializadas](https://www.postgresql.org/docs/16/rules-materializedviews.html)
- **Como testar.** Comparar a consulta atual com uma leitura da view sobre os mesmos dados. Preservar a exclusão dos pedidos cancelados, os limites e a ordem por receita e ID. Medir p95 e vazão sob carga, espaço em disco e tempo de criação. Em um ensaio com escritas, medir a defasagem do ranking, o custo de atualização da view e o efeito sobre as leituras. [Plano atual do ranking](diagnostico/11-top-produtos-depois.txt) · [PostgreSQL 16, REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/16/sql-refreshmaterializedview.html)
- **O que é necessário.** Criar a view em um novo script SQL e adaptar apenas a rota do ranking. Preencher a view na inicialização para o ensaio com dados fixos. Para o ensaio com escritas, definir a frequência de atualização e a tolerância a dados defasados.

## 3. Paginação por cursor

- **Hipótese.** Para avançar entre páginas, um cursor com a data e o ID do último pedido pode reduzir o trabalho de descartar linhas no `OFFSET`. A paginação atual permite saltar diretamente para uma página pelo número e devolve também a contagem total. [Plano da página 250](diagnostico/09-pedidos-status-depois.txt) · [PostgreSQL 16, LIMIT e OFFSET](https://www.postgresql.org/docs/16/queries-limit.html) · [GitLab, paginação por cursor](https://docs.gitlab.com/development/database/keyset_pagination/)
- **Como testar.** Em um protótipo separado, comparar a mesma sequência de páginas com `OFFSET` e com cursor. Verificar IDs e ordem por `criado_em DESC, id DESC`, inclusive em empates de data. Medir a consulta de paginação e o custo da contagem total separadamente. Para medir a navegação pela API, usar uma carga própria do protótipo.
- **O que é necessário.** Usar a mesma base, o mesmo filtro de status e o índice de pedidos por status. O protótipo precisa de um cliente que mantenha o cursor entre chamadas. A rota por número de página continua disponível no projeto entregue. [GitLab, diretrizes de paginação](https://docs.gitlab.com/development/database/pagination_guidelines/)

## Repetição dos testes de pedidos por cliente

O índice de pedidos por cliente teve ganho no SQL isolado e resultados mistos sob carga. A busca em lote reduziu o número de consultas no caso do cliente 42. Na série medida com a busca em lote, em outro horário, a vazão foi menor e o p95 foi maior. Para investigar esses resultados, comparar a configuração validada com cada uma das duas mudanças separadamente, em rodadas alternadas na mesma sessão. Registrar p95 geral e da rota de pedidos do cliente, vazão e consumo de recursos. [Experimentos E2 e E7](experimentos.md) · [Diagnóstico do cliente 42](diagnostico/14-pedidos-cliente-lote-antes.txt)
