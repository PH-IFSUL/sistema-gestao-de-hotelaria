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