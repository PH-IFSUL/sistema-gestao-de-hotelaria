import sqlite3
from typing import List, Optional

from ...quarto import Quarto
from ...estado_quarto import (
    Disponivel,
    Reservado,
    Ocupado,
    Limpeza,
    Manutencao,
)
from ..conexao import ConexaoBanco


class QuartoRepositorioSQLite:

    ESTADOS = {
        "disponivel": Disponivel,
        "reservado": Reservado,
        "ocupado": Ocupado,
        "limpeza": Limpeza,
        "manutencao": Manutencao,
    }

    def __init__(self, banco: ConexaoBanco | None = None) -> None:
        self._gerencia_banco = banco is None
        self._banco = banco if banco is not None else ConexaoBanco()
        self._conexao = self._banco.obter_conexao()

    def adicionar(self, quarto: Quarto) -> None:

        numero = quarto.get_numero()

        if self.buscar_por_numero(numero) is not None:
            raise ValueError(
                f"Já existe um quarto com o número {numero}."
            )

        estado = str(quarto.estado)

        try:
            self._conexao.execute(
                """
                INSERT INTO quartos (numero, tipo, valor_diaria, estado)
                VALUES (?, ?, ?, ?)
                """,
                (
                    numero,
                    quarto.get_tipo(),
                    quarto.get_valor_diaria(),
                    estado,
                ),
            )
            self._conexao.commit()

        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(
                f"Não foi possível adicionar o quarto {numero}: {erro}"
            ) from erro

    def remover(self, numero_busca: int) -> bool:

        cursor = self._conexao.execute(
            "DELETE FROM quartos WHERE numero = ?",
            (numero_busca,),
        )

        self._conexao.commit()
        return cursor.rowcount > 0

    def listar(self) -> List[Quarto]:

        cursor = self._conexao.execute(
            """
            SELECT numero, tipo, valor_diaria, estado
            FROM quartos
            ORDER BY numero
            """
        )

        return [self._converter_quarto(linha) for linha in cursor.fetchall()]

    def buscar_por_numero(self, numero_busca: int) -> Optional[Quarto]:

        cursor = self._conexao.execute(
            """
            SELECT numero, tipo, valor_diaria, estado
            FROM quartos
            WHERE numero = ?
            """,
            (numero_busca,),
        )

        linha = cursor.fetchone()

        if linha is None:
            return None

        return self._converter_quarto(linha)

    def obter_tipos(self) -> List[str]:

        cursor = self._conexao.execute(
            """
            SELECT DISTINCT tipo
            FROM quartos
            ORDER BY tipo
            """
        )

        return [linha["tipo"] for linha in cursor.fetchall()]

    def _converter_quarto(self, linha: sqlite3.Row) -> Quarto:

        quarto = Quarto(
            numero=linha["numero"],
            tipo=linha["tipo"],
            valor_diaria=linha["valor_diaria"],
        )

        estado = linha["estado"]
        classe_estado = self.ESTADOS.get(estado)

        if classe_estado is None:
            raise ValueError(f"Estado de quarto desconhecido: {estado}")

        quarto.estado.set_estado(classe_estado())

        return quarto

    def fechar(self) -> None:
        if self._gerencia_banco:
            self._banco.fechar()
