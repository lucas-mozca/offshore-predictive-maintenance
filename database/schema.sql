CREATE TABLE equipamentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(100) NOT NULL,
    modelo VARCHAR(100),
    status VARCHAR(30) NOT NULL,
    data_instalacao DATE NOT NULL
);

CREATE TABLE sensores_telemetria (
    id BIGSERIAL PRIMARY KEY,
    id_equipamento INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperatura_celsius DECIMAL(6,2) NOT NULL,
    vibracao_mm_s DECIMAL(6,2) NOT NULL,
    pressao_bar DECIMAL(6,2) NOT NULL,
    status VARCHAR(30) NOT NULL,

    CONSTRAINT fk_telemetria_equipamento
        FOREIGN KEY (id_equipamento)
        REFERENCES equipamentos(id)
);

CREATE TABLE alertas (
    id BIGSERIAL PRIMARY KEY,
    id_equipamento INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    mensagem TEXT NOT NULL,
    resolvido BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_alerta_equipamento
        FOREIGN KEY (id_equipamento)
        REFERENCES equipamentos(id)
);

CREATE TABLE manutencoes (
    id BIGSERIAL PRIMARY KEY,
    id_equipamento INTEGER NOT NULL,
    data TIMESTAMP NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    descricao TEXT NOT NULL,
    responsavel VARCHAR(100),

    CONSTRAINT fk_manutencao_equipamento
        FOREIGN KEY (id_equipamento)
        REFERENCES equipamentos(id)
);