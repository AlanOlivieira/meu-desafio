CREATE INDEX idx_pedidos_status_criado_id
    ON pedidos (status, criado_em DESC, id DESC);
