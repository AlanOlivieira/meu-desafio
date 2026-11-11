CREATE INDEX idx_pedidos_dia_nao_cancelado
    ON pedidos ((criado_em::date))
    WHERE status <> 'cancelado';
