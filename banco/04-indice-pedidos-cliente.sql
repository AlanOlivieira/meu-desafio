-- H2: localizar os pedidos do cliente na ordem exigida pela API.
CREATE INDEX idx_pedidos_cliente_criado_id
    ON pedidos (cliente_id, criado_em DESC, id DESC);