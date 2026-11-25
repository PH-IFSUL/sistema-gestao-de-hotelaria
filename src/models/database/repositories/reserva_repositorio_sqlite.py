"""Repositório de reservas no SQLite."""

from datetime import date
import sqlite3
from typing import List, Optional

from ...estadia import Reserva
from ..conexao import ConexaoBanco
from ..interfaces.cliente_repositorio_interface import ClienteRepositorio
from ..interfaces.quarto_repositorio_interface import QuartoRepositorio


class ReservaRepositorioSQLite:
    """Persistência de reservas em banco SQLite."""

    def __init__(
        self,
        banco: ConexaoBanco | None,
        cliente_repo: ClienteRepositorio,
        quarto_repo: QuartoRepositorio,
    ) -> None:
        self._gerencia_banco = banco is None
        self._banco = banco if banco is not None else ConexaoBanco()
        self._conexao = self._banco.obter_conexao()
        self._cliente_repo = cliente_repo
        self._quarto_repo = quarto_repo

    def salvar(self, reserva: Reserva) -> None:
        cliente_id = reserva.hospede.get_id()
        if cliente_id is None:
            raise ValueError("O cliente selecionado não possui ID cadastrado.")
        if reserva.quarto is None:
            raise ValueError("Selecione um quarto para a reserva.")

        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO reservas (cliente_id, quarto_numero, data_checkin, data_checkout, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    cliente_id,
                    reserva.quarto.get_numero(),
                    reserva.data_checkin.isoformat(),
                    reserva.data_checkout.isoformat(),
                    reserva.status,
                ),
            )
            self._conexao.commit()
            reserva.id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível salvar a reserva: {erro}") from erro

    def atualizar(self, reserva: Reserva) -> bool:
        if reserva.id is None:
            return False
        cliente_id = reserva.hospede.get_id()
        if cliente_id is None:
            raise ValueError("O cliente selecionado não possui ID cadastrado.")
        if reserva.quarto is None:
            raise ValueError("Selecione um quarto para a reserva.")

        try:
            cursor = self._conexao.execute(
                """
                UPDATE reservas
                SET cliente_id = ?, quarto_numero = ?, data_checkin = ?, data_checkout = ?, status = ?
                WHERE id = ?
                """,
                (
                    cliente_id,
                    reserva.quarto.get_numero(),
                    reserva.data_checkin.isoformat(),
                    reserva.data_checkout.isoformat(),
                    reserva.status,
                    reserva.id,
                ),
            )
            self._conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível atualizar a reserva: {erro}") from erro

    def remover(self, id_reserva: int) -> bool:
        cursor = self._conexao.execute(
            "DELETE FROM reservas WHERE id = ?",
            (id_reserva,),
        )
        self._conexao.commit()
        return cursor.rowcount > 0

    def listar(self) -> List[Reserva]:
        linhas = self._conexao.execute(
            """
            SELECT id, cliente_id, quarto_numero, data_checkin, data_checkout, status
            FROM reservas
            ORDER BY data_checkin, id
            """
        ).fetchall()
        return [self._converter_linha(linha) for linha in linhas]

    def buscar_por_id(self, id_reserva: int) -> Optional[Reserva]:
        linha = self._conexao.execute(
            """
            SELECT id, cliente_id, quarto_numero, data_checkin, data_checkout, status
            FROM reservas
            WHERE id = ?
            """,
            (id_reserva,),
        ).fetchone()
        return self._converter_linha(linha) if linha else None

    def existe_conflito(
        self,
        numero_quarto: int,
        data_inicio: date,
        data_fim: date,
        ignorar_id: int | None = None
    ) -> bool:
        params: list[object] = [
            numero_quarto,
            data_fim.isoformat(),
            data_inicio.isoformat(),
        ]
        sql = """
            SELECT 1
            FROM reservas
            WHERE quarto_numero = ?
              AND status = 'CONFIRMADA'
              AND data_checkin < ?
              AND data_checkout > ?
        """
        if ignorar_id is not None:
            sql += " AND id != ?"
            params.append(ignorar_id)

        linha = self._conexao.execute(sql + " LIMIT 1", params).fetchone()
        return linha is not None

    def _converter_linha(self, linha: sqlite3.Row) -> Reserva:
        cliente = self._cliente_repo.buscar_por_id(linha["cliente_id"])
        quarto = self._quarto_repo.buscar_por_numero(linha["quarto_numero"])
        if cliente is None:
            raise ValueError(f"Cliente ID {linha['cliente_id']} não encontrado.")
        if quarto is None:
            raise ValueError(f"Quarto {linha['quarto_numero']} não encontrado.")

        return Reserva(
            hospede=cliente,
            data_checkin=date.fromisoformat(linha["data_checkin"]),
            data_checkout=date.fromisoformat(linha["data_checkout"]),
            quarto=quarto,
            status=linha["status"],
            id=linha["id"],
        )

    def fechar(self) -> None:
        if self._gerencia_banco:
            self._banco.fechar()
