CREATE TABLE IF NOT EXISTS clientes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    cpf         TEXT NOT NULL UNIQUE
                CHECK (
                    length(cpf) = 11
                    AND cpf NOT GLOB '*[^0-9]*'
                ),
    telefone    TEXT NOT NULL CHECK (length(trim(telefone)) > 0),
    email       TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS quartos (
    numero          INTEGER PRIMARY KEY CHECK (numero > 0),
    tipo            TEXT NOT NULL
                    CHECK (tipo IN ('Simples', 'Duplo', 'Suíte')),
    valor_diaria    REAL NOT NULL CHECK (valor_diaria > 0),
    estado          TEXT NOT NULL DEFAULT 'disponivel'
                    CHECK (estado IN (
                        'disponivel',
                        'reservado',
                        'ocupado',
                        'limpeza',
                        'manutencao'
                    ))
);

CREATE TABLE IF NOT EXISTS reservas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    quarto_numero   INTEGER NOT NULL REFERENCES quartos(numero) ON DELETE RESTRICT,
    data_checkin    TEXT NOT NULL,
    data_checkout   TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'CONFIRMADA'
                    CHECK (status IN ('CONFIRMADA', 'CANCELADA', 'FINALIZADA')),
    CHECK (data_checkout > data_checkin)
);

CREATE INDEX IF NOT EXISTS idx_reservas_cliente ON reservas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_reservas_quarto  ON reservas(quarto_numero);
CREATE INDEX IF NOT EXISTS idx_reservas_datas   ON reservas(data_checkin, data_checkout);

CREATE TABLE IF NOT EXISTS itens (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL UNIQUE,
    preco   REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS estadias (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id      INTEGER NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    quarto_numero   INTEGER NOT NULL REFERENCES quartos(numero) ON DELETE RESTRICT,
    reserva_id      INTEGER REFERENCES reservas(id) ON DELETE SET NULL,
    data_checkin    TEXT NOT NULL,
    data_checkout   TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'HOSPEDADO'
                    CHECK (status IN ('HOSPEDADO', 'FINALIZADA'))
);

CREATE TABLE IF NOT EXISTS itens_fatura (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    estadia_id      INTEGER NOT NULL REFERENCES estadias(id) ON DELETE CASCADE,
    item_id         INTEGER NOT NULL REFERENCES itens(id) ON DELETE RESTRICT,
    quantidade      INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0)
);

CREATE INDEX IF NOT EXISTS idx_estadias_cliente ON estadias(cliente_id);
CREATE INDEX IF NOT EXISTS idx_estadias_quarto  ON estadias(quarto_numero);
CREATE INDEX IF NOT EXISTS idx_itens_fatura_estadia ON itens_fatura(estadia_id);

INSERT OR IGNORE INTO itens (nome, preco) VALUES
    ('Frigobar', 15.00),
    ('Lavanderia', 30.00),
    ('Serviço de Quarto', 25.00);

/*

FUNCIONALIDADES AINDA NÃO CRIADAS / TABELAS AINDA NÃO LOCALIZADAS EM PT-BR

CREATE TABLE IF NOT EXISTS item (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome   TEXT NOT NULL UNIQUE,
    preco  REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS stay (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id     INTEGER NOT NULL REFERENCES client(id) ON DELETE RESTRICT,
    room_numero   INTEGER REFERENCES room(numero) ON DELETE RESTRICT,
    checkin       TEXT NOT NULL,
    checkout      TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'RESERVADA'
                  CHECK (status IN ('RESERVADA', 'HOSPEDADO',
                                    'FINALIZADA', 'CANCELADA')),
    CHECK (checkout > checkin)
);

CREATE TABLE IF NOT EXISTS bill_item (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    stay_id         INTEGER NOT NULL REFERENCES stay(id) ON DELETE CASCADE,
    item_id         INTEGER NOT NULL REFERENCES item(id) ON DELETE RESTRICT,
    quantidade      INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario  REAL NOT NULL CHECK (preco_unitario >= 0)
);

CREATE INDEX IF NOT EXISTS idx_stay_client ON stay(client_id);
CREATE INDEX IF NOT EXISTS idx_stay_room   ON stay(room_numero);
CREATE INDEX IF NOT EXISTS idx_stay_dates  ON stay(checkin, checkout);
CREATE INDEX IF NOT EXISTS idx_bill_stay   ON bill_item(stay_id);

INSERT OR IGNORE INTO item (nome, preco) VALUES
    ('Frigobar', 15.00),
    ('Lavanderia', 30.00),
    ('Serviço de Quarto', 25.00);
*/