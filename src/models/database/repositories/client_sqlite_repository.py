import sqlite3
from typing import List, Optional
from models.client.client import Client


class SQLite_Client_Repository:

    def __init__(self, conexao: sqlite3.Connection) -> None:
        self._conn = conexao

    @staticmethod
    def _to_client(row: sqlite3.Row) -> Client:
        return Client(row["nome"], row["cpf"], row["telefone"],
                      row["email"], id=row["id"])

    def save(self, cliente: Client) -> None:
        try:
            with self._conn:
                cur = self._conn.execute(
                    "INSERT INTO client (nome, cpf, telefone, email) "
                    "VALUES (?, ?, ?, ?)",
                    (cliente.get_nome(), cliente.get_cpf(),
                     cliente.get_telefone(), cliente.get_email()))
        except sqlite3.IntegrityError:
            raise ValueError(
                f"Já existe um cliente com o CPF {cliente.get_cpf()}.")
        cliente.set_id(cur.lastrowid)

    def delete(self, client_cpf: str) -> bool:
        try:
            with self._conn:
                cur = self._conn.execute(
                    "DELETE FROM client WHERE cpf = ?", (client_cpf,))
        except sqlite3.IntegrityError:
            raise ValueError("Cliente possui estadias registradas e não "
                             "pode ser removido.")
        return cur.rowcount > 0

    def get_all(self) -> List[Client]:
        rows = self._conn.execute(
            "SELECT * FROM client ORDER BY id").fetchall()
        return [self._to_client(r) for r in rows]

    def find_by_id(self, id_query: int) -> Optional[Client]:
        row = self._conn.execute(
            "SELECT * FROM client WHERE id = ?", (id_query,)).fetchone()
        return self._to_client(row) if row else None

    def find_by_Cpf(self, cpf_query: str) -> Optional[Client]:
        row = self._conn.execute(
            "SELECT * FROM client WHERE cpf = ?", (cpf_query,)).fetchone()
        return self._to_client(row) if row else None

    def update(self, guest: Client) -> bool:
        if guest.get_id() is None:
            return False
        try:
            with self._conn:
                cur = self._conn.execute(
                    "UPDATE client SET nome = ?, cpf = ?, telefone = ?, "
                    "email = ? WHERE id = ?",
                    (guest.get_nome(), guest.get_cpf(), guest.get_telefone(),
                     guest.get_email(), guest.get_id()))
        except sqlite3.IntegrityError:
            raise ValueError(
                f"Já existe um cliente com o CPF {guest.get_cpf()}.")
        return cur.rowcount > 0