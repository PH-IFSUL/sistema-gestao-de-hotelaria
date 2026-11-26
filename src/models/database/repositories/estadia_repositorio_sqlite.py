"""Repositório de estadias e faturas no SQLite."""

from datetime import datetime
import sqlite3
from typing import List, Optional

from ...estadia import Estadia
from ...fatura import Fatura
from ...item import Item, ItemFatura
from ..conexao import ConexaoBanco
from ..interfaces.cliente_repositorio_interface import ClienteRepositorio
from ..interfaces.quarto_repositorio_interface import QuartoRepositorio


class EstadiaRepositorioSQLite:
    """Persistência de estadias e itens de fatura em banco SQLite."""

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

    def salvar(self, estadia: Estadia) -> None:
        cliente_id = estadia.hospede.get_id()
        if cliente_id is None:
            raise ValueError("O cliente selecionado não possui ID cadastrado.")
        if estadia.quarto is None:
            raise ValueError("Selecione um quarto para a estadia.")

        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO estadias (cliente_id, quarto_numero, reserva_id, data_checkin, data_checkout, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    cliente_id,
                    estadia.quarto.get_numero(),
                    estadia.reserva_id,
                    estadia.data_checkin.isoformat(),
                    estadia.data_checkout.isoformat(),
                    estadia.status,
                ),
            )
            self._conexao.commit()
            estadia.id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível salvar a estadia: {erro}") from erro

    def atualizar(self, estadia: Estadia) -> bool:
        if estadia.id is None:
            return False
        cliente_id = estadia.hospede.get_id()
        if cliente_id is None or estadia.quarto is None:
            return False

        try:
            cursor = self._conexao.execute(
                """
                UPDATE estadias
                SET cliente_id = ?, quarto_numero = ?, reserva_id = ?,
                    data_checkin = ?, data_checkout = ?, status = ?
                WHERE id = ?
                """,
                (
                    cliente_id,
                    estadia.quarto.get_numero(),
                    estadia.reserva_id,
                    estadia.data_checkin.isoformat(),
                    estadia.data_checkout.isoformat(),
                    estadia.status,
                    estadia.id,
                ),
            )
            self._conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível atualizar a estadia: {erro}") from erro

    def remover(self, id_estadia: int) -> bool:
        cursor = self._conexao.execute(
            "DELETE FROM estadias WHERE id = ?",
            (id_estadia,),
        )
        self._conexao.commit()
        return cursor.rowcount > 0

    def listar(self) -> List[Estadia]:
        linhas = self._conexao.execute(
            """
            SELECT id, cliente_id, quarto_numero, reserva_id, data_checkin, data_checkout, status
            FROM estadias
            ORDER BY CASE WHEN status = 'HOSPEDADO' THEN 0 ELSE 1 END, id DESC
            """
        ).fetchall()
        return [self._converter_linha(linha) for linha in linhas]

    def buscar_por_id(self, id_busca: int) -> Optional[Estadia]:
        linha = self._conexao.execute(
            """
            SELECT id, cliente_id, quarto_numero, reserva_id, data_checkin, data_checkout, status
            FROM estadias
            WHERE id = ?
            """,
            (id_busca,),
        ).fetchone()
        return self._converter_linha(linha) if linha else None

    def obter_fatura(self, id_estadia: int) -> Optional[Fatura]:
        estadia = self.buscar_por_id(id_estadia)
        return estadia.fatura if estadia is not None else None

    def listar_itens_catalogo(self) -> List[Item]:
        linhas = self._conexao.execute(
            "SELECT id, nome, preco FROM itens ORDER BY id"
        ).fetchall()
        return [
            Item(id=linha["id"], nome=linha["nome"], preco=linha["preco"])
            for linha in linhas
        ]

    def adicionar_item_fatura(self, id_estadia: int, item_fatura: ItemFatura) -> None:
        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO itens_fatura (estadia_id, item_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (
                    id_estadia,
                    item_fatura.item.id,
                    item_fatura.quantidade,
                    item_fatura.item.preco,
                ),
            )
            self._conexao.commit()
            item_fatura.id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível lançar item na fatura: {erro}") from erro

    def _carregar_fatura(self, estadia_id: int) -> Fatura:
        fatura = Fatura(id_estadia=estadia_id)
        linhas = self._conexao.execute(
            """
            SELECT inf.id, inf.item_id, inf.quantidade, inf.preco_unitario, it.nome
            FROM itens_fatura inf
            JOIN itens it ON it.id = inf.item_id
            WHERE inf.estadia_id = ?
            ORDER BY inf.id
            """,
            (estadia_id,),
        ).fetchall()
        for linha in linhas:
            item = Item(
                id=linha["item_id"],
                nome=linha["nome"],
                preco=linha["preco_unitario"],
            )
            fatura.adicionar_item(
                ItemFatura(
                    id=linha["id"],
                    item=item,
                    quantidade=linha["quantidade"],
                )
            )
        return fatura

    def _converter_linha(self, linha: sqlite3.Row) -> Estadia:
        cliente = self._cliente_repo.buscar_por_id(linha["cliente_id"])
        quarto = self._quarto_repo.buscar_por_numero(linha["quarto_numero"])
        if cliente is None:
            raise ValueError(f"Cliente ID {linha['cliente_id']} não encontrado.")
        if quarto is None:
            raise ValueError(f"Quarto {linha['quarto_numero']} não encontrado.")

        estadia = Estadia(
            hospede=cliente,
            quarto=quarto,
            data_checkin=datetime.fromisoformat(linha["data_checkin"]),
            data_checkout=datetime.fromisoformat(linha["data_checkout"]),
            status=linha["status"],
            reserva_id=linha["reserva_id"],
            id=linha["id"],
        )
        estadia.fatura = self._carregar_fatura(linha["id"])
        return estadia

    def fechar(self) -> None:
        if self._gerencia_banco:
            self._banco.fechar()
