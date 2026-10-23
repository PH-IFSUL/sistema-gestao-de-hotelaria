import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parents[3] / "data" / "hotel.db" ## onde fica o banco 
                                                                          ##parents[0] é database/ 
                                                                          ##parents[1] é models/
                                                                          ##parents[2] é src/
                                                                          ##parents[3] é a raiz do projeto


class Database_Connection:
    ## construtor
    def __init__(self) -> None:
        CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True) 
        self._conexao = sqlite3.connect(CAMINHO_BANCO)
    
    ## métodos
    def get_connection(self) -> sqlite3.Connection:
        return self._conexao

    def close(self) -> None:
        self._conexao.close()

## teste - mostra aonde está o banco de dados e fecha
if __name__ == "__main__":
    banco = Database_Connection()
    print("Conectado em:", CAMINHO_BANCO)
    banco.close()