import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parents[3] / "data" / "hotel.db"


class Database_Connection:

    def __init__(self) -> None:
        CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True) 
        self._conexao = sqlite3.connect(CAMINHO_BANCO)

    def get_connection(self) -> sqlite3.Connection:
        return self._conexao

    def close(self) -> None:
        self._conexao.close()


if __name__ == "__main__":
    banco = Database_Connection()
    print("Conectado em:", CAMINHO_BANCO)
    banco.close()