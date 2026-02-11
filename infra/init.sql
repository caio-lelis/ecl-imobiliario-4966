CREATE TABLE historico_mensal (
    id SERIAL PRIMARY KEY,
    id_contrato INT REFERENCES contratos(id_contrato),
    data_referencia DATE NOT NULL,
    saldo_devedor NUMERIC(15,2) NOT NULL,
    dias_atraso INT NOT NULL,
    desemprego NUMERIC(5,2) NOT NULL,
    selic NUMERIC(5,2) NOT NULL,
    default_flag INT NOT NULL
);

CREATE TABLE contratos (
    id_contrato SERIAL PRIMARY KEY,
    data_concessao DATE NOT NULL,
    valor_imovel NUMERIC(15,2) NOT NULL,
    valor_financiado NUMERIC(15,2) NOT NULL,
    ltv NUMERIC(5,4) NOT NULL,
    prazo_anos INT NOT NULL,
    taxa_juros NUMERIC(5,4) NOT NULL,
    renda_cliente NUMERIC(12,2) NOT NULL,
    score_credito INT NOT NULL,
    idade_cliente INT NOT NULL,
    regiao VARCHAR(50) NOT NULL
);