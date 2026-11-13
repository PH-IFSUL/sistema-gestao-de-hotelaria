import sqlite3
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[3]
CAMINHO_BANCO = RAIZ_PROJETO / "data" / "hotelaria.db"
##parents[0] é database/ 
##parents[1] é models/
##parents[2] é src/
##parents[3] é a raiz do projeto
CAMINHO_ESQUEMA = Path(__file__).resolve().parent / "schema.sql"


class ConexaoBanco:

    def __init__(self, caminho: str | Path = CAMINHO_BANCO) -> None:
        self._caminho = str(caminho)
        self._conexao: sqlite3.Connection | None = None

    def conectar(self) -> sqlite3.Connection:
        """conexão com bd"""
        if self._conexao is not None:
            return self._conexao

        if self._caminho != ":memory:":
            Path(self._caminho).parent.mkdir(parents=True, exist_ok=True)

        self._conexao = sqlite3.connect(self._caminho)
        self._conexao.row_factory = sqlite3.Row
        self._conexao.execute("PRAGMA foreign_keys = ON") #para ligar o SQLite
        self._conexao.execute("PRAGMA busy_timeout = 5000")

        try:
            self._inicializar_esquema()
        except Exception:
            self._conexao.close()
            self._conexao = None
            raise

        return self._conexao

    def obter_conexao(self) -> sqlite3.Connection:
        """retorna a conexão ativa"""
        return self.conectar()

    def _inicializar_esquema(self) -> None:
        """esquema SQL"""
        if self._conexao is None:
            raise RuntimeError("Conexão não esbalecida com o banco")

        if not CAMINHO_ESQUEMA.is_file():
            raise FileNotFoundError(
                f"Esquema não encontrado: {CAMINHO_ESQUEMA}"
            )

        script = CAMINHO_ESQUEMA.read_text(encoding="utf-8")
        self._conexao.executescript(script)
        self._conexao.commit()

    def fechar(self) -> None:
        if self._conexao is not None:
            self._conexao.close()
            self._conexao = None

    def __enter__(self) -> "ConexaoBanco":
        self.conectar()
        return self

    def __exit__(self, tipo_erro, erro, rastreamento) -> None:
        self.fechar()


##mostra aonde está o banco de dados, lista as tabelas e fecha
if __name__ == "__main__":
    banco = ConexaoBanco()
    conexao = banco.conectar()

    tabelas = conexao.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    ).fetchall()

    print(f"Banco conectado em: {CAMINHO_BANCO}")
    print("Tabelas disponíveis:", [tabela["name"] for tabela in tabelas])

    banco.fechar()
