import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parents[3] / "data" / "hotel.db" ## onde fica o banco 
                                                                          ##parents[0] é database/ 
                                                                          ##parents[1] é models/
                                                                          ##parents[2] é src/
                                                                          ##parents[3] é a raiz do projeto
CAMINHO_SCHEMA = Path(__file__).resolve().parent / "schema.sql"


class Database_Connection:
    ## construtor
    def __init__(self, caminho: Path | str = CAMINHO_BANCO) -> None:
        if str(caminho) != ":memory:":
            Path(caminho).parent.mkdir(parents=True, exist_ok=True)
        self._conexao = sqlite3.connect(caminho)
        self._conexao.row_factory = sqlite3.Row
        self._conexao.execute("PRAGMA foreign_keys = ON")  # SQLite não liga por padrão
        self.init_schema()

    def init_schema(self) -> None:
        script = CAMINHO_SCHEMA.read_text(encoding="utf-8")
        self._conexao.executescript(script)
        self._conexao.commit()
    
    ## métodos
    def get_connection(self) -> sqlite3.Connection:
        return self._conexao

    def close(self) -> None:
        self._conexao.close()

## teste - mostra aonde está o banco de dados, lista as tabelas e fecha
if __name__ == "__main__":
    banco = Database_Connection()
    print("Conectado em:", CAMINHO_BANCO)
    tabelas = banco.get_connection().execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    print("Tabelas:", [t["name"] for t in tabelas])
    banco.close()