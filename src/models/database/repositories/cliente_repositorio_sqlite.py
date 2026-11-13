"""Reposiório de clientes no SQLite"""

import sqlite3
from typing import Optional

from ...cliente import Cliente
from ..conexao import ConexaoBanco


class ClienteRepositorioSQLite:

    def __init__(self, banco: ConexaoBanco | None = None) -> None:
        self._gerencia_banco = banco is None
        self._banco = banco if banco is not None else ConexaoBanco()
        self._conexao = self._banco.obter_conexao()

    def salvar(self, cliente: Cliente) -> None:
        try:
            cursor = self._conexao.execute(
                """
                INSERT INTO clientes (nome, cpf, telefone, email)
                VALUES (?, ?, ?, ?)
                """,
                (
                    cliente.get_nome(),
                    cliente.get_cpf(),
                    cliente.get_telefone(),
                    cliente.get_email(),
                ),
            )
            self._conexao.commit()
            cliente.set_id(cursor.lastrowid)
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            if "clientes.cpf" in str(erro).lower() or "unique constraint" in str(erro).lower():
                raise ValueError(
                    f"Já existe um cliente com o CPF {cliente.get_cpf()}."
                ) from erro
            raise ValueError(f"Não foi possível cadastrar o cliente: {erro}") from erro

    def remover(self, cpf_cliente: str) -> bool:
        cursor = self._conexao.execute(
            "DELETE FROM clientes WHERE cpf = ?",
            (cpf_cliente,),
        )
        self._conexao.commit()
        return cursor.rowcount > 0

    def obter_todos(self) -> list[Cliente]:
        linhas = self._conexao.execute(
            """
            SELECT id, nome, cpf, telefone, email
            FROM clientes
            ORDER BY id
            """
        ).fetchall()
        return [self._converter_linha(linha) for linha in linhas]

    def buscar_por_id(self, id_busca: int) -> Optional[Cliente]:
        linha = self._conexao.execute(
            """
            SELECT id, nome, cpf, telefone, email
            FROM clientes
            WHERE id = ?
            """,
            (id_busca,),
        ).fetchone()
        return self._converter_linha(linha) if linha else None

    def buscar_por_cpf(self, cpf_busca: str) -> Optional[Cliente]:
        linha = self._conexao.execute(
            """
            SELECT id, nome, cpf, telefone, email
            FROM clientes
            WHERE cpf = ?
            """,
            (cpf_busca,),
        ).fetchone()
        return self._converter_linha(linha) if linha else None

    def atualizar(self, cliente: Cliente) -> bool:
        try:
            cursor = self._conexao.execute(
                """
                UPDATE clientes
                SET nome = ?, telefone = ?, email = ?
                WHERE cpf = ?
                """,
                (
                    cliente.get_nome(),
                    cliente.get_telefone(),
                    cliente.get_email(),
                    cliente.get_cpf(),
                ),
            )
            self._conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            self._conexao.rollback()
            raise ValueError(f"Não foi possível atualizar o cliente: {erro}") from erro

    @staticmethod
    def _converter_linha(linha: sqlite3.Row) -> Cliente:
        cliente = Cliente(
            nome=linha["nome"],
            cpf=linha["cpf"],
            telefone=linha["telefone"],
            email=linha["email"],
            id=linha["id"],
        )
        return cliente

    # Métodos de compatibilidade com nomes antigos da interface.
    def save(self, cliente: Cliente) -> None:
        self.salvar(cliente)

    def delete(self, client_cpf: str) -> bool:
        return self.remover(client_cpf)

    def get_all(self) -> list[Cliente]:
        return self.obter_todos()

    def find_by_id(self, id_query: int) -> Optional[Cliente]:
        return self.buscar_por_id(id_query)

    def find_by_Cpf(self, cpf_query: str) -> Optional[Cliente]:
        return self.buscar_por_cpf(cpf_query)

    def update(self, guest: Cliente) -> bool:
        return self.atualizar(guest)

    def fechar(self) -> None:
        if self._gerencia_banco:
            self._banco.fechar()